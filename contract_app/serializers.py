from rest_framework import serializers
from .models import Oferta,InspectionGeneral,TypeService,District,Region
from rest_framework_gis.serializers import GeoModelSerializer
#get serializer information about the rector
class InspectionGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model =InspectionGeneral
        fields = "__all__"

#get serializer information about type of service
class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model =TypeService
        fields = "__all__"

#get serializer information about district
class DistricteSerializer(serializers.ModelSerializer):
    class Meta:
        model =District
        fields = "__all__"

#get serializer information about region
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Region
        fields = "__all__"

#get serializer information about all contract
class AllContractserializer(serializers.ModelSerializer):
    service_type=TypeServiceSerializer()
    general_inspection=InspectionGeneralSerializer()
    class Meta:
        model =Oferta
        fields = "__all__"
#get serializer information about all contract
class ConcludingContractSerializer(GeoModelSerializer):
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
            'adress_location': {'required': True},
        }
        
#get serializer information about inn and aferta number
class InnOrCodeNumberSerializer(serializers.ModelSerializer):
     class Meta:
        model =Oferta
        fields = ['applicant_tin','code_number']