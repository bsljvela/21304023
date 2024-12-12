from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny


from users.models import User
from users.serializers import UserSerializer, RegisterUserSerializer


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


    def create(self, request, *args, **kwargs):
        # Crear una copia mutable de request.data
        mutable_data = request.data.copy()


        # Modificar la copia mutable
        mutable_data['password'] = make_password(mutable_data['password'])


        # Pasar la copia mutable al serializer
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


        # request.data['password'] = make_password(request.data['password'])
        # return super().create(request, *args, **kwargs)


    def partial_update(self, request, *args, **kwargs):
        # Crear una copia mutable de request.data
        mutable_data = request.data.copy()


        # Modificar la copia mutable
        if "password" in mutable_data:
            mutable_data["password"] = make_password(mutable_data["password"])
        else:
            mutable_data["password"] = request.user.password


        # Pasar la copia mutable al serializer
        serializer = self.get_serializer(
            instance=self.get_object(), data=mutable_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


        return Response(serializer.data)


        # if "password" in request.data:
        #     request.data["password"] = make_password(request.data["password"])
        # else:
        #     request.data["password"] = request.user.password
        # return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterUserView(ModelViewSet):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()


    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.user)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteNonAdminUsersView(APIView):
    permission_classes = [IsAdminUser]  # Solo permite acceso a administradores


    def delete(self, request):
        # Filtra usuarios que no sean administradores (is_staff=False)
        non_admin_users = User.objects.filter(is_staff=False)


        # Cuenta los usuarios antes de eliminarlos
        count = non_admin_users.count()


        # Elimina los usuarios
        non_admin_users.delete()


        return Response({"message": f"Se eliminaron {count} usuarios no administradores."}, status=200)
