# at03/practice_thecatapi/main.py
import requests

class CatAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.thecatapi.com/v1'
        self.headers = {
            'x-api-key': api_key
        }
    
    def get_random_cat(self):
        """
        Получает случайное изображение кота
        
        Returns:
            dict: Информация о коте или None при ошибке
        """
        url = f'{self.base_url}/images/search'
        
        try:
            response = requests.get(
                url, 
                headers=self.headers,
                params={'limit': 1}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0]
                return None
            else:
                print(f"Ошибка API: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")
            return None
    
    def get_cat_breeds(self, limit=10):
        url = f'{self.base_url}/breeds'
        
        try:
            response = requests.get(
                url, 
                headers=self.headers,
                params={'limit': limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка API: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")
            return None
    
    def search_cats_by_breed(self, breed_name):
        url = f'{self.base_url}/images/search'
        
        try:
            response = requests.get(
                url, 
                headers=self.headers,
                params={'breed_ids': breed_name, 'limit': 5}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка API: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")
            return None