import pytest
import requests
from main_at03 import CatAPI

class TestCatAPI:
    def setup_method(self):
        self.api_key = 'live_XS1HTKpTlT0jq83DFhdzOrDSVmj6A5Hf4tvhPgleaP0Xj6vvkgZZZkXxBVpoLH10'
        self.cat_api = CatAPI(self.api_key)
    
    def test_get_random_cat_success(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')

        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'id': 'abc123',
            'url': 'https://cdn2.thecatapi.com/images/abc123.jpg',
            'width': 500,
            'height': 400,
            'breeds': [{'name': 'Siamese'}]
        }]
        mock_get.return_value = mock_response

        result = self.cat_api.get_random_cat()

        assert result is not None
        assert result['id'] == 'abc123'
        assert 'thecatapi.com' in result['url']
        assert result['breeds'][0]['name'] == 'Siamese'

        mock_get.assert_called_once_with(
            'https://api.thecatapi.com/v1/images/search',
            headers={'x-api-key': self.api_key},
            params={'limit': 1}
        )
    
    def test_get_random_cat_empty_response(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')

        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []  # Пустой список
        mock_get.return_value = mock_response

        result = self.cat_api.get_random_cat()

        assert result is None
    
    def test_get_random_cat_api_error(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')

        mock_response = mocker.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.cat_api.get_random_cat()

        assert result is None
    
    def test_get_random_cat_network_error(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        result = self.cat_api.get_random_cat()

        assert result is None
    
    def test_get_cat_breeds_success(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')

        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 'siam', 'name': 'Siamese', 'origin': 'Thailand'},
            {'id': 'pers', 'name': 'Persian', 'origin': 'Iran'},
            {'id': 'mcoo', 'name': 'Maine Coon', 'origin': 'United States'}
        ]
        mock_get.return_value = mock_response

        result = self.cat_api.get_cat_breeds(limit=3)

        assert len(result) == 3
        assert result[0]['name'] == 'Siamese'
        assert result[1]['id'] == 'pers'

        mock_get.assert_called_once_with(
            'https://api.thecatapi.com/v1/breeds',
            headers={'x-api-key': self.api_key},
            params={'limit': 3}
        )
    
    def test_get_cat_breeds_error(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')

        mock_response = mocker.Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.cat_api.get_cat_breeds()

        assert result is None

        mock_get.assert_called_once_with(
            'https://api.thecatapi.com/v1/breeds',
            headers={'x-api-key': self.api_key},
            params={'limit': 10}  # По умолчанию limit=10
        )
    
    def test_get_cat_breeds_network_error(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')
        mock_get.side_effect = requests.exceptions.ConnectionError("DNS resolution failed")

        result = self.cat_api.get_cat_breeds(limit=5)

        assert result is None

        mock_get.assert_called_once_with(
            'https://api.thecatapi.com/v1/breeds',
            headers={'x-api-key': self.api_key},
            params={'limit': 5}
        )
    
    def test_search_cats_by_breed(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')

        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 'img1', 'url': 'https://cdn2.thecatapi.com/images/img1.jpg', 'breeds': [{'name': 'Siamese'}]},
            {'id': 'img2', 'url': 'https://cdn2.thecatapi.com/images/img2.jpg', 'breeds': [{'name': 'Siamese'}]}
        ]
        mock_get.return_value = mock_response

        result = self.cat_api.search_cats_by_breed('siam')

        assert len(result) == 2
        assert all('Siamese' in cat['breeds'][0]['name'] for cat in result)

        mock_get.assert_called_once_with(
            'https://api.thecatapi.com/v1/images/search',
            headers={'x-api-key': self.api_key},
            params={'breed_ids': 'siam', 'limit': 5}
        )
    
    def test_search_cats_by_breed_error(self, mocker):
        mock_get = mocker.patch('main_at03.requests.get')

        mock_response = mocker.Mock()
        mock_response.status_code = 404                         # Порода не найдена
        mock_get.return_value = mock_response

        result = self.cat_api.search_cats_by_breed('unknown_breed')

        assert result is None

        mock_get.assert_called_once_with(
            'https://api.thecatapi.com/v1/images/search',
            headers={'x-api-key': self.api_key},
            params={'breed_ids': 'unknown_breed', 'limit': 5}
        )

def test_cat_api_initialization():
    api_key = 'test_key_123'
    cat_api = CatAPI(api_key)
    
    assert cat_api.api_key == api_key
    assert cat_api.base_url == 'https://api.thecatapi.com/v1'
    assert cat_api.headers == {'x-api-key': api_key}