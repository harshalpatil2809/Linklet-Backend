from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def on_authentication_error(self, request, provider, error=None, exception=None, extra_context=None):
        # User ko wapas Next.js login page par bhej do with error code
        return redirect(f"{settings.FRONTEND_URL}/login?error=email_exists")