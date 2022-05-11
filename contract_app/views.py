
from pickletools import read_uint8
from django.shortcuts import render
from rest_framework import generics, views, response, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import ConcludingContractSerializer,AllContractserializer,InnOrCodeNumberSerializer,TypeServiceSerializer,DistricteSerializer,RegionSerializer
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa 
import datetime
from .models import Oferta,InspectionGeneral,TwoTypeService,TypeService,District,Region,OfertaDetail,QrCode
from .numer_write_word import son,float2comma
from io import BytesIO
from django.views.generic import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
import os


#Get pdf of contract and contract data filter
class ContractFilter(views.APIView):
    def get(self,request):
        inn=self.request.query_params.get("inn")
        aferta_number=self.request.query_params.get("aferta_number")
        contract=Oferta.objects.filter()
        if inn:
            contract=contract.filter(applicant_tin=inn)
        # if not contract.filter(applicant_tin=inn).exists():
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        if aferta_number:
            contract=get_object_or_404(Oferta, code_number=aferta_number)
            template_path = 'Shartnoma.html'
            if contract.service_type.id<=5:
                contract.service_type.type='Qishloq xo\'jaligiga mo\'ljallangan yerlarning agrokimyoviy tahlili'
                numer_or_hectare='Gektar'
            else:
                numer_or_hectare='Namuna'
                contract.square_of_services=int(contract.square_of_services)
            #if this id is not available, return not found detail
            # OfertaDetail=get_object_or_404(OfertaDetail,id=1)
            Detail = OfertaDetail.objects.all().first()
            # OfertaDetail, _ = OfertaDetail.objects.get_or_create(inn=12313)
            #information for pdf
            qr_url='{}?inn={}&aferta_number={}'.format(settings.MAIN_URL,inn,aferta_number)
            sa=QrCode.objects.create(url=qr_url)
            info={
                    "id": contract.id,
                    "product_type": contract.product_type,
                    "service_type": {
                        "id": contract.service_type.id,
                        "type": contract.service_type.type,
                        "value":float2comma(contract.service_type.value) ,  
                    },
                    "general_inspection": {
                        "id": contract.general_inspection.id,
                        "name": contract.general_inspection.name,
                    },
                    "code_number": contract.code_number,
                    "given_date":  contract.given_date,
                    "cadastre_number": contract.cadastre_number,
                    "square_of_services": contract.square_of_services,
                    "payment_amount": float2comma(contract.payment_amount),
                    "paid_amount":float2comma(contract.paid_amount),
                    "applicant_organization": contract.applicant_organization,
                    "applicant_tin": contract.applicant_tin,
                    "applicant_fullname": contract.applicant_fullname,
                    "applicant_phone": contract.applicant_phone,
                    "added_at": "2022-04-29T06:15:54.124708Z",
                    "updated_at": "2022-04-29T06:15:54.641506Z",
                    "region": contract.region.name_en,
                    "district": contract.district.name_en,
                    'numer_or_hectare':numer_or_hectare,
                    'adress':Detail.adress,
                    'x_r':Detail.x_r,
                    'sh_x':Detail.sh_x,
                    'bank':Detail.bank,
                    'mfo':Detail.mfo,
                    'oked':Detail.oked,
                    'inn':Detail.inn,
                    'phone_number':Detail.phone_number,
                    "end_data":int(datetime.datetime.now().strftime('%y')),
                    "payment_amount_word":son(contract.payment_amount),
                    'code_qr':sa
                }
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(contract.code_number)
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(info)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html.encode('UTF-8'), dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        return Response(AllContractserializer(contract,many=True).data,status=status.HTTP_200_OK)

