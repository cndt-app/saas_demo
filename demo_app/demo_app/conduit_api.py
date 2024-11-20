import requests


BASE_URL = 'https://api.getconduit.app/v2/'


def workspaces_list(token):
    return _request('GET', 'workspaces/', token)


def workspaces_create(token, name, ext_id):
    return _request('POST', 'workspaces/', token, {'name': name, 'ext_id': ext_id})


def dashboards_list(token):
    return _request('GET', 'dashboards/', token)


def dashboards_get_url(token, dashboard_id):
    return _request('GET', f'dashboards/{dashboard_id}/share/', token)


def dashboards_clone(token, dashboard_id, workspace_id):
    return _request('POST', f'dashboards/{dashboard_id}/clone/', token, {'workspace': workspace_id})


def _request(method, path, token, data=None):
    res = requests.request(
        method,
        f'{BASE_URL}{path}',
        headers={'Authorization': f'Bearer {token}'},
        json=data,
    )
    res.raise_for_status()

    return res.json()