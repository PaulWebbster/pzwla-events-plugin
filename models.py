# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from pzwla_events.models import FieldEvent
from django.db import models
from filer.models.foldermodels import Folder
from filer.models.filemodels import File
import os
from settings import *
from django.contrib.staticfiles.templatetags.staticfiles import static

class ExplorerFile(File):
    class Meta:
        proxy = True

    objects = models.Manager()

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        # the extensions we'll recognise for this file type
        filename_extensions = ['.doc', '.docx', '.pdf', '.xls', '.odt', ]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

    @property
    def get_document_icon(self):
        r = {}
        ext = os.path.splitext(str(self.file))[1][1:]
        file_img = 'regular'
        for extension in SUPPORTED_EXTENSIONS:
            if ext in SUPPORTED_EXTENSIONS[extension]:
                file_img = extension

        for size in ICON_SIZES:
            r[size] = static('pzwla_events/icons/%s_file_%sx%s.png' % (file_img, size, size))
        return r['32']

    @property
    def get_mb_size(self):
        return "%.2f MB" % (float(self.size)/1024/1024)

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


class OstatnioDodanePlikiPlugin(CMSPlugin):
    name = models.CharField("Nazwa wyświetlana w nagłówku", max_length=50)
    files_number = models.IntegerField("Liczba wyświetlanych ostatnio dodanych plików", default=4)
    files_folder = models.ForeignKey(Folder)

    def __unicode__(self):
        return self.name


class InformacjeONachodzacychZawodach(CMSPlugin):
    events_number = models.IntegerField("Liczba informacji wyświetlanych o najbliższych zawodach", default=8)

    def __unicode__(self):
        return u"Informacje o nadchodzacych zawodach"


class KalukulatorWynikowPlugin(CMSPlugin):
    name = models.CharField("Nazwa", max_length=50)

    def __unicode__(self):
        return self.name
