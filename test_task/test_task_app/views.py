
#Django & rest freimwork
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_http_methods

#Імпорти із внутрішнього app
from test_task_app.serializers import CreateRequestSerrializer, GetRequestInfoSerrializer, GetGoodsInfoSerrializer
from test_task_app.services import get_items_query, creare_html_histogram

#Celery & tasks
from test_task_app.tasks import sync_data_task
from celery.result import AsyncResult


# Словник для приведення респода до умов ТЗ
task_status = {
    'PENDING':'PENDING',
    'STARTED':'IN_PROGRESS',
    'RETRY':'IN_PROGRESS',
    'FAILURE':'FAILED',
    'SUCCESS':'SUCCEED'
}



class CreateRequest(APIView):
    '''
    Метод для запуска таска по синхронізації даних із бакетом
    '''

    def post(self, request):
        serializer = CreateRequestSerrializer(data=request.data)
        
        if serializer.is_valid():

            #Запускаємо такс в Celery
            res = sync_data_task.delay(serializer['from'].value, serializer['to'].value)
            
            #Повертаємо ІД таску
            return Response(status=status.HTTP_201_CREATED, data={'request_id': res.id})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    pass


class GetRequestInfo (APIView):
    '''
    Вью. Видаємо інформацію (статус) по конкретному запиту
    '''

    def post(self, request):
        serializer = GetRequestInfoSerrializer(data=request.data)
    
        if serializer.is_valid():  
                res = AsyncResult(serializer['request_id'].value)

                #Створюємо словник-відповідь
                responce_dict = {'status': task_status[res.status]}
                
                # Якщо була помилка - то передаємо повідомлення посилки
                if res.status == 'FAILURE':
                    responce_dict['msg'] = str(res.result)

                return Response(status=status.HTTP_200_OK, data=responce_dict)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetItems (APIView):
    """
    Вью. Видаємо результати запиту
    """

    def post(self, request):
        serializer = GetGoodsInfoSerrializer(data=request.data)

        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK, data=get_items_query(**serializer.data))


@require_http_methods(["GET"])
def get_statistisc(request):
    """
    Вью для відображення статистики
    """

    return HttpResponse(creare_html_histogram())
