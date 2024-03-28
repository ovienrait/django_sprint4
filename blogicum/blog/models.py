from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count

from core.models import CoreModel
from .constants import TITLE_FIELD_LENGTH

User = get_user_model()


class PostManager(models.Manager):
    def get_posts(self):
        return self.select_related(
            'category', 'location', 'author'
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')

    def get_published(self):
        return self.get_posts().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )


class Post(CoreModel):
    """Модель, описывающая поля публикаций"""

    objects = PostManager()

    title = models.CharField(
        max_length=TITLE_FIELD_LENGTH,
        verbose_name='Заголовок'
    )

    text = models.TextField(
        verbose_name='Текст'
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем '
                  '— можно делать отложенные публикации.'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )

    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение'
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='posts_images',
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Category(CoreModel):
    """Модель, описывающая поля категорий"""

    title = models.CharField(
        max_length=TITLE_FIELD_LENGTH,
        verbose_name='Заголовок'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(CoreModel):
    """Модель, описывающая поля мест"""

    name = models.CharField(
        max_length=TITLE_FIELD_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Модель, описывающая поля комментариев"""

    text = models.TextField(
        max_length=300,
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.text
