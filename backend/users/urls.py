from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from users import views


router = routers.DefaultRouter()
router.register(r'users', views.UserApiViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', views.UserView.as_view(), name='user-view'),
    path('auth/register/',
        views.RegisterUserView.as_view({'post': 'create'}), name='register'),
    path('delete-non-admins/', views.DeleteNonAdminUsersView.as_view(),
        name='delete_non_admin_users'),
    # Aqui pueden utilizar el nombre de auth/token/  o  auth/login/
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
