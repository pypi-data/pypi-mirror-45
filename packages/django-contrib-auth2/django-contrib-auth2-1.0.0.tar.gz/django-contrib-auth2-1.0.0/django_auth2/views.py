from django.db import transaction
from django.http import JsonResponse
from django.views import View

from .authentication import create_refresh_token, load_refresh_token, \
    extend_refresh_token
from .forms import LoginForm, LoginRefreshForm
from .models import get_oauth_userinfo, InvalidProviderAccessToken, \
    InvalidRefreshToken


class LoginWithProvider(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({
                'status': 'error',
                'error': 'invalid_method',
            }, status=405)

        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic()
    def post(self, request):
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            return JsonResponse({
                'status': 'error',
                'error': 'bad_request',
                'error_details': form.errors.get_json_data()
            })
        data = form.clean()

        provider = data['provider']
        device_id = data['device_id']

        credentials = {
            'access_token': data['provider_access_token']
        }
        try:
            userinfo = get_oauth_userinfo(provider, credentials)
        except InvalidProviderAccessToken:
            return JsonResponse({
                'status': 'error',
                'error': 'invalid_access_token',
            }, status=400)
        except RuntimeError as e:
            return JsonResponse({
                'status': 'error',
                'error': 'internal_server_error',
                'error_details': str(e)
            }, status=500)

        user = self.get_or_create_user(provider, userinfo)
        request.set_authenticated_user(user.id)

        return JsonResponse({
            'status': 'ok',
            'credentials': {
                'access_token': request.session.session_key,
                'refresh_token': create_refresh_token(user.id, device_id)
            }
        })

    def get_or_create_user(self, provider, userinfo):
        raise NotImplementedError()


class RefreshAuthentication(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({
                'status': 'error',
                'error': 'invalid_method',
            }, status=405)

        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic()
    def post(self, request):
        form = LoginRefreshForm(data=request.POST)
        if not form.is_valid():
            return JsonResponse({
                'status': 'error',
                'error': 'bad_request',
                'error_details': form.errors.get_json_data()
            })
        data = form.clean()

        device_id = data['device_id']

        try:
            (user_id, device_id) = load_refresh_token(
                data['refresh_token'], device_id
            )

        except InvalidRefreshToken:
            return JsonResponse({
                'status': 'error',
                'error': 'invalid_refresh_token',
            })

        request.set_authenticated_user(user_id)

        return JsonResponse({
            'status': 'ok',
            'credentials': {
                'access_token': request.session.session_key,
                'refresh_token': extend_refresh_token(data['refresh_token'])
            }
        })
