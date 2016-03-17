# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from pzwla_events.models import FieldEvent
from models import ZawodyPlugin
from models import WynikiZawodowPlugin
from datetime import datetime
from pzwla_events.models import utc


class CMSZawodyPlugin(CMSPluginBase):
    model = ZawodyPlugin  # model where plugin data are saved
    module = _("Zawody")
    name = _("Wtyczka - najblizsze zawody")  # name of the plugin in the interface
    render_template = "pzwla_events/zawody_plugin.html"

    def render(self, context, name, placeholder):
        settings = ZawodyPlugin.objects.all()[0]
        events = list()
        events_number = 0

        if settings.add_preferable:
            events_query = FieldEvent.objects.all().filter(preferable=True, date_time__gt=datetime.now(tz=utc))\
                .order_by('date_time')
            for event in events_query:
                events.append(event)
            events_number = len(events)

        for event in FieldEvent.objects.all().filter(date_time__gt=datetime.now(tz=utc)).order_by('date_time'):
            if event in events:
                continue
            if events_number > settings.events_number:
                break
            events.append(event)
            events_number += 1

        events.sort(key=lambda x: x.date_time)

        dates = list()

        for event in events:
            dates.append(event.date_time.strftime("%Y/%m/%d"))
        context.update({'name': name,
                        'events': events,
                        'dates': dates
                        })
        return context


class CMSWynikiZawodowPlugin(CMSPluginBase):
    model = WynikiZawodowPlugin
    module = _("Zawody")
    name = _("Wtyczka - najnowsze wyniki zawodow")  # name of the plugin in the interface
    render_template = "pzwla_events/wyniki_plugin.html"

    def render(self, context, name, placeholder):
        settings = ZawodyPlugin.objects.all()[0]
        events = list()
        events_number = 0
        if settings.add_preferable:
            events_query = FieldEvent.objects.all().filter(preferable=True, date_time__lt=datetime.now(tz=utc))\
                .order_by('date_time')
            for event in events_query:
                events.append(event)
            events_number = len(events)

        for event in FieldEvent.objects.all().filter(date_time__lt=datetime.now(tz=utc)).order_by('date_time'):
            if event in events:
                continue
            if events_number > settings.events_number:
                break
            events.append(event)
            events_number += 1

        events.sort(key=lambda x: x.date_time)

        context.update({'name': name,
                        'last_meetings': events,
                        })
        return context


class CMSKalkulatorWynikowPlugin(CMSPluginBase):
    module = _("Zawody")
    name = _("Wtyczka - kalkulator zawodow")  # name of the plugin in the interface
    render_template = "pzwla_events/kalkulator_plugin.html"

plugin_pool.register_plugin(CMSZawodyPlugin)
plugin_pool.register_plugin(CMSWynikiZawodowPlugin)
plugin_pool.register_plugin(CMSKalkulatorWynikowPlugin)
