from contract_app import views
from django.urls import path

urlpatterns = [
    path('contract/create',views.Agrement.as_view()),
    path('contract/list',views.ContractFilter.as_view()),
    path('service/type',views.ServieType.as_view()),
    # path('crop/type',views.CropType.as_view()),
    path('district',views.DistrictAll.as_view()),
    path('region',views.Regionall.as_view()),
    ##
    path('aferta/<slug:number>/pdf/',views.PdfVersionView.as_view(), name='pdf_of_ppp_registration_protocol'),
]
