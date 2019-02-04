import datetime
import logging
import pytz

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer
from ..api_key.permissions import HasAPIAccess


_LOGGER = logging.getLogger(__name__)

API_SETTINGS = getattr(settings, 'API_SETTINGS', None)
if API_SETTINGS is None:
    raise RuntimeError('Define API_SETTINGS in django settings.')

DEFAULT_PAGE_SIZE = API_SETTINGS.get('DEFAULT_PAGE_SIZE', None)
if DEFAULT_PAGE_SIZE is None:
    raise RuntimeError('Define API_SETTINGS.DEFAULT_PAGE_SIZE in django settings')

MAX_PAGE_SIZE = API_SETTINGS.get('MAX_PAGE_SIZE', None)
if MAX_PAGE_SIZE is None:
    raise RuntimeError('Define API_SETTINGS.MAX_PAGE_SIZE in django settings')


def bad_request(message):
    return Response({
        'status': 'error',
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((HasAPIAccess, ))
def sources(request):
    return Response({
        'status': 'ok',
        'sources': {
            'id': 'rpp',
            'name': 'RPP Noticias',
            'url': 'https://www.rpp.pe',
        },
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((HasAPIAccess, ))
def sections(request):
    return Response({
        'status': 'ok',
        'sections': [
            'politica',
            'mundo',
            'economia',
            'actualidad',
            'deportes',
            'entretenimiento',
            'tecnologia',
            'ciencia',
        ],
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((HasAPIAccess, ))
def articles(request):
    if request.method == 'GET':
        source = request.GET.get('source', None)
        if source is None:
            return bad_request('No source provided.')
        source = source.split(',')

        section = request.GET.get('section', None)

        date = request.GET.get('date', None)
        if date is None:
            # Use current peruvian date by default.
            date = datetime.datetime.now(pytz.timezone('America/Lima'))
            date = date.strftime('%Y-%m-%d')
        date = date.split('-')

        # Use to page through results if total results
        # is greater than page_size.
        page_num = request.GET.get('page', 1)
        try:
            page_num = int(page_num)
        except (TypeError, ValueError):
            return bad_request('Invalid page number.')

        # The number of results per page.
        page_size = request.GET.get('pageSize', DEFAULT_PAGE_SIZE)
        try:
            page_size = int(page_size)
        except (TypeError, ValueError):
            return bad_request('Invalid page size.')
        if page_size > MAX_PAGE_SIZE:
            page_size = MAX_PAGE_SIZE

        if section is None or section == 'all':
            articles = Article.objects.filter(sid__in=source,
                                              published_at__year=date[0],
                                              published_at__month=date[1],
                                              published_at__day=date[2])
        else:
            section = section.split(',')
            articles = Article.objects.filter(sid__in=source, section__in=section,
                                              published_at__year=date[0],
                                              published_at__month=date[1],
                                              published_at__day=date[2])

        data = []
        for a in articles:
            serializer = ArticleSerializer(a)
            data.append(serializer.data)

        bottom = (page_num - 1) * page_size
        top = bottom + page_size

        return Response({
            'status': 'ok',
            'totalResults': len(data),
            'articles': data[bottom:top],
        })
    else:
        source = request.data.get('source', None)
        if source is None:
            return bad_request('No source provided.')

        # todo: allow data to not only be a list.
        data = request.data.get('data', None)
        if data is None:
            return bad_request('No data provided.')

        for a in data:
            adata = {
                'sid': source.get('id'),
                'sname': source.get('name'),
                'aid': a.get('aid'),
                'headline': a.get('headline'),
                'section': a.get('section'),
                'url': a.get('url'),
                'published_at': a.get('publishedAt'),
            }

            try:
                instance = Article.objects.get(sid=adata['sid'], aid=adata['aid'])
            except ObjectDoesNotExist:
                instance = None

            if instance is None:
                serializer = ArticleSerializer(data=adata)
            else:
                serializer = ArticleSerializer(instance, data=adata)

            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(status=status.HTTP_201_CREATED)
