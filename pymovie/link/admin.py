from link.models import Link
from django.contrib import admin
from django.contrib.contenttypes import generic


class LinkInlines(generic.GenericStackedInline):
    model = Link
    extra = 1
