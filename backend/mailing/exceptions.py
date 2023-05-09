# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException


class MailNotFound(APIException):
    default_code = 404
    default_detail = 'The mail with this id has not been found'
