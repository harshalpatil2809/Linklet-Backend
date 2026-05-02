from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny]) # 🔥 Ise 'IsAuthenticated' se 'AllowAny' karein
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    print(f"Attempting login for: {username}") # Debug print

    # Django authenticate check
    user = authenticate(username=username, password=password)

    if user is not None:
        print(f"User {username} authenticated successfully!") # Debug print
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'userid': user.id
        }, status=status.HTTP_200_OK)
    else:
        print(f"Authentication failed for user: {username}") # Debug print
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Logout successful 🔥"})

    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        user = request.user
        
        # Check karein agar user object exist karta hai
        if not user:
            return Response(
                {"error": "User found but data is missing"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        # Error ko console/logs mein print karein
        print(f"Error fetching user: {str(e)}")
        
        return Response(
            {"error": "Something went wrong on the server"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def google_login_callback(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("https://intellex-ai-harshal.vercel.app/login?error=social-auth-failed")

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    frontend_url = "https://linklet-by-harshal.vercel.app/auth-callback"
    return redirect(f"{frontend_url}?access={access_token}&refresh={refresh_token}")