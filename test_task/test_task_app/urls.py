from django.urls import path

from test_task_app.views import CreateRequest, GetRequestInfo, GetItems, get_statistisc


urlpatterns = [
    path('create-request/', CreateRequest.as_view()),   #Створення запиту на синхронізацію даних
    path('request-info/', GetRequestInfo.as_view()),    #Отримання статусу задачі по ІД
    path('get-items/', GetItems.as_view()),             #Запитуємо речі по заданим параметрам
    path('statistics/', get_statistisc)                 #Завантажуємо статистику у вигляді гістограми
]