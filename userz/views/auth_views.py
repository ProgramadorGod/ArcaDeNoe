from django.http import HttpResponseRedirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.account.views import LogoutView as AllauthLogoutView
from allauth.account.views import LoginView as AllauthLoginView
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import LoginSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from ..models import Account



# if want to use jwt
# class OwnLoginView(APIView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]  # Permitir acceso sin autenticación

#     def post(self, request, *args, **kwargs):
#         # Validamos los datos del serializer
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Obtenemos el username y password del serializer
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']

#         try:
#             # Verificamos si el usuario existe en la base de datos
#             user = Account.objects.get(username=username)
#         except Account.DoesNotExist:
#             # Si el usuario no existe, devolvemos un error
#             return Response({'Detail': 'Invalid Username'}, status=status.HTTP_401_UNAUTHORIZED)

#         # Intentamos autenticar al usuario
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # Si el usuario es autenticado correctamente, creamos el token
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'Detail': 'Logged Successfully...'
#             })
        
#         # Si la contraseña es incorrecta, devolvemos un error
#         return Response({'Detail': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class CustomLogoutView(AllauthLogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CustomLoginView(AllauthLoginView):
    def form_valid(self, form):
        return redirect('accounts/google/login/continue')  # Cambia 'google_login' según la URL de inicio de sesión de Google en tus URLs




class OwnLoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return Response({'Detail': 'Invalid Username'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                'Detail': 'Logged Successfully...'
            })
        
        return Response({'Detail': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)
