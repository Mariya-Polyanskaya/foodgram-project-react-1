from django.db.models import Sum

from recipes.models import IngredientRecipe


def get_ingredients(self, request):
    return IngredientRecipe.objects.filter(
        recipe__shoppingcart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(total=Sum('amount'))
