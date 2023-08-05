#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhangyue'

from django import template
from django.conf import settings
from django.shortcuts import reverse
from bee_django_course.models import UserQuestionAnswerRecord
from bee_django_course.exports import filter_local_datetime
from bee_django_course.utils import get_user_name
from bee_django_course.views import get_user_last_course_section

register = template.Library()




# 求两个值的差的绝对值
@register.filter
def get_difference_abs(a, b):
    return abs(a - b)
