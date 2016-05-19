from lib.Settings import Settings


class DefaultProfileProvider:
    def __init__(self, settings=None):
        self.settings = settings or Settings()

    def get_default_profiles(self):
        default_profile = 'all'
        profile = default_profile
        settings = self.settings.getSettings()
        try:
            profile = settings['general']['profiles_to_use'].strip() or default_profile
        except KeyError:
            profile = default_profile

        return profile.replace(',', ' ').split()
