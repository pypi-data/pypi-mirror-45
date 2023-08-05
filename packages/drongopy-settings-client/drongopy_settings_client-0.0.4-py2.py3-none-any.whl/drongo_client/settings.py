from drongo.client import DrongoClient


class SettingsClient(DrongoClient):
    def __init__(self, *args, **kwargs):
        super(SettingsClient, self).__init__(*args, **kwargs)
        self._ns = 'core'

    def set_namespace(self, ns):
        self._ns = ns

    def settings_set(self, mod, settings):
        response = self.put_json(
            '/{ns}/settings/{mod}'.format(mod=mod, ns=self._ns), settings)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']

    def settings_get(self, mod):
        response = self.get(
            '/{ns}/settings/{mod}'.format(mod=mod, ns=self._ns))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response['payload']
