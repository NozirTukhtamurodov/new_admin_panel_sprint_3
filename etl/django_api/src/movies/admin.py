from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 1


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmWorkInline)
    # Отображение полей в списке
    list_display = ('id', 'title', 'type', 'creation_date', 'rating', 'updated_at')

    # Фильтрация в списке
    list_filter = ('type',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id')
