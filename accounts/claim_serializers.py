from datetime import timedelta
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken


class CustomAccessToken(AccessToken):
    """Custom access token that includes the user role"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add role and username to the token
        if self.payload.get('user_id'):
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(id=self.payload['user_id'])
                self.payload['role'] = user.role
                self.payload['username'] = user.username
            except User.DoesNotExist:
                pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer that includes role in the response"""
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add the user role and username to the response
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['role'] = user.role
        token['username'] = user.username
        return token
