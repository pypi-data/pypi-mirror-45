from drongo.client import DrongoClient


class AuthClient(DrongoClient):
    def __init__(self, *args, **kwargs):
        super(AuthClient, self).__init__(*args, **kwargs)
        self._ns = 'core'

    def set_namespace(self, ns):
        self._ns = ns

    def user_from_token(self, token):
        response = self.get(
            '/{ns}/users/from-token'.format(ns=self._ns),
            params={'token': token})
        if response['status'] == 'ERROR':
            return False, None
        else:
            return True, response.get('payload')

    def user_create(self, username, password):
        login_data = {'username': username, 'password': password}
        response = self.post_json(
            '/{ns}/users'.format(ns=self._ns),
            login_data)
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_verify_credentials(self, username, password):
        login_data = {'username': username, 'password': password}
        response = self.post_json(
            '/{ns}/users/operations/verify-credentials'.format(ns=self._ns),
            login_data)
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_token_create(self, username):
        url = '/{ns}/users/{username}/operations/token-create'.format(
            username=username,
            ns=self._ns
        )
        response = self.post_json(url, {})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_token_delete(self, token):
        url = '/{ns}/users/operations/token-delete'.format(ns=self._ns)
        response = self.delete(url, params={'token': token})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_token_refresh(self, token):
        pass  # FIXME: Implement

    def user_login(self, username, password):
        status, _ = self.user_verify_credentials(username, password)
        if status:
            status, token = self.user_token_create(username)
            if status:
                return True, token
        return False, None

    def user_change_password(self, username, password):
        login_data = {'username': username, 'password': password}
        response = self.post_json(
            '/{ns}/users/operations/change-password'.format(ns=self._ns),
            login_data)
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_logout(self, token):
        self.user_token_delete(token)

    def user_activate(self, username):
        response = self.post_json(
            '/{ns}/users/{username}/operations/activate'.format(
                username=username, ns=self._ns), {}
        )
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_deactivate(self, username):
        response = self.post_json(
            '/{ns}/users/{username}/operations/deactivate'.format(
                username=username, ns=self._ns), {}
        )
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_list(self, active_only=True, page_number=1, page_size=50):
        response = self.get('/{ns}/users'.format(ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def group_create(self, groupname):
        response = self.post_json(
            '/{ns}/groups'.format(ns=self._ns), {'name': groupname})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def group_delete(self, groupname):
        response = self.delete(
            '/{ns}/groups/{groupname}'.format(
                groupname=groupname, ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def group_list(self, page_number=1, page_size=50):
        response = self.get(
            '/{ns}/groups'.format(ns=self._ns),
            {'page_number': page_number, 'page_size': page_size})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def group_add_user(self, groupname, username):
        response = self.post_json(
            '/{ns}/groups/{groupname}/users'.format(
                groupname=groupname,
                ns=self._ns
            ),
            {'username': username}
        )
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def group_delete_user(self, groupname, username):
        response = self.delete(
            '/{ns}/groups/{groupname}/users/{username}'.format(
                groupname=groupname, username=username, ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def group_list_users(self, groupname):
        response = self.get(
            '/{ns}/groups/{groupname}/users'.format(
                groupname=groupname, ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def user_list_groups(self, username):
        response = self.get(
            '/{ns}/users/{username}/groups'.format(
                username=username, ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def permission_add_client(self, permission_id, client):
        response = self.post_json(
            '/{ns}/permissions/{permission_id}/clients'.format(
                permission_id=permission_id, ns=self._ns),
            {'client': client})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def permission_delete_client(self, permission_id, client):
        response = self.delete(
            '/{ns}/permissions/{permission_id}/clients/{client}'.format(
                permission_id=permission_id,
                client=client,
                ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def permission_list_clients(self, permission_id):
        response = self.get(
            '/{ns}/permissions/{permission_id}/clients'.format(
                permission_id=permission_id, ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def permission_check_user(self, permission_id, username):
        response = self.post_json(
            '/{ns}/permissions/{permission_id}/check-user'.format(
                permission_id=permission_id, ns=self._ns),
            {'username': username})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def object_permission_add_client(
            self, object_type, object_id, permission_id, client):
        response = self.post_json(
            (
                '/{ns}/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/clients'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id,
                ns=self._ns),
            {'client': client}
        )
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def object_permission_delete_client(
            self, object_type, object_id, permission_id, client):
        response = self.delete(
            (
                '/{ns}/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/clients/{client}'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id,
                client=client,
                ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def object_permission_list_clients(
            self, object_type, object_id, permission_id):
        response = self.get(
            (
                '/{ns}/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/clients'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id,
                ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def object_permission_check_user(
            self, object_type, object_id, permission_id, username):
        response = self.post_json(
            (
                '/{ns}/permissions/{permission_id}/objects/'
                '{object_type}/{object_id}/check-user'
            ).format(
                permission_id=permission_id,
                object_type=object_type,
                object_id=object_id,
                ns=self._ns),
            {'username': username})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def object_owner_set(self, object_type, object_id, username):
        response = self.put_json(
            (
                '/{ns}/objects/{object_type}/'
                '{object_id}/operations/set-owner'
            ).format(
                object_type=object_type,
                object_id=object_id,
                ns=self._ns),
            {'username': username})
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])

    def object_owner_get(self, object_type, object_id):
        response = self.get(
            '/{ns}/objects/{object_type}/{object_id}/owner'.format(
                object_type=object_type,
                object_id=object_id,
                ns=self._ns))
        if response['status'] == 'OK':
            return True, response.get('payload')
        else:
            return False, response.get('errors', [])
