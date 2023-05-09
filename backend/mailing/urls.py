# -*- coding: utf-8 -*-
from django.urls import path
from mailing.views import (
    CreateMail,
    UpdateDeleteMailAPIView,
    CreateClientAPIView,
    UpdateDeleteClientAPIView,
    GetMailStatistic
)

urlpatterns = [
    path('user/create/', CreateClientAPIView.as_view(), name='create_client'),
    path('user/<int:pk>/', UpdateDeleteClientAPIView.as_view(), name='update_destroy_client'),

    path('<int:pk>/', UpdateDeleteMailAPIView.as_view(), name='update_destroy_mail'),
    path('create/', CreateMail.as_view(), name='create_mail'),
    path('stat/<int:pk>/', GetMailStatistic.as_view(), name='get_statistic'),
]
