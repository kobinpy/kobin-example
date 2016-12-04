from kobin import request, RedirectResponse
from .. import app
from ..service import github as github_service


def github_oauth_callback():
    code = request.query['code']
    payload = {
        "client_id": app.config.get('GITHUB_CLIENT_ID'),
        "client_secret": app.config.get('GITHUB_CLIENT_SECRET'),
        "code": code,
    }
    access_token = github_service.get_access_token(payload)
    user = github_service.get_user(access_token)

    r = app.config.get('REDIS')
    r.set('access_token_{id}'.format(id=user["id"]), access_token)
    response = RedirectResponse('/')
    response.set_cookie("session_id", f"access_token_{user['id']}")
    return response
