from django.contrib import admin
from .models import Mesaje, Report, Favorit, Profile

class MesajeAdmin(admin.ModelAdmin):
    list_display = ['titlu', 'autor', 'destinatar']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['titluu', 'autor', 'destinatar']

class FavoritAdmin(admin.ModelAdmin):
    list_display = ['alegator', 'ales']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['userul', 'produs1', 'produs2', 'produs3', 'produs4', 'produs5', 'image1', 'image2', 'descriere']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Mesaje, MesajeAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Favorit, FavoritAdmin)