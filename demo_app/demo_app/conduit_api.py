import requests
from dataclasses import dataclass


BASE_URL = 'https://api.getconduit.app/v2/'


@dataclass
class ConduitAPIError(Exception):
    code: str
    message: str
    http_code: int


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
    try:
        res = requests.request(
            method,
            f'{BASE_URL}{path}',
            headers={'Authorization': f'Bearer {token}'},
            json=data,
        )
    except requests.exceptions.RequestException as e:
        raise ConduitAPIError(code='http_error', message=str(e), http_code=0) from e

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        code = None
        message = None

        if e.response.status_code == 400:
            data = e.response.json()
            code = data['code']
            message = data['message']

        if e.response.status_code == 401:
            code='auth'
            message='Invalid token'

        raise ConduitAPIError(
            code=code or 'unknown',
            message=message or str(e),
            http_code=e.response.status_code,
        ) from e

    return res.json()