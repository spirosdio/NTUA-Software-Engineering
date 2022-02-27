"""tolls21 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import *
from django.urls import include, re_path


urlpatterns = [
    path('djangoadmin/', admin.site.urls),
    path('interoperability/api/PassesPerStation/<station>/<startdate>/<enddate>', PassPerStation.as_view()),
    path('interoperability/api/PassesCost/<op1>/<op2>/<startdate>/<enddate>', PassesCost.as_view()),    
    path('interoperability/api/PassesAnalysisAndChargesBy/<op1>/<op2>/<startdate>/<enddate>', PassesAnalysisAndChargesBy.as_view()),
    path('interoperability/api/PassesAnalysis/<op1>/<op2>/<startdate>/<enddate>', PassesAnalysis.as_view()),
    path('interoperability/api/ChargesBy/<op>/<startdate>/<enddate>', ChargesBy.as_view()),
    path("backend/ChargesBy/<op>/<startdate>/<enddate>",  ChargesByBackend.as_view()),
    path('backend/ChargesTo/<op>/<startdate>/<enddate>', ChargesToBackend.as_view()),
    path('backend/uploadCSV', FileUploadAPIView.as_view()),
    path('backend/deleteCSV', deleteTest.as_view()),
    path('interoperability/api/admin/resetpasses', resetpasses.as_view()),
    path('interoperability/api/admin/resetstations', resetstations.as_view()),
    path('interoperability/api/admin/resetvehicles', resetvehicles.as_view()),
    # path('/admin/healthcheck', ) ,
    re_path(r'^ht/', include('health_check.urls')),
    path('interoperability/api/admin/healthcheck', healthcheck.as_view()),
    re_path(r'^interoperability/api/', include('rest_auth.urls')),
    # re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
    # url(r'^ht/', include('health_check.urls')),
    path('interoperability/api/getprovider', getprovider.as_view())

]

