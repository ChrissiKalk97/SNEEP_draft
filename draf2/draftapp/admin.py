from django.contrib import admin

from .models import Enhancers, Snps

admin.site.register(Enhancers)
admin.site.register(Snps)