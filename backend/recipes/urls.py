from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipesViewSet, TagViewSet

app_name = 'recipes'

recipes_router_v1 = DefaultRouter()
recipes_router_v1.register('tags', TagViewSet, basename='tags')
recipes_router_v1.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
recipes_router_v1.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(recipes_router_v1.urls)),
]
