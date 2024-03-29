from csv import reader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Добавление ингредиентов из CSV файла.
    Сначала выполнить миграции, затем запустить командой:
    - локально `python manage.py load_ingredients`
    - в контейнере
    `sudo docker-compose exec backend python manage.py load_ingredients`
    """
    help = 'Load data ingredients to DB from csv-file.'

    def handle(self, *args, **kwargs):
        with open(
                'recipes/data/ingredients.csv', 'r',
                encoding='UTF-8'
        ) as ingredients:
            for row in reader(ingredients):
                if len(row) == 2:
                    Ingredient.objects.get_or_create(
                        name=row[0], measurement_unit=row[1],
                    )
