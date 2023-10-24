import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Type(models.TextChoices):
    movie = 'movie', _('Movie')
    tv_show = 'tv_show', _('TV show')


class RoleType(models.TextChoices):
    actor = 'actor', _('Actor')
    writer = 'writer', _('Writer')
    director = 'director', _('Director')


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created datetime'),
        null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('modified datetime'),
        null=True, blank=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name=_('id'))

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE, verbose_name=_('Filmwork'))
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE, verbose_name=_('Genre'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created datetime'),
        null=True, blank=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = (('film_work', 'genre',),)



class Person(UUIDMixin, TimeStampedMixin):
    id = models.UUIDField(primary_key=True)
    full_name = models.TextField()

    class Meta:
        managed = True
        db_table = "content\".\"person"
        verbose_name = _("Person")
        verbose_name_plural = _("People")
    
    def __str__(self) -> str:
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    genres = models.ManyToManyField("movies.Genre", through="movies.GenreFilmwork")
    persons = models.ManyToManyField("movies.Person", through="movies.PersonFilmwork")
    description = models.TextField(verbose_name=_('description'), null=True)
    creation_date = models.DateField(
        null=True, verbose_name=_('creation date'))
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100),],
                                null=True)
    type = models.TextField(choices=Type.choices, verbose_name=_('Type'))
    file_path = models.FileField(
        _('file'), null=True, upload_to='movies/')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")
        managed = True


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, blank=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, blank=True)
    role = models.TextField(blank=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "content\".\"person_film_work"
        unique_together = (('film_work', 'person', 'role'),)
