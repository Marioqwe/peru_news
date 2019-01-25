from django.urls import reverse
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from app.api_key.models import APIKey


class TestGetArticles(APITestCase):

    SAMPLE_DATA = [
        {'source': 'apple', 'date': '2018-10-10', 'section': 'iphone', 'data': ['foo1', 'foo2']},
        {'source': 'apple', 'date': '2018-10-10', 'section': 'ipad', 'data': ['bar1', 'bar2', 'bar3']},
        {'source': 'amazon', 'date': '2018-10-10', 'section': 'alexa', 'data': ['baz1', 'baz2', 'baz3', 'baz4', 'baz5',
                                                                                'baz6', 'baz7', 'baz8', 'baz9', 'baz10',
                                                                                'baz11', 'baz12', 'baz13', 'baz14', 'baz15',
                                                                                'baz16', 'baz17', 'baz18', 'baz19', 'baz20',
                                                                                'baz21', 'baz22', 'baz23', 'baz24', 'baz25']}
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_key = APIKey.objects.create(name='TestApiKey',
                                            key='key-1').key
        cls.api_key_can_post = APIKey.objects.create(name='TestApiKeyCanPost',
                                                     key='key-2', can_post=True).key
        cls.url = reverse('articles')

    def setUp(self):
        self.client.credentials(HTTP_API_KEY=self.api_key)

    def tearDown(self):
        cache.clear()

    def post_dummy_data(self):
        self.client.credentials(HTTP_API_KEY=self.api_key_can_post)
        for data in self.SAMPLE_DATA:
            self.client.post(self.url, data)

        self.client.credentials(HTTP_API_KEY=self.api_key)

    def test_source_is_none(self):
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_page_cannot_be_casted_to_int(self):
        params = {'source': 'a', 'page': 'invalid'}
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_page_size_cannot_be_casted_to_int(self):
        params = {'source': 'a', 'pageSize': 'invalid'}
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_with_section(self):
        self.post_dummy_data()
        params = {
            'source': 'apple',
            'section': 'iphone',
            'date': '2018-10-10',
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['totalResults'], 2)
        self.assertListEqual(response.data['articles'], ['foo1', 'foo2'])

    def test_get_without_section(self):
        self.post_dummy_data()
        params = {
            'source': 'apple',
            'date': '2018-10-10',
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['totalResults'], 5)
        self.assertListEqual(response.data['articles'], ['foo1', 'foo2', 'bar1', 'bar2', 'bar3'])

    def test_get_with_invalid_source(self):
        self.post_dummy_data()
        params = {
            'source': 'invalid',
            'date': '2018-10-10',
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['totalResults'], 0)
        self.assertListEqual(response.data['articles'], [])

    def test_get_with_invalid_date(self):
        self.post_dummy_data()
        params = {
            'source': 'apple',
            'date': 'invalid',
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['totalResults'], 0)
        self.assertListEqual(response.data['articles'], [])

    def test_results_are_trimmed(self):
        self.post_dummy_data()
        params = {
            'source': 'amazon',
            'date': '2018-10-10',
            'section': 'alexa',
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['totalResults'], 25)
        self.assertListEqual(response.data['articles'], ['baz1', 'baz2', 'baz3', 'baz4', 'baz5',
                                                         'baz6', 'baz7', 'baz8', 'baz9', 'baz10',
                                                         'baz11', 'baz12', 'baz13', 'baz14', 'baz15',
                                                         'baz16', 'baz17', 'baz18', 'baz19', 'baz20'])

    def test_get_with_page_size_and_page_param(self):
        self.post_dummy_data()
        params = {
            'source': 'amazon',
            'date': '2018-10-10',
            'section': 'alexa',
            'pageSize': '5',
            'page': '3',
        }
        response = self.client.get(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['totalResults'], 25)
        self.assertListEqual(response.data['articles'], ['baz11', 'baz12', 'baz13', 'baz14', 'baz15'])


class TestPostArticles(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_key = APIKey.objects.create(name='TestApiKeyCanPost', key='api-key', can_post=True).key
        cls.url = reverse('articles')

    def setUp(self):
        self.client.credentials(HTTP_API_KEY=self.api_key)

    def tearDown(self):
        cache.clear()

    def test_no_source_in_data(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_date_in_data(self):
        data = {'source': 'a'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_section_in_data(self):
        data = {'source': 'a', 'date': '2018-10-10'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_data_in_data(self):
        data = {'source': 'a', 'date': '2018-10-10', 'section': 'politica'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_post(self):
        # note: cache_key would be 'a:2018-10-10:b'
        data = {
            'source': 'a',
            'date': '2018-10-10',
            'section': 'b',
            'data': ['foo'],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.data, {'status': 'ok', 'message': 'Created.'})