#Get data about agrements
# 
class Agrement(views.APIView):

    def get(self,request):
        all_agreemant=Oferta.objects.all()
        serializer=ConcludingContractSerializer(all_agreemant,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer=ConcludingContractSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            regionall=District.objects.filter(region__id=serializer.data.get('region'))
            #check cadastre number is not minuse number
            if not str(serializer.data.get('cadastre_number')).isdigit() :
                return Response({"error":"can not enter minuse number  to cadastre number"},status=status.HTTP_400_BAD_REQUEST)
            #check applicant_tin is not minuse number
            if not serializer.data.get('applicant_tin').isdigit() :
                return Response({"error":"can not enter minuse number or letter to applicant_inn"},status=status.HTTP_400_BAD_REQUEST)
            #check applicant_phone is not minuse number
            if not serializer.data.get('applicant_phone').isdigit() :
                return Response({"error":"can not enter minuse number or letter to applicant_phone"},status=status.HTTP_400_BAD_REQUEST)
            #check square_of_services is not minuse number
            if serializer.data.get('square_of_services')<0 :
                return Response({"error":"can not enter minuse number to square_of_services"},status=status.HTTP_400_BAD_REQUEST)
            #Check there is district in region
            if not regionall.filter(id=serializer.data.get('district')).exists():
                return Response({"error":"district is existent"},status=status.HTTP_400_BAD_REQUEST)
            #Calculation all payment
            if TypeService.objects.filter(id=serializer.data.get('service_type')).exists():
                type=TypeService.objects.get(id=serializer.data.get('service_type'))
                type2=TwoTypeService.objects.all().first()
                if serializer.data.get('square_of_services')>0 :
                    if type.id==type2.type.id:
                        if serializer.data.get('square_of_services')<=50:
                            count=serializer.data.get('square_of_services')*TwoTypeService.objects.get(id=1).value
                        if serializer.data.get('square_of_services')>50 and serializer.data.get('square_of_services')<=100:
                            count=serializer.data.get('square_of_services')*TwoTypeService.objects.get(id=2).value
                        if serializer.data.get('square_of_services')>100 and serializer.data.get('square_of_services')<=500:
                            count=serializer.data.get('square_of_services')*TwoTypeService.objects.get(id=3).value
                        if serializer.data.get('square_of_services')>500 and serializer.data.get('square_of_services')<=1000:
                            count=serializer.data.get('square_of_services')*TwoTypeService.objects.get(id=4).value
                        if serializer.data.get('square_of_services')>1000:
                            count=serializer.data.get('square_of_services')*TwoTypeService.objects.get(id=5).value
                    else:
                        count=serializer.data.get('square_of_services')*type.value
                else:
                    return Response({"error":"You entered minuse number ", "success": False},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"servece_type is not existent ", "success": False},status=status.HTTP_400_BAD_REQUEST)
            #add payment_amount to data   
            data['payment_amount']=count
            # get type of service
            type=TypeService.objects.get(id=serializer.data.get('service_type'))
            #create aferta number
            current_year = int(datetime.datetime.now().strftime('%y'))
            if int(serializer.data.get('region')) < 10:
                first_four_digits = str(current_year) + '0' + str(serializer.data.get('region'))
            else:
                first_four_digits = str(current_year) + str(serializer.data.get('region'))
            if int(type.id) < 10:
                first_six_digits = str(first_four_digits) + '0' + str(type.id)
            else:
                first_six_digits = str(first_four_digits) + str(type.id)
            last_invoice = Oferta.objects.filter(code_number__startswith=first_six_digits).order_by(
                                'code_number').last()
            if last_invoice:
                invoice_number = int(last_invoice.code_number) + 1
            else:
                invoice_number = int(first_six_digits) * 100000 + 1
            #get data of rector
            #rector=InspectionGeneral.objects.get(id=1)
            rector = InspectionGeneral.objects.all().first()
            data['general_inspection']=rector
            data['code_number']=invoice_number
            print(data.get('adress_location'))
            oneagremment = Oferta.objects.create(**data)
            oneagremment.save()
            return Response(AllContractserializer(oneagremment).data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#get service_type json
class ServieType(views.APIView):
    def get(self,request):
        allservice_serializer=TypeServiceSerializer(TypeService.objects.all(),many=True)
        return Response(allservice_serializer.data,status=status.HTTP_200_OK)

#get crop json
# class CropType(views.APIView):
#     def get(self,request):
#         allcrop_serializer=ProductTypeSerializer(product_type.objects.all(),many=True)
#         return Response(allcrop_serializer.data,status=status.HTTP_200_OK)

#get district 
class DistrictAll(views.APIView):
    def get(self,request):
        region=self.request.query_params.get("region")
        district=District.objects.all()
        if region is not None:
            district=district.filter(region_id=region)
        return Response(DistricteSerializer(district,many=True).data,status=status.HTTP_200_OK)

#get Region json 
class Regionall(views.APIView):
    def get(self,request):
        regionserializers=RegionSerializer(Region.objects.all(),many=True)
        return Response(regionserializers.data,status=status.HTTP_200_OK)

####################
class PdfVersionView(View):
    def get(self, request, *args, **kwargs):
        contract = get_object_or_404(Oferta, code_number=kwargs['number'])
        template_path = 'Shartnoma.html'
        if contract.service_type.id <= 5:
            contract.service_type.type = 'Qishloq xo\'jaligiga mo\'ljallangan yerlarning agrokimyoviy tahlili'
            numer_or_hectare = 'Gektar'
        else:
            numer_or_hectare = 'Namuna'
            contract.square_of_services = int(contract.square_of_services)
        # if this id is not available, return not found detail
        # OfertaDetail=get_object_or_404(OfertaDetail,id=1)
        Detail = OfertaDetail.objects.all().first()
        # OfertaDetail, _ = OfertaDetail.objects.get_or_create(inn=12313)
        # information for pdf
        qr_url = 'http://127.0.0.1:8000/agrement/aferta/{}/pdf/'.format(contract.code_number)
        sa = QrCode.objects.create(url=qr_url)
        info = {
            "id": contract.id,
            "product_type": contract.product_type,
            "service_type": {
                "id": contract.service_type.id,
                "type": contract.service_type.type,
                "value": float2comma(contract.service_type.value),
            },
            "general_inspection": {
                "id": contract.general_inspection.id,
                "name": contract.general_inspection.name,
            },
            "code_number": contract.code_number,
            "given_date": contract.given_date,
            "cadastre_number": contract.cadastre_number,
            "square_of_services": contract.square_of_services,
            "payment_amount": float2comma(contract.payment_amount),
            "paid_amount": float2comma(contract.paid_amount),
            "applicant_organization": contract.applicant_organization,
            "applicant_tin": contract.applicant_tin,
            "applicant_fullname": contract.applicant_fullname,
            "applicant_phone": contract.applicant_phone,
            "added_at": "2022-04-29T06:15:54.124708Z",
            "updated_at": "2022-04-29T06:15:54.641506Z",
            "region": contract.region.name_en,
            "district": contract.district.name_en,
            'numer_or_hectare': numer_or_hectare,
            'adress': Detail.adress,
            'x_r': Detail.x_r,
            'sh_x': Detail.sh_x,
            'bank': Detail.bank,
            'mfo': Detail.mfo,
            'oked': Detail.oked,
            'inn': Detail.inn,
            'phone_number': Detail.phone_number,
            "end_data": int(datetime.datetime.now().strftime('%y')),
            "payment_amount_word": son(contract.payment_amount),
            'code_qr': sa
        }
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(contract.code_number)
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(info)
        # create a pdf
        pisa_status = pisa.CreatePDF(
            html.encode('UTF-8'), dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response