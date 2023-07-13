import requests
import logging

logging.basicConfig(level=logging.INFO)
class Shodan():
    def __init__(self, api_key:str) -> None:
        self.api_key = api_key

    def search(self, query:str):
        try:
            logging.info('Start search on shodan')
            params = {
                'key':self.api_key,
                'query':query
            }
            req = requests.get(
                'https://api.shodan.io/shodan/host/search',
                params=params)
            
            if req.status_code == 200:
                logging.info('Search success')
                req = req.json()
                return req
            else:
                logging.info('Search Failed')
                logging.debug(req.json())
                return None
        except Exception as ex:
            logging.info(f'Error to fetch shodan: {str(ex)}')
            return None
