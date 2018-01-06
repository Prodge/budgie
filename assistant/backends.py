from django.contrib.auth import get_user_model
from oauth2_provider.models import AccessToken

User = get_user_model()

class DialogFlowBackend(object):
    """
    DialogFlow does not send requests with an authorization header.
    Instead the users token is in:
        originalRequest > data > user > accessToken
    Here we authenticate the user based on this value
    """

    def authenticate(self, request=None):
        if request is not None and request.body:
            access_token = request.body.get('originalRequest', {}).get('data', {}).get('user', {}).get('accessToken', None)
            try:
                return AccessToken.objects.get(token = access_token).user
            except AccessToken.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
