# -*- coding: utf-8 -*-
import operator
import logging
from functools import reduce

import requests

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone


from requests import RequestException

from mailing.models import Mail, Client, Message

logger = logging.getLogger('mailing')


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        now = timezone.now().strftime('%Y-%m-%d %H:%M:%S+00:00')

        mails = Mail.objects.filter(
            start_time__lte=now,
            end_time__gte=now
        )

        for mail in mails:
            clients = self._get_clients_by_filters(mail.filters)
            for client in clients:
                message = self._create_message(client, mail)
                self._send_message(message)

    @staticmethod
    def _send_message(message: Message) -> None:
        """ This method allows to send a message using an external API """

        if message is None:
            return

        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ4MzAwODgsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9lcmlrYXJzdGFteWFuIn0.qqTiGFIdLey4Kaa16_YQChpj5yzeZSONod0CTmlhmDw',
        }

        payload = {
            'id': message.id,
            'phone': int(message.client.phone),
            'text': message.mail.text
        }

        try:
            response = requests.post(url=f'https://probe.fbrq.cloud/v1/send/{message.id}', headers=headers, json=payload)
            if response.status_code == 200:
                message.status = 3
                logger.info(f'The message has been successfully sent for client_phone={message.client.phone}, '
                            f'mail_id={message.mail.id}')
            else:
                message.status = 2
                logger.error(f'Occurred error while sending message for client_phone={message.client.phone}, '
                             f'mail_id={message.mail.id}')

            message.save()
        except RequestException as e:
            message.status = 2
            message.save()
            logger.error(f'Occurred error while sending message for client_phone={message.client.phone}, '
                         f'mail_id={message.mail.id}, the error message was: {e}')

    @staticmethod
    def _get_clients_by_filters(filters: str) -> list[Client]:
        """ This method returns a filtered queryset of clients with set parameters"""
        clauses = (Q(tag__contains=tag) for tag in filters.split(','))
        return Client.objects.filter(reduce(operator.or_, clauses))

    @staticmethod
    def _create_message(client: Client, mail: Mail) -> Message:
        """ This method creates a message object in the database. """
        obj = None
        try:
            Message.objects.get(
                mail=mail,
                client=client
            )
            logger.error(f'The mailing for client_phone={client.phone}, mail_id={mail.id} '
                         f'has been already activated, skipping...')
        except Message.DoesNotExist:
            try:
                obj = Message.objects.create(
                    status=1,
                    mail=mail,
                    client=client
                )
            except Exception as e:
                logger.error(f'Occurred an error while creating a message'
                             f'for client_phone={client.phone}, mail_id={mail.id}. '
                             f'The exception was: {e.message}')
        return obj
