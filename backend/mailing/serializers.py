# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from mailing.models import Client, Mail, Message


class MailSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs.get('end_time') < attrs.get('start_time'):
            raise ValidationError(_('The end time cannot be greater than start time'))
        return attrs

    class Meta:
        model = Mail
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        try:
            phone_number = attrs.get('phone')
            if len(phone_number) < 11:
                raise ValidationError(_('The phone number has less than 11 numbers'))
            int(phone_number)
            return attrs
        except ValueError:
            raise ValidationError(_('The phone number has an invalid format'))

    class Meta:
        model = Client
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
