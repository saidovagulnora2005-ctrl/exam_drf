from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import TokenError, RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    email = request.data.get('email')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    full_name = request.data.get('full_name')
    role = request.data.get('role')

    if not email or not password1 or not full_name or not role:
        return Response({"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST)

    if password1 != password2:
        return Response({"error": "Passwords do not match!"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "This email address already exists!"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(email=email,password=password1,full_name=full_name, role=role)
    refresh = RefreshToken.for_user(user)

    return Response({'refresh': str(refresh),
                     'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    pass
    