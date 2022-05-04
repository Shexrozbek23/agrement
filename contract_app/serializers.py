from rest_framework import serializers
from .models import Oferta,inspection_general,type_service,product_type
from rest_framework_gis.serializers import GeoModelSerializer
#get serializer information about the rector
class inspection_generalSerializer(serializers.ModelSerializer):
    class Meta:
        model =inspection_general
        fields = "__all__"

#get serializer information about type of service
class type_serviceSerializer(serializers.ModelSerializer):
    class Meta:
        model =type_service
        fields = "__all__"

#get serializer information about crop type
class product_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model =product_type
        fields = "__all__"

#get serializer information about all contract
class allcontractserializer(serializers.ModelSerializer):
    product_type=product_typeSerializer()
    service_type=type_serviceSerializer()
    general_inspection=inspection_generalSerializer()
    class Meta:
        model =Oferta
        fields = "__all__"
#get serializer information about all contract
class concluding_contract_serializer(GeoModelSerializer):
    class Meta:
        model =Oferta
        geo_field = 'adress_location'
        fields = ['region','payment_amount','district','cadastre_number','product_type','adress_location','square_of_services','applicant_organization','applicant_tin','applicant_fullname','applicant_phone','service_type']
        #these elements is required
        extra_kwargs = {
            'region': {'required': True},
            'district': {'required': True},
            'service_type':{'required': True},
            'cadastre_number': {'required': True},
            'product_type': {'required': False},
            'square_of_services': {'required': True},
            'applicant_organization':{'required': True},
            'applicant_tin': {'required': True},
            'applicant_fullname': {'required': True},
            'applicant_phone': {'required': True},
            'payment_amount': {'required': False},
            'adress_location': {'required': False},

        }

class inn_or_code_number_serializer(serializers.ModelSerializer):
     class Meta:
        model =Oferta
        fields = ['applicant_tin','code_number']