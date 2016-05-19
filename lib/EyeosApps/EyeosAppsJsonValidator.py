import re


class EyeosAppsJsonValidator:
    def __init__(self):
        self.required_fields = {
            "eyeosApps": (
                "appID",
                "bigIcon",
                "smallIcon",
                "name",
                "tooltip",
                "description",
                "url",
                "showInDesktop",
                "showInTab",
                "settings",
                "settings.minSize",
                "settings.minSize.height",
                "settings.minSize.width",
                "isVdi",
                "type"
            ),
            "controlPanelApps": (
                "appID",
                "name",
                "icon",
                "link",
                "urlkey",
                "type"
            )
        }
        self.used_app_ids = []

    def validate(self, all_apps):
        for app_type, required_fields in self.required_fields.items():
            apps = all_apps[app_type]
            app_num = 0
            for app in apps:
                app_num += 1
                for required_field in required_fields:
                    context = app
                    for subfield in required_field.split('.'):
                        if subfield not in context:
                            raise ValueError("missing '{0}' required field in application #{1} of {2}"
                                             .format(required_field,
                                                     app_num,
                                                     app_type))
                        context = context[subfield]

                if not self._validate_app_id(app['appID']):
                    raise ValueError("appID '{0}' of app #{1} ({2}) is not valid"
                                     .format(app['appID'], app_num, app_type))

                if app['appID'] in self.used_app_ids:
                    raise ValueError("duplicated appID '{0}' (duplicated found in app #{1} of {2})"
                                     .format(app['appID'], app_num, app_type))
                self.used_app_ids.append(app['appID'])

        # if we haven't returned earlier, all is good :)
        return True

    def _validate_app_id(self, app_id):
        # app_id cannot contain dots or whitespace
        return not re.search(r'[\s.]', app_id)
