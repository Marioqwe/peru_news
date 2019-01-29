import datetime
import logging
import pytz

from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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


@api_view(['GET', 'POST'])
def articles(request):
    if request.method == 'GET':
        source = request.GET.get('source', None)
        if source is None:
            return bad_request('No source provided.')

        section = request.GET.get('section', None)

        date = request.GET.get('date', None)
        if date is None:
            # Use current peruvian date by default.
            date = datetime.datetime.now(pytz.timezone('America/Lima'))
            date = date.strftime('%Y-%m-%d')

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

        if section is None:
            _LOGGER.info('No section provided.')
            pattern = '%s:%s:*' % (source, date)
            keys = cache.iter_keys(pattern)
        else:
            _LOGGER.info('Section \'%s\' provided.' % section)
            keys = ['%s:%s:%s' % (source, date, section)]

        data = []
        for cache_key in keys:
            _LOGGER.info('Retrieving \'%s\' from cache.' % cache_key)
            saved_data = cache.get(cache_key)
            if saved_data is not None:
                data.extend(saved_data)
            else:
                _LOGGER.info('\'%s\' does not exist in cache.' % cache_key)

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

        date = request.data.get('date', None)
        if date is None:
            return bad_request('No date provided.')

        section = request.data.get('section', None)
        if section is None:
            return bad_request('No section provided.')

        data = request.data.get('data', None)
        if not data:
            return bad_request('No data provided.')

        cache_key = '%s:%s:%s' % (source, date, section)
        _LOGGER.info('Saving cache_key \'%s\'' % cache_key)
        cache.set(cache_key, data, timeout=None)

        return Response({
            'status': 'ok',
            'message': 'Created.',
        }, status=status.HTTP_201_CREATED)
