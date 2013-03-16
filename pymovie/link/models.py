from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Link(models.Model):
    link = models.CharField(verbose_name = "link",max_length=150)
    tipo = models.CharField(verbose_name = "tipo",max_length=10)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')