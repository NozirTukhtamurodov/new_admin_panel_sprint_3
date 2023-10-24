from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import Http404


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return  Filmwork.objects.prefetch_related('genres', 'persons').values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='actor') ,distinct=True,),
            directors=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='director') ,distinct=True,),
            writers=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='writer') ,distinct=True,),
        ).order_by('title')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {'count': paginator.count, 
                'total_pages': paginator.num_pages,
                'prev': page.previous_page_number() if page.has_previous() else None,
                'next': page.next_page_number() if page.has_next() else None,
                'results': list(queryset),
                } 

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_object(self, queryset=None):
        # Customize this method to fetch the specific Filmwork object you want to display
        # For example, you can retrieve the object based on the URL parameter 'pk'
        pk = self.kwargs.get('pk')
        try:
            return self.get_queryset().get(pk=pk)
        except Filmwork.DoesNotExist:
            raise Http404("Filmwork does not exist")

    def get_context_data(self, **kwargs):
        queryset = self.get_object()
        return queryset