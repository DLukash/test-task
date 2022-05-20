#Celery & tasks
from celery import shared_task

#Імпорти із внутрішнього app
from test_task_app.services import get_collection

#Бібліотека для AWS S3
import boto3
from botocore import UNSIGNED
from botocore.config import Config

#Інше
import json


@shared_task()
def sync_data_task(from_id: int, to_id:int):
    """
    Таск на синхронізацію даних
    """
    
    #Генеруємо з'єднання з базою даних та з'єднання з колекцією
    col = get_collection()

    #Отримуємо існуючі об'єкти
    exist_images = [x['img'] for x in list(col.find({}, {'img':1, '_id':0}))]

    #Підключаємося до бакету
    s3=boto3.resource('s3', config=Config(signature_version=UNSIGNED), region_name='us-east-1')

    for i in range(from_id , to_id):

        #Вантажимо лише не існуючі дані
        if i in exist_images: continue
        #Читаємо файл з бакету
        response = s3.Object('aft-vbi-pds', f"metadata/{i}.json").get()
        #Робимо словник
        bin_data = json.load(response['Body'])
        
        #Якщо коробка не пуста - зберізаємо дані про предмети
        if 'BIN_FCSKU_DATA' in bin_data:    
            for key, value in bin_data['BIN_FCSKU_DATA'].items():
                
                #Вставляємо дані в колекцію
                col.insert_one({
                            'item_key':key,
                            'item_data':value,
                            'bin_number':i
                        })


    return True