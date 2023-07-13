import logging
import requests 

# Schemas
from django.http import JsonResponse, FileResponse, HttpResponse

# Models
from ..models import Devices

# Services
from .shodanServices import Shodan

# Extras
from datetime import datetime
from uuid import UUID
import re
from PIL import Image
from io import BytesIO


logging.basicConfig(level=logging.INFO)

class DBSessionMixin:
    pass
class AppService(DBSessionMixin):
    pass
class AppDataAccess(DBSessionMixin):
    pass
class DevicesDataAccess(AppDataAccess):
    def bulk_insert_devices(self, insert_list:list):
        devices = Devices.objects.bulk_create(
            insert_list,
            ignore_conflicts=True,
        )

        return devices
    
    def get_items(self):
        devices = Devices.objects.filter(is_active = True)
        return devices if devices else None
    
    def get_item(self, item_uuid:UUID):
        item = Devices.objects.filter(uuid__iexact = item_uuid).first()
        return item if item else None
    
class DevicesServices(AppService):
    def create_inserts(self, object):
        patron = r'(?P<clave>.*?): (?P<valor>.*?)\r\n'
        extra_data = re.findall(patron, object['data'], re.DOTALL)
        extra_data_dict = {}

        for clave, valor in extra_data:
            extra_data_dict[clave] = valor

        object = Devices(
            ip=object.get('ip_str'), 
            port=object.get('port'), 
            full_address=f"{object.get('ip_str')}:{object.get('port')}",
            created_at=datetime.now().timestamp(),
            latitude= object.get('location').get('latitude'),
            longitude= object.get('location').get('longitude'),
            country=object.get('location').get('country_name'),
            city=object.get('location').get('city'),
            extra_data=extra_data_dict
            )
        return object
    
    def fetch_devices(self, api_key:str, query:str):
        try:
            logging.info('Start fetch devices')
            results = Shodan(api_key).search(query)

            if results:
                insert_list = list(map(self.create_inserts, results.get('matches')))

                inserts = DevicesDataAccess().bulk_insert_devices(insert_list)

            return JsonResponse(inserts)

        except Exception as ex:
            logging.error(f'Error to fetch Shodan - str{ex}')
            return JsonResponse({'status_code':400, 'message':f'Error to fetch Shodan: {str(ex)}'})
        
    def get_devices(self):
        try:
            devices = DevicesDataAccess().get_items()
            
            list_location = []

            if devices:
                list_location = [{
                    'info':{
                        'uuid': x.uuid,
                        'full_address': x.full_address,
                        'country': x.country,
                        'city': x.city,
                        'status':x.is_active,
                        'last_snapt_at': datetime.fromtimestamp(x.last_screen_shot_at).strftime('%d-%m-%Y %H:%Mhs') if x.last_screen_shot_at else ''
                    },
                    'location':{
                        'lat': x.latitude, 
                        'lng': x.longitude} 
                    } for x in devices]
                
            return JsonResponse(
                {'status_code':200,
                'message':'Get Success',
                'data':list_location if list_location else None
                })
        
        except Exception as ex:
            logging.error(f'Error to get devices - str{ex}')
            return JsonResponse({'status_code':400, 'message':f'Error to get devices: {str(ex)}'})
    
    def get_snapshop(self, device_uuid:UUID):
        try:
            device = DevicesDataAccess().get_item(device_uuid)

            if not device.is_active or not device.is_online:
                return JsonResponse({
                'status_code':200,
                'message':'Camera not working'
            })

            url = f'http://{device.full_address}/onvif-http/snapshot?auth=YWRtaW46MTEK'
            params = {
                'auth':'YWRtaW46MTEK'
            }

            req = requests.get(url, params=params)

            if not req.status_code == 200:
                raise Exception('Camera Not Working')
            
            image = Image.open(BytesIO(req.content))

            output = BytesIO()

            image.save(output, format='JPEG')
            image_data = output.getvalue()

            device.last_screen_shot_at = datetime.now().timestamp()
            device.save()

            return HttpResponse(image_data, content_type='image/jpeg')
       
        except Exception as ex:
            logging.info(f'Error to get snapshop - {str(ex)}')

            device.is_active = False
            device.is_online = False
            device.save()

            return JsonResponse({
                'status_code':200,
                'message':'Camera not working'
            })
        

      