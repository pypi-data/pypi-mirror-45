from drongo.client import DrongoClient


class NSClient(DrongoClient):
    def __init__(self, *args, **kwargs):
        super(NSClient, self).__init__(*args, **kwargs)
        self._ns = 'core'

    def set_namespace(self, ns):
        self._ns = ns

    def ns_create(self, name, description=None):
        data = {'name': name, 'description': description}
        response = self.post_json(
            '/{ns}/ns'.format(ns=self._ns), data)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def ns_activate(self, uid):
        response = self.get(
            '/{ns}/ns/{uid}/operations/activate'.format(uid=uid, ns=self._ns))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def ns_deactivate(self, uid):
        response = self.get(
            '/{ns}/ns/{uid}/operations/deactivate'.format(
                uid=uid, ns=self._ns))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def ns_get(self, uid):
        response = self.get('/{ns}/ns/{uid}'.format(uid=uid, ns=self._ns))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def ns_update(self, uid, name=None, description=None):
        data = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description

        response = self.put_json(
            '/{ns}/ns/{uid}'.format(uid=uid, ns=self._ns),
            data)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def ns_delete(self, uid):
        response = self.delete('/{ns}/ns/{uid}'.format(uid=uid, ns=self._ns))
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def ns_list(self, active_only=True, page_number=1, page_size=50):
        params = {
            'active_only': 'yes' if active_only else 'no',
            'page_number': str(page_number),
            'page_size': str(page_size)
        }
        response = self.get('/{ns}/ns'.format(ns=self._ns), params=params)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def ns_modules_get_settings(self, module, instance=None):
        if instance is None:
            url = '/{ns}/ns/modules/{module}/settings'.format(
                ns=self._ns, module=module)
        else:
            url = '/{ns}/ns/modules/{module}/{mid}/settings'.format(
                ns=self._ns, module=module, mid=instance)
        response = self.get(url)
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')
