from rest_framework_simplejwt.tokens import RefreshToken


# this function is used to generate the tokens for authorization
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
