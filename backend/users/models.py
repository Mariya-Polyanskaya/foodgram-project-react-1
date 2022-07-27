from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.settings import (
    EMAIL_LENGTH, USERNAME_LENGTH,
    FIRST_NAME_LENGHT, LAST_NAME_LENGHT)


class User(AbstractUser):

    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'

    ACCESS_ROLES = (
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin')
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=EMAIL_LENGTH,
        blank=False,
        unique=True,
        help_text='Укажите электронная почту'
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
        help_text='Укажите свое имя пользователя',
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=FIRST_NAME_LENGHT,
        blank=True,
        help_text='Укажите своё имя',
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=LAST_NAME_LENGHT,
        blank=True,
        help_text='Укажите свою фамилию',
    )

    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text='Введите пароль',
    )

    role = models.CharField(
        max_length=max(
            len(iteration[0]) for iteration in ACCESS_ROLES),
        choices=ACCESS_ROLES,
        default=USER_ROLE,
        blank=False,
        verbose_name='роль'
    )

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE

    @property
    def is_admin(self):
        return (self.role == self.ADMIN_ROLE
                or self.is_staff)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user_code'
            ),
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='uniq_follow',
            ),
        )

    def __str__(self):
        return f'{self.user} - {self.author}'
