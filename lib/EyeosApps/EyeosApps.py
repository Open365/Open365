import json
import re

from lib.EyeosApps.EyeosAppsStorage import EyeosAppsStorage
from lib.EyeosApps.EyeosAppsJsonValidator import EyeosAppsJsonValidator
from lib.EyeosApi.Application import Application
from lib.Settings import Settings
from lib.Wrappers.Logger import Logger
from lib.Errors.EyeosAPIError import EyeosAPIError
from lib.EyeosApi.Principals import Principals
from lib.EyeosApi.Login import Login


class EyeosApps:

    DEFAULT_APPS_DIR = './eyeos_apps/default'

    def __init__(self, injected_open=None, injected_eyeos_apps_storage=None, injected_json=None,
                 injected_eyeos_apps_validator=None,
                 injected_application_api=None,
                 injected_principals_api=None,
                 injected_base_group=None,
                 injected_login_api=None):
        self.eyeos_apps_storage = injected_eyeos_apps_storage or EyeosAppsStorage()
        self.open = injected_open or open
        self.json = injected_json or json
        self.logger = Logger(__name__)
        self.eyeos_apps_validator = injected_eyeos_apps_validator or EyeosAppsJsonValidator()
        self.application_api = injected_application_api or Application()
        self.principals_api = injected_principals_api or Principals()
        self.principal_base_group = injected_base_group or Settings().getSettings()['principalservice']['base_group']
        self.login_api = injected_login_api or Login()

    def install(self, apps_directory, admin_user, password, domain):
        apps_file = apps_directory + '/apps.json'

        with self.open(apps_file, 'r') as f:
            try:
                apps = self.json.load(f)
            except ValueError as e:
                raise ValueError("File {0} does not contain valid JSON".format(apps_file)) from e

        self.eyeos_apps_validator.validate(apps)

        try:
            eyeos_card = self.login_api.authenticate(admin_user, password, domain)
            self.logger.info('Emptying previous apps...')
            self.application_api.empty_apps(eyeos_card)
            self.logger.info('Saving apps...')
            self.eyeos_apps_storage.save(apps)
            self.application_api.save(apps, eyeos_card)
            group = self.principals_api.get_systemgroup(self.principal_base_group, eyeos_card)
            group = self._generate_new_permissions(apps, group)
            self.principals_api.put_systemgroup(group, eyeos_card)

        except (ValueError, KeyError, EyeosAPIError) as e:
            self.logger.error(e)
            exit(1)

    def _generate_new_permissions(self, applications, group):
        """ existing permissions like eyeos.application.* should be removed
        and then add new eyeos.applications.whatever permissions for each eyeos_apps applications.
        permissions like eyeos.admin.*.edit should be removed and add new ones from the
        control_panel applications

        the eyeos.admin.*.edit permissions might pose a problem in the future if there appear new
        permissions not tied to an application. That's a problem for future everyone :S
        """

        permissions = group['permissions']

        i = 0
        while i < len(permissions):
            permission = permissions[i]
            if (re.match(r'^eyeos\.application\.[^.]*$', permission['id']) or
                    re.match(r'^eyeos\.admin\.[^.]*\.edit$', permission['id'])):
                permissions.remove(permission)
                continue
            i += 1

        for eyeos_application in applications['eyeosApps']:
            permissions.append({
                "id": "eyeos.application." + eyeos_application['appID'],
                "name": 'Execute ' + eyeos_application['name'],
                "description": "Run " + eyeos_application['name'] + " application",
                "enabled": True
            })
        for admin_application in applications['controlPanelApps']:
            permissions.append({
                "id": "eyeos.admin." + admin_application['appID'] + '.edit',
                "name": 'Manage ' + admin_application['name'],
                "description": "Manage " + admin_application['name'] + " in admin panel",
                "enabled": False
            })

        return group
