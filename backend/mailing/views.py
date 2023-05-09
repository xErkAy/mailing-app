# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from mailing.exceptions import MailNotFound
from mailing.models import Mail, Client, Message
from mailing.serializers import MailSerializer, ClientSerializer, MessageSerializer


class CreateMail(CreateAPIView):
    serializer_class = MailSerializer
    queryset = Mail.objects.all()


class UpdateDeleteMailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer


class CreateClientAPIView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class UpdateDeleteClientAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class GetMailStatistic(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Message.objects.filter(mail__id=kwargs['pk'])
        if queryset.first() is None:
            raise MailNotFound()

        data = {
            'inProcess': MessageSerializer(instance=queryset.filter(status=1), many=True).data,
            'canceled': MessageSerializer(instance=queryset.filter(status=2), many=True).data,
            'done': MessageSerializer(instance=queryset.filter(status=3), many=True).data
        }

        return Response(data=data, status=status.HTTP_200_OK)
