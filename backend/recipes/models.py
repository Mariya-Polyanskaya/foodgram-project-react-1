from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """Модель для создания тегов."""
    ORANGE = '#FB581C'
    GREEN = '#5EFF9E'
    PURPLE = '#C922CC'

    COLOR_CHOICES = [
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Пурпурный'),
    ]

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега')

    color = models.CharField(
        max_length=7, unique=True,
        choices=COLOR_CHOICES,
        verbose_name='Цвет в HEX')

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для одного ингридиента."""
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        blank=False,
        help_text='Введите название ингредиента',
    )

    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50,
        blank=False,
        help_text='Выберите единицу измерения',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='pair_unique'),
        )
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для создания рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Автор рецепта',
    )

    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
        help_text='Укажите название рецепта',
    )

    text = models.TextField(
        verbose_name='Описание'
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
        help_text='Выберите теги',
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты рецепта',
        related_name='recipes',
        help_text='Выберите ингредиенты',
    )

    image = models.ImageField(
        verbose_name='Фото готового блюда',
        upload_to='recipes/',
        help_text='Загрузите изображение с фотографией готового блюда',
    )

    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1,
            message='Укажите время больше нуля!',
        ),),
        verbose_name='Время приготовления',
        help_text='Задайте время приготовления блюда',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Модель связанная для ингридиентов рецепта."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Минимальное количество ингридиентов 1'),),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
        ]


class Favorite(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe for user')
        ]


class ShoppingCart(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name='shoppingcart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique shoppingcart user')
        ]
