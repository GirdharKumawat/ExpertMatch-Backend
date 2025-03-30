from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import userRegister, userLogin,profile,addUser,userinfo,allCandidates,allExperts ,scoreMatch

urlpatterns = [
    path('register/', userRegister, name='user-register'),
    path('login/', userLogin, name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('candidates/', allCandidates, name='candidates'),
    path('experts/', allExperts, name='experts'),
    path('profile/<int:id>', profile, name='user-profile'),
    path('adduser/', addUser, name='add-user'),
    path('userinfo/<int:id>', userinfo, name='userinfo'),
    path('score/<int:id>',scoreMatch, name='scoreMatch')
]
