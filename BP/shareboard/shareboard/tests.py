from django.test import TestCase
from django import template
# Create your tests here.
register = template.Library()

def ranges_tr(count=4):
    return range(1, count)

def ranges_td(count=5):
    return range(1, count)