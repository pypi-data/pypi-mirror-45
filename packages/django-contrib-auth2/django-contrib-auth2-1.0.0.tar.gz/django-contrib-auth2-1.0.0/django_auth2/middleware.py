from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.core.exceptions import SuspiciousOperation
from django.utils.functional import SimpleLazyObject


def set_authenticated_user(request, user_id):
    request.session.flush()
    request.session.cycle_key()

    request.session['_user_id'] = user_id


class HttpAuthorizationSessionMiddleware:
    @staticmethod
    def get_session_key(request):
        authorization = request.META.get('HTTP_AUTHORIZATION', '')

        if authorization.startswith('Bearer '):
            return authorization[6:].strip()

        return None

    def __init__(self, get_response):
        self.get_response = get_response
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def __call__(self, request):
        session_key = self.get_session_key(request)
        request.session = self.SessionStore(session_key)

        response = self.get_response(request)

        try:
            modified = request.session.modified
            empty = request.session.is_empty()
        except AttributeError:
            return response

        if not empty and (modified or settings.SESSION_SAVE_EVERY_REQUEST):
            if response.status_code != 500:
                try:
                    request.session.save()
                except UpdateError:
                    raise SuspiciousOperation(
                        "The request's session was deleted before the "
                        "request completed. The user may have logged "
                        "out in a concurrent request, for example."
                    )
        return response


class Auth2Middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.USER_MODEL = apps.get_model(settings.AUTH_USER_MODEL)

    def __call__(self, request):
        User = self.USER_MODEL

        if request.session.get('_user_id'):
            user_id = request.session['_user_id']

            request.user_id = user_id
            request.user = SimpleLazyObject(
                lambda: User.objects.get(id=user_id)
            )

        if settings.DEBUG and request.GET.get('user_id'):
            user_id = int(request.GET.get('user_id'))

            request.user_id = user_id
            request.user = SimpleLazyObject(
                lambda: User.objects.get(id=user_id)
            )

        setattr(
            request,
            'set_authenticated_user',
            lambda user_id: set_authenticated_user(request, user_id)
        )

        return self.get_response(request)
