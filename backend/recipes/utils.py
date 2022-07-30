from django.db.models import Sum

from recipes.models import IngredientRecipe


def get_cart(self, request):
    return IngredientRecipe.objects.filter(
        recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
                count=Sum('amount'))
