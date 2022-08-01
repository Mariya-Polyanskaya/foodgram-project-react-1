from django.urls import include, path

from rest_framework.routers import DefaultRouter

from djoser.views import TokenCreateView, TokenDestroyView

from .views import (
    CustomUserViewSet,
    SubscriptionListView,
    subscribe_unsubscribe_author
)

app_name = 'users'

api_users_router_v1 = DefaultRouter()
api_users_router_v1.register(r'users/subscriptions',
                             SubscriptionListView,
                             basename='subscriptions')
api_users_router_v1.register('users', CustomUserViewSet)

urlpatterns = [
    path('users/<int:pk>/subscribe/',
         subscribe_unsubscribe_author,
         name='subscribe_unsubscribe_author'
         ),
    path('', include(api_users_router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]
