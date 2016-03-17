# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from pzwla_events.models import FieldEvent
from django.db import models


class ZawodyPlugin(CMSPlugin):
    name = models.CharField("Nazwa", max_length=30)
    events_number = models.IntegerField("Liczba wyświetlanych zawodów", default=4)
    add_preferable = models.BooleanField("Czy wyświetlać preferowane", default=True)

    def __unicode__(self):
        return self.name


class WynikiZawodowPlugin(CMSPlugin):
    name = models.CharField("Nazwa", max_length=50)
    events_number = models.IntegerField("Liczba wyświetlanych zawodów", default=4)
    add_preferable = models.BooleanField("Czy wyświetlić w pierwszej kolejności ważne pzwla_events", default=False)

    def __unicode__(self):
        return self.name


class KalukulatorWynikowPlugin(CMSPlugin):
    name = models.CharField("Nazwa", max_length=50)

    def __unicode__(self):
        return self.name
