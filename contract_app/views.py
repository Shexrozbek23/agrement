
from django.shortcuts import render
from rest_framework import generics, views, response, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import concluding_contract_serializer,allcontractserializer,inn_or_code_number_serializer
from django.template.loader import render_to_string
from .models import Oferta,type_service,inspection_general,Oferta_detail,QrCode
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa 
import datetime
from .models import Oferta,inspection_general,type_service,product_type,District,Region
from .numer_write_word import son,float2comma

from io import BytesIO
from django.views.generic import View
from django.conf import settings
# Create your views here.
import os




#Get pdf of contract and contract data filter
class Contract_filter(views.APIView):
    def get(self,request):
        inn=self.request.query_params.get("inn")
        aferta_number=self.request.query_params.get("aferta_number")
        contract=Oferta.objects.filter()
        if inn !=None:
            contract=contract.filter(applicant_tin=inn)
        if aferta_number !=None:
            contract=get_object_or_404(Oferta,code_number=aferta_number)
            template_path = 'Shartnoma.html'
            if contract.service_type.id<=5:
                contract.service_type.type='Qishloq xo\'jaligiga mo\'ljallangan yerlarning agrokimyoviy tahlili'
                numer_or_hectare='Gektar'
            else:
                numer_or_hectare='Namuna'
                contract.square_of_services=int(contract.square_of_services)
            #if this id is not avalible, return not found detail
            oferta_detail=get_object_or_404(Oferta_detail,id=1)
            #information for pdf
            qr_url='http://127.0.0.1:8000/?inn={}&aferta_number={}'.format(inn,aferta_number)
            sa=QrCode.objects.create(url=qr_url)
            info={
                    "id": contract.id,
                    "product_type": {
                        "id": contract.product_type.id,
                        "type": contract.product_type.type,   
                    },
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
                    'adress':oferta_detail.adress,
                    'x_r':oferta_detail.x_r,
                    'sh_x':oferta_detail.sh_x,
                    'bank':oferta_detail.bank,
                    'mfo':oferta_detail.mfo,
                    'oked':oferta_detail.oked,
                    'inn':oferta_detail.inn,
                    'phone_number':oferta_detail.phone_number,
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
        return Response(inn_or_code_number_serializer(contract,many=True).data,status=status.HTTP_200_OK)

#Get data about agrements
class Agrement(views.APIView):
    def get(self,request):
        all_agreemant=Oferta.objects.all()
        serializer=concluding_contract_serializer(all_agreemant,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, request):
        serializer=concluding_contract_serializer(data=request.data)
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
            if type_service.objects.filter(id=serializer.data.get('service_type')).exists():
                type=type_service.objects.get(id=serializer.data.get('service_type'))
                if serializer.data.get('square_of_services')>0 :
                    count=serializer.data.get('square_of_services')*type.value
                else:
                    return Response({"error":"You entered minuse number ", "success": False},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"servece_type is not existent ", "success": False},status=status.HTTP_400_BAD_REQUEST)
            #add payment_amount to data   
            data['payment_amount']=count
            # get type of service
            type=type_service.objects.get(id=serializer.data.get('service_type'))
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
            rector=inspection_general.objects.get(id=1)
            data['general_inspection']=rector
            data['code_number']=invoice_number
            print(data.get('adress_location'))
            oneagremment = Oferta.objects.create(**data)
            oneagremment.save()
            return Response(allcontractserializer(oneagremment).data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)