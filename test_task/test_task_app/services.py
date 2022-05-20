
import os

#Бібліотека для mongodb
from pymongo import MongoClient

#Бібліотека для гістограми
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
import pandas as pd



def get_collection():
    """
    Повертаємо коннект з базою даних та з колекцією в ній
    """

    CONNECTION_STRING = os.getenv('CONNECTION_STRING_MONGO')
    client = MongoClient(CONNECTION_STRING)
    return client['testDB']['goods']


def get_items_query(volume_min:float = None, volume_max:float = None, weight_min:float= None, weight_max:float= None):

    col = get_collection()

    filter= {'$and':[]}
    
    #Додаємо умови запиту, у разі наявності параметрів
    if  volume_min:
        filter['$and'].append(
            {
                    '$expr': {
                        '$gte': [
                            {
                                '$multiply': [
                                    '$item_data.height.value', '$item_data.width.value', '$item_data.length.value'
                                ]
                            }, volume_min
                        ]
                    }
                }
        )
    
    if  volume_max:
        filter['$and'].append(
            {
                    '$expr': {
                        '$lte': [
                            {
                                '$multiply': [
                                    '$item_data.height.value', '$item_data.width.value', '$item_data.length.value'
                                ]
                            }, volume_max
                        ]
                    }
                }
        )

    if  weight_min:
        filter['$and'].append(
            {
            'item_data.weight.value': {
                '$gte': weight_min
            }
        }
        )
    
    if  weight_max:
        filter['$and'].append(
            {
            'item_data.weight.value': {
                '$lte': weight_max
            }
        }
        )
    
    #Повертаємо результат списком без ід
    return list(col.find(filter = filter if filter['$and'] else None, projection={'_id': False}))



def creare_html_histogram(data = None):

    """
    Функція побудови гісторгами з вхідних даних
    """


    col = get_collection()

    #Дані для гістограмі по ширині
    df_width = pd.DataFrame(col.aggregate([
        {
            '$group': {
                '_id': '$item_data.width.value', 
                'quantity': {
                    '$sum': 1
                }
            }
        }
    ]))

    #Дані для гістограмі по вазі
    df_weight = pd.DataFrame(col.aggregate([
        {
            '$group': {
                '_id': '$item_data.weight.value', 
                'quantity': {
                    '$sum': 1
                }
            }
        }
    ]))

    df_number_in_box = pd.DataFrame(col.aggregate(
        [
    {
        '$group': {
            '_id': '$item_data.asin', 
            'quantity': {
                '$sum': 1
            }
        }
    }, {
        '$group': {
            '_id': '$quantity', 
            'quantity': {
                '$sum': 1
            }
        }
    }
        ]
    ))

    
    #Генеримо HTML для відображення статистики
    fig = make_subplots(rows=2, cols=2,specs=[[{}, {"rowspan": 2}],
           [{}, None]] ,subplot_titles=("Розподіл ширини речей", "Розподіл ваги речей", "Кількість предметів у коробці"))

    histo_width = go.Histogram(histfunc="sum",x=df_width['_id'], xbins={"size": 0.1}, y=df_width['quantity'], name='Ширина (in)')
    histo_weight = go.Histogram(histfunc="sum",x=df_weight['_id'], xbins={"size": 0.1}, y=df_weight['quantity'], name='Вага (pounds)')
    histo_number_in_box = go.Histogram(histfunc="sum",x=df_number_in_box['_id'], xbins={"size": 0.8}, y=df_number_in_box['quantity'], name='Кількість в коробці (шт)')

    fig = fig.add_trace(histo_width, row=1, col= 1)
    fig = fig.add_trace(histo_weight, row=2, col= 1)
    fig = fig.add_trace(histo_number_in_box, row=1, col= 2)
    

    return(fig.to_html(full_html=True))
    