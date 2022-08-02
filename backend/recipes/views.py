from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from foodgram.pagination import LimitPageNumberPagination
from api.filters import IngredientFilter, RecipeFilter
from api.serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, ReduceRecipeSerializer
)
from api.permissions import IsAdminOrReadOnly, IsAuthorOrAdmin
from recipes.utils import get_ingredients
from recipes.models import (
    Tag, Ingredient, Recipe, Favorite, ShoppingCart)


class TagIngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Общий родительский класс для TagViewSet и IngredientViewSet"""
    ...


class TagViewSet(TagIngredientViewSet):
    """ViewSet для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(TagIngredientViewSet):
    """ViewSet для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdmin,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Favorite, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['get', 'post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(ShoppingCart, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = get_ingredients(self, request)
        shopping_list = 'Список покупок:\n'
        for number, ingredient in enumerate(ingredients, start=1):

            shopping_list += (
                f'{number} '
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["total"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n')

        shoppingcart_list = 'shoppingcart_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (f'attachment;'
                                           f'filename={shoppingcart_list}')
        return response

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ReduceRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)
