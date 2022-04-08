from pydoc import Doc
from django.contrib import admin
from .models import *

admin.site.register(Address)
admin.site.register(Doctor)
admin.site.register(Patient)