# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from pzwla_events.models import FieldEvent
from models import ZawodyPlugin
from models import WynikiZawodowPlugin
from models import OstatnioDodanePlikiPlugin
from models import ExplorerFile
from models import InformacjeONachodzacychZawodach
from datetime import datetime
from filer.models.foldermodels import Folder
from pzwla_events.models import utc
from django.db.models import Q


class CMSInformacjeONajblizszychZawodach(CMSPluginBase):
    model = InformacjeONachodzacychZawodach
    module = _("Zawody")
    name = _("Wtyczka - informacje o zblizajacych sie zawodach")
    render_template = "pzwla_events/informacje_plugin.html"

    def render(self, context, instance, placeholder):
        max_events_number = self.model.objects.all()[0].events_number
        events = list()
        events_number = 0

        for event in FieldEvent.objects.all().filter(date_time__gt=datetime.now(tz=utc)).order_by('date_time')\
                .exclude(Q(entry_booklet='') & Q(entry_booklet_file='')).order_by('-date_time'):
            if event in events:
                continue
            if events_number > max_events_number:
                break

            events.append(event)
            events_number += 1

        events.sort(key=lambda x: x.date_time)

        dates = list()

        for event in events:
            dates.append(event.date_time.strftime("%Y/%m/%d"))
        context.update({'name': instance,
                        'events': events,
                        'dates': dates
                        })
        return context


class CMSOstatnioDodanelikiPlugin(CMSPluginBase):
    model = OstatnioDodanePlikiPlugin  # model where plugin data are saved
    module = _("Zawody")
    name = _("Wtyczka - ostatnio dodane pliki")  # name of the plugin in the interface
    render_template = "pzwla_events/pliki_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        context['files'] = self.get_subfolder_files(instance.files_folder)[-instance.files_number:]
        return context

    def get_subfolder_files(self, parent):
        files_list = []
        sub_folders = []

        for obj in Folder.objects.all().filter(parent=parent):
            if obj.file_type == "Folder":
                sub_folders.append(obj)

        for folder in sub_folders:
            files_list.extend(self.get_subfolder_files(folder))

        files_list.extend(self.get_files(parent))

        return files_list

    @staticmethod
    def get_files(folder):
        files = []
        for fp in folder.files:
            files.append(ExplorerFile.objects.get(id=fp.id))

        return files


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

        for event in FieldEvent.objects.all().filter(date_time__lt=datetime.now(tz=utc))\
                .exclude(Q(results_file='') & Q(results='')).order_by('-date_time'):
            #dupa
            if event in events:
                continue
            if events_number > settings.events_number:
                break

            if event.results or event.results_file:
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

plugin_pool.register_plugin(CMSOstatnioDodanelikiPlugin)
plugin_pool.register_plugin(CMSZawodyPlugin)
plugin_pool.register_plugin(CMSWynikiZawodowPlugin)
plugin_pool.register_plugin(CMSKalkulatorWynikowPlugin)
plugin_pool.register_plugin(CMSInformacjeONajblizszychZawodach)
