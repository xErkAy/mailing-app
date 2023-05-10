# -*- coding: utf-8 -*-
from django.db import models


class Mail(models.Model):
    start_time = models.DateTimeField(verbose_name='Start time')
    text = models.CharField(max_length=100, verbose_name='Text')
    filters = models.CharField(max_length=100, verbose_name='Filters')
    end_time = models.DateTimeField(verbose_name='End time')

    def __str__(self):
        return f"[{self.start_time.strftime('%d.%m.%Y %H:%M:%S')} - {self.end_time.strftime('%d.%m.%Y %H:%M:%S')}] {self.text}"

    class Meta:
        verbose_name = 'Mail'
        verbose_name_plural = 'Mails'


class Message(models.Model):
    STATUS = (
        (1, 'In process'),
        (2, 'Canceled'),
        (3, 'Done'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    status = models.PositiveSmallIntegerField(choices=STATUS, verbose_name='Status', default=1)
    mail = models.ForeignKey('mailing.Mail', verbose_name='Mail', on_delete=models.PROTECT)
    client = models.ForeignKey('mailing.Client', verbose_name='Client', on_delete=models.PROTECT)

    def __str__(self):
        return f'[{self.client}] Message: {self.mail.text}. Status: {self.STATUS[self.status - 1][1]}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Client(models.Model):
    TIMEZONES = (
        (1, 'Moscow/Europe'),
        (2, 'Asia/Yekaterinburg')
    )

    phone = models.CharField(max_length=11, verbose_name='Phone number')
    code = models.PositiveSmallIntegerField(verbose_name='Operator code')
    tag = models.CharField(max_length=250, verbose_name='Tag')
    timezone = models.PositiveSmallIntegerField(choices=TIMEZONES, verbose_name='Timezone')

    def __str__(self):
        return self.formatted_phone_number

    @property
    def formatted_phone_number(self):
        return f'+7 ({self.phone[1:4]}) {self.phone[4:7]}-{self.phone[7:9]}-{self.phone[9:11]}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
