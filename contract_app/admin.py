from django.contrib import admin
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import District,Region,Oferta_detail,Oferta,product_type,type_service,inspection_general,QrCode
# Register your models here.
admin.site.register(District)
admin.site.register(Region)
admin.site.register(Oferta_detail)
admin.site.register(Oferta,LeafletGeoAdmin)
admin.site.register(product_type)
admin.site.register(type_service)
admin.site.register(inspection_general)
admin.site.register(QrCode)
