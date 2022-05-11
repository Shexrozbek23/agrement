from django.contrib import admin
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import District,Region,OfertaDetail,Oferta,TypeService,InspectionGeneral,QrCode,TwoTypeService
# Register your models here.
admin.site.register(District)
admin.site.register(Region)
admin.site.register(OfertaDetail)
admin.site.register(Oferta,LeafletGeoAdmin)

admin.site.register(TypeService)
admin.site.register(InspectionGeneral)
admin.site.register(QrCode)
admin.site.register(TwoTypeService)
