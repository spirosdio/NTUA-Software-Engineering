from telnetlib import AUTHENTICATION
from django.utils.timezone import make_aware
from rest_framework.response import Response
from .management.commands.populate import populate_pass_events,populate_stations,populate_vehicles
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.db.models import query
from django.core.serializers import serialize
import json
from itertools import chain 
from django.db.models import Avg, Count, Min, Sum
from django.test import tag
import io
import csv
import requests
# from rest_framework_csv import 
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core import serializers
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,

    )
from rest_framework import generics
from rest_framework.generics import ListAPIView,UpdateAPIView


from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework_csv.renderers import JSONRenderer, CSVRenderer
from rest_framework import status
import json, os
import datetime
from .models import *

from datetime import datetime

from rest_framework.exceptions import APIException

# def getJsonObject(objects, model):
#         list=[]
#         for object in objects:
#             temp={}
#             for field in model._meta.fields:
#                 fieldname = field.get_attname_column()
#                 fieldobj = model._meta.get_field(fieldname[0])
#                 value = fieldobj.value_from_object(object)
#                 temp[fieldname[1]] = value
#             list.append(temp)
#         dict = {}
#         for i, sub_dict in enumerate(list):
#             dict[i] = sub_dict
#         dictlist = []
#         for key, value in dict.items():
#             temp = value
#             dictlist.append(temp)    
#         return json.loads(json.dumps(dictlist, indent=4, sort_keys=True, default=str))

## for pagination
def stringToDate(string):
    format = "%Y%m%d"

    try:
        start=datetime.strptime(string, format)
        return str(start)
        print("This is the correct date string format.")
    except ValueError:
        raise BadRequest()


def check_dates(startdate,enddate):
    format = "%Y%m%d"

    try:
        start=datetime.strptime(startdate, format)

        print("This is the correct date string format.")
    except ValueError:
        raise BadRequest()
    try:
        end=datetime.strptime(enddate, format)

        print("This is the correct date string format.")
    except ValueError:
        raise BadRequest()

    if (start>end): raise BadRequestDateFromTo()


class NoData(APIException):
    status_code = 402
    default_detail = 'No data'
    default_code = 'No data'


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad Request'
    default_code = 'Bad Request'


class NotAuthorized(APIException):
    status_code = 401
    default_detail = 'Not authorized'
    default_code = 'Not authorized'

class InternalError(APIException):
    status_code = 500
    default_detail = 'Internal server error'
    default_code = 'Internal server error'



class BadRequestDateFromTo(APIException):
    status_code = 400
    default_detail = 'Start Date can not be after Finish Date'
    default_code = 'Start Date can not be after Finish Date'



class PassesAnalysisPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page'

    def get_paginated_response(self, data):
        # print(dict(item))

        try:


            passes=dict(data[0])["pass_event_set"] 
            charges = [dict(item)['charge'] for item in passes]
            count = [dict(item)['charge'] for item in passes]
            counter=len(count)
            page_price_avg = sum(charges)
            # print(data)
            # op1 = self.kwargs["op1"]

            periodfrom=dict(data[0])["PeriodFrom"]
            
            return Response({
                'NumberOfPasses': counter,
                'page_price_avg': page_price_avg,
                # 'results': data[0]["pass_event_set"],
                # "station_id" : data[0]["station_id"],
                # "station_name" : data[0]["station_name"],
                # "provider" : data[0]["provider"],

                # 'RequestTimestamp': data[0]["RequestTimestamp"],
                # "PeriodFrom" : data[0]["PeriodTo"],
                # "station_name" : data[0]["station_name"],
                # "provider" : data[0]["provider"],


            })

        except ValueError:
            raise InternalError()








class StationPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page'

    def get_paginated_response(self, data):
        # print(dict(item))
        try:
            passes=dict(data[0])["pass_event_set"]
        except:
            print(154)
            raise NoData()

        try:
            passes=dict(data[0])["pass_event_set"]

            charges = [dict(item)['PassCharge'] for item in passes]
            count = [dict(item)['PassCharge'] for item in passes]
            counter=len(count)
            page_price_avg = sum(charges)
            # print(data)
            # op1 = self.kwargs["op1"]

            periodfrom = stringToDate(dict(data[0])["PeriodFrom"])
            periodTo = stringToDate(dict(data[0])["PeriodTo"])

            print("\n\n\n\n",stringToDate(dict(data[0])["PeriodFrom"]),"\n\n\n\n\n")
            startString=dict(data[0])["PeriodFrom"]
            finishString=dict(data[0])["PeriodTo"]



            for i in range(0,len(passes)):
                passes[i]["PassIndex"]=i


            return Response(
                {
                "Station" : data[0]["station_id"],
                # "station_name" : data[0]["station_name"],
                "StationOperator" : data[0]["provider"],
                'RequestTimestamp': data[0]["RequestTimestamp"],
                "PeriodFrom" : periodfrom,
                "PeriodTo" : periodTo,
                'NumberOfPasses': counter,
                # 'page_price_avg': page_price_avg,
                'PassesList': data[0]["pass_event_set"],
                # "station_name" : data[0]["station_name"],
                # "StationOperator" : data[0]["provider"],
                

                # 'RequestTimestamp': data[0]["RequestTimestamp"],
                # "PeriodFrom" : periodfrom,
                # "PeriodTo" : periodTo,
                # "station_name" : data[0]["station_name"],
                # "provider" : data[0]["provider"],


            })

        except ValueError:
                raise InternalError()
        



##################################################11111111111111111111##################################################

class PassPerStation(generics.ListAPIView):
    serializer_class = StationSerializer
    pagination_class= StationPagination
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """


        try:
            stationkwarg = self.kwargs["station"] 
            startString = self.kwargs["startdate"]
            finishString = self.kwargs["enddate"]
            check_dates(startString,finishString)


            # startStrstartdateing = startdate[0:4] + "-" + startdate[4:6] + "-" + startdate[6:8] + " 00:00:00"
            queryset=station.objects.filter(station_id=stationkwarg)#.order_by(str(pass_event.timestamp))
            return queryset


        except ValueError:
            raise InternalError()
        
##################################################222222222222222222##################################################

class PassesAnalysis(generics.ListAPIView):
    serializer_class = AnalysisPassSerializer
    pagination_class=  None

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        try:
            op1 = self.kwargs["op1"]
            op2 = self.kwargs["op2"]
            startdate = self.kwargs["startdate"]
            enddate = self.kwargs["enddate"]
            startString = stringToDate(startdate)
            finishString = stringToDate(enddate)

            check_dates(startdate,enddate)




            # startStrstartdateing = startdate[0:4] + "-" + startdate[4:6] + "-" + startdate[6:8] + " 00:00:00"
            # pro1= provider.objects.filter(provider_id=op1)
            # pro2= provider.objects.filter(provider_id=op2)
            queryset=pass_event.objects.all().order_by("timestamp")
            # queryset=list(chain (pro1,pro2,query1 ))
            # queryset= pro1 | pro2 | query1
            return queryset

        except ValueError:
            raise InternalError()


    def list(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)


            try:
                serializer.data[0]
            except:
                raise NoData()
            


            newdata=serializer.data
            for i in range(0,len(newdata)):
                newdata[i]["PassIndex"]=i

            

            charges = [dict(item)['Charge'] for item in newdata]
            summer = sum(charges)
            counter= len(charges)
            mydatetime=datetime.now()
            timestamp=str(mydatetime)[:-7]

            # change the data
            # serializer.data is the response that your serializer generates
            res = {
                "op1_ID"    : self.kwargs["op1"],
                "op2_ID"    : self.kwargs["op2"],
                "RequestTimestamp" : timestamp ,
                "PeriodFrom" : stringToDate(self.kwargs["startdate"]),
                "PeriodTo"  :stringToDate( self.kwargs["enddate"]),
                "NumberOfPasses" : counter ,
                "PassesList": serializer.data,

                
            
            }
        
            return Response(res)
        
        except ValueError:
            raise InternalError()



    def counter(self ):
        try:
            serializer=AnalysisPassSerializer(pass_event.objects.all())

            return serializer.data

        except ValueError:
            raise InternalError()




##################################################333333333333333333##################################################

class PassesCost(generics.ListAPIView):
    serializer_class = AnalysisPassSerializer
    pagination_class=  None

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        try:
            op1 = self.kwargs["op1"]
            op2 = self.kwargs["op2"]
            startdate = self.kwargs["startdate"]
            enddate = self.kwargs["enddate"]
            startString = stringToDate(startdate)
            finishString = stringToDate(enddate)
            check_dates(startdate,enddate)
            queryset=pass_event.objects.all()
            return queryset

        except ValueError:
            raise InternalError()

    def list(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)


            try:
                serializer.data[0]
            except:
                raise NoData()

            newdata=serializer.data
            charges = [dict(item)['Charge'] for item in newdata]
            summer = sum(charges)
            counter= len(charges)

            mydatetime=datetime.now()
            timestamp=str(mydatetime)[:-7]
            # change the data
            # serializer.data is the response that your serializer generates
            res = {
                "op1_ID"    : self.kwargs["op1"],
                "op2_ID"    : self.kwargs["op2"],

                "RequestTimestamp" : timestamp ,
                "PeriodFrom" : stringToDate(self.kwargs["startdate"]),
                "PeriodTo"  :stringToDate( self.kwargs["enddate"]),
                "NumberOfPasses" : counter ,
                "PassesCost"   : summer,

                
            
            }
        
            return Response(res)

        except ValueError:
            raise InternalError()

    def counter(self ):
        try:
            serializer=AnalysisPassSerializer(pass_event.objects.all())

            return serializer.data

        except ValueError:
            raise InternalError()
#############################################dummy#######################################################

class PassesAnalysisAndChargesBy(generics.ListAPIView):
    serializer_class = AnalysisPassSerializer
    pagination_class=  None


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        try:
            op1 = self.kwargs["op1"]
            op2 = self.kwargs["op2"]
            startdate = self.kwargs["startdate"]
            enddate = self.kwargs["enddate"]

            startString = stringToDate(startdate)
            finishString = stringToDate(enddate)

            check_dates(startdate,enddate)
            # startStrstartdateing = startdate[0:4] + "-" + startdate[4:6] + "-" + startdate[6:8] + " 00:00:00"
            # pro1= provider.objects.filter(provider_id=op1)
            # pro2= provider.objects.filter(provider_id=op2)
            queryset=pass_event.objects.all()
            # queryset=list(chain (pro1,pro2,query1 ))
            # queryset= pro1 | pro2 | query1
            return queryset

        except ValueError:
            raise InternalError()


    def list(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)

            try:
                serializer.data[0]
            except:
                raise NoData()


            newdata=serializer.data

            for i in range(0,len(newdata)):
                newdata[i]["PassIndex"]=i
            
            charges = [dict(item)['Charge'] for item in newdata]
            summer = sum(charges)
            counter= len(charges)

            # change the data
            # serializer.data is the response that your serializer generates
            res = {
                "op1_ID"    : self.kwargs["op1"],
                "op2_ID"    : self.kwargs["op2"],
                "charges"   : summer,
                "NumberOfPasses" : counter ,
                "PeriodFrom" :stringToDate(self.kwargs["startdate"]) ,
                "PeriodTo"  : stringToDate(self.kwargs["enddate"]),
                "PassesList": serializer.data,
                
            
            }
        
            return Response(res)

        except ValueError:
            raise InternalError()

    def counter(self ):

        serializer=AnalysisPassSerializer(pass_event.objects.all())

        return serializer.data


##################################################44444444444444444444444#############################################



class ChargesBy(generics.ListAPIView):
    serializer_class = ChargesByPassSerializer
    pagination_class=  None
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """

        try:
            # op1 = self.kwargs["op1"]
            op = self.kwargs["op"]
            startdate = self.kwargs["startdate"]
            enddate = self.kwargs["enddate"]
            startString = stringToDate(startdate)
            finishString = stringToDate(enddate)

            check_dates(startdate,enddate)
            # startStrstartdateing = startdate[0:4] + "-" + startdate[4:6] + "-" + startdate[6:8] + " 00:00:00"
            # pro1= provider.objects.filter(provider_id=op1)
            # pro2= provider.objects.filter(provider_id=op2)
            queryset=pass_event.objects.all()

            # queryset=list(chain (pro1,pro2,query1 ))
            # queryset= pro1 | pro2 | query1
            return queryset
        
        except ValueError:
            raise InternalError()

    def list(self, request, *args, **kwargs):

        try:

            serializer = self.get_serializer(self.get_queryset(), many=True)

            #try:
            #    serializer.data[0]
            #except:
            #    raise NoData()


            newdata=serializer.data
            #print(newdata)
            charges = [dict(item)['charge'] for item in newdata]

            numberPerOperator = {} 
            chargePerOperator = {}
            ##count
            for item in newdata:
                tagProvider=dict(item)['TagProvider']
                numberPerOperator[tagProvider]=0
                chargePerOperator[tagProvider]=0
            for item in newdata:
                tagProvider=dict(item)['TagProvider']
                charger=dict(item)['charge']
                numberPerOperator[tagProvider]=numberPerOperator[tagProvider]+1
                chargePerOperator[tagProvider]=chargePerOperator[tagProvider]+charger
            summer = sum(charges)
            counter= len(charges)
            mydatetime=datetime.now()
            timestamp=str(mydatetime)[:-7]
            objectLists=[]

            
            for (k,v), (k2,v2) in zip(numberPerOperator.items(), chargePerOperator.items()):
                myprovider = provider.objects.get(fullname=k)
                bidict={}
                bidict["VisitingOperator"]=myprovider.provider_id
                bidict["NumberOfPasses"] = v
                bidict["PassesCost"] = v2
                qdict = QueryDict("", mutable=True)
                qdict.update(bidict)
                objectLists.append(qdict)
            


            # change the data
            # serializer.data is the response that your serializer generates
            res = {
                "op_ID"    : self.kwargs["op"],
                "RequestTimestamp" : timestamp ,
                #"NumberOfPasses" : counter ,
                "PeriodFrom" : stringToDate(self.kwargs["startdate"]),
                "PeriodTo"  : stringToDate(self.kwargs["enddate"]),
                # "PassesList": serializer.data,
                # "merchant" : merchants,
                "PPOList" :objectLists        
            }

            return Response(res)


        except ValueError:
            raise InternalError()

    def counter(self):
        serializer=ChargesByPassSerializer(pass_event.objects.all())
        return serializer.data










############################# backend 1st use case ###################################3


### read pass_event csv and populate (Someone have to implement the appropriate error handling)

class FileUploadAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            file = serializer.validated_data['file']
            decoded_file = file.read().decode()
            # upload_products_csv.delay(decoded_file, request.user.pk)
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)
            next(reader)
            for row in reader:
                if row:
                    ### error handling for , ; 
                    #### CREATE PASSID

                    strings = row[0].split(";")
                    #print(strings)
                    date = strings[1].split()[0].split("/")
                    time = strings[1].split()[1].split(":")
                    obj, created = pass_event.objects.get_or_create(
                        pass_id = strings[0],
                        timestamp = make_aware(datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))),
                        vehicleRef = vehicle.objects.get(vehicle_id=strings[3]),
                        stationRef = station.objects.get(station_id=strings[2]),
                        charge = float(strings[4])
                    )
                    if created: print(f"Table entry {obj} created!")
                    else: print(f"Table entry {obj} already exists!")
            print("Done populating pass events table!\n")        


            ######## edw prepei error handling gia lathos format !!!!!! 
            return Response({'status':'OK'})

        except ValueError:
            raise InternalError()



########################################## reset #######################################


############ passes ############

############ stations ############


############ vehicles ############




class resetpasses(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, format=None):
        try:
             ### first drop database ####
            pass_event.objects.all().delete()
            # populate_stations()
        
        except ValueError:
            raise InternalError()
        return Response({'status':'OK'})




class resetstations(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, format=None):
        try:
             ### first drop database ####
            station.objects.all().delete()
            populate_stations()
        
        except ValueError:
            raise InternalError()
        return Response({'status':'OK'})





class resetvehicles(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, format=None):
        try:
            ### first drop database ####
            vehicle.objects.all().delete()
            populate_vehicles()
        except ValueError:
            raise InternalError()
        return Response({'status':'OK'})


class healthcheck(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None): 
        try:
            r=requests.get('http://127.0.0.1:9103/ht')
            print(r.data)
        except :
            return Response( {"status":"OK","dbconnection":"BM25PHF40639ekjejuwn34553JSQ0002840"})


class getprovider(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sela = self.request.user
        userID = sela.id
        providerID = provider.objects.get(user_id=userID)
        return Response({"provider_id": providerID.provider_id})











# def populate_pass_events():
#     print("Populating pass events from sampledata01_passes100_8000.csv")
#     file = open('../../sample_data/sampledata01_passes100_8000.csv')
#     reader = csv.reader(file)
#     next(reader)
#     for row in reader:
#         strings = row[0].split(";")
#         date = strings[1].split()[0].split("/")
#         time = strings[1].split()[1].split(":")
#         obj, created = pass_event.objects.get_or_create(
#             pass_id = strings[0],
#             timestamp = make_aware(datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))),
#             vehicleRef = vehicle.objects.get(vehicle_id=strings[3]),
#             stationRef = station.objects.get(station_id=strings[2]),
#             charge = float(strings[4])
#         )
#         if created: print(f"Table entry {obj} created!")
#         else: print(f"Table entry {obj} already exists!")
#         ######## edw prepei error handling gia lathos format !!!!!!


#     print("Done populating pass events table!\n")













#      
# class CsvToDatabase(APIView):

#     def post(self, request, format=None):
#         data = request.data
#         for vendor in data:
#             Vendors(
#                 vendor_name=vendor['Vendor'],
#                 country=vendor['Country']
#             ).save()


#         return Response({'received data': request




# def csv_file_parser(file):
#     result_dict = {}
#     with open(file) as csvfile:
#         reader = csv.DictReader(csvfile)
#         line_count = 1
#         for rows in reader:
#             for key, value in rows.items():
#                 if not value:
#                     raise ParseError('Missing value in file. Check the {} line'.format(line_count))
#             result_dict[line_count] = rows
#             line_count += 1


#     return result_dict




# class FileUploadView(APIView):
#     parser_classes = ( MultiPartParser, FormParser)
#     renderer_classes = [JSONRenderer]

#     def put(self, request, format=None):
#         if 'file' not in request.data:
#             raise ParseError("Empty content")
#         f = request.data['file']
#         filename = f.name
#         if filename.endswith('.csv'):
#             file = default_storage.save(filename, f)
#             r = csv_file_parser(file)
#             status = 204
#         else:
#             status = 406
#             r = "File format error"
#         return Response(r, status=status)

class deleteTest(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def post(self, request, format=None):
        try:
             ### first drop database ####
            x=1000000000
            for i in range(1,100+1):
                obj = pass_event.objects.filter(pass_id = str(x+i)).delete()
            # populate_stations()
        except:
            return Response({'status':'failed'})
        return Response({'status':'OK'})












class ChargesByBackend(generics.ListAPIView):
    serializer_class = ChargesByPassSerializer
    pagination_class=  None
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """

        try:
            # op1 = self.kwargs["op1"]
            op = self.kwargs["op"]
            startdate = self.kwargs["startdate"]
            enddate = self.kwargs["enddate"]
            startString = startdate[0:4] + startdate[4:6] + startdate[6:11] + " 00:00:00"
            finishString = enddate[0:4] + enddate[4:6] +  enddate[6:11] + " 23:59:59"

            check_dates(startdate,enddate)
            # startStrstartdateing = startdate[0:4] + "-" + startdate[4:6] + "-" + startdate[6:8] + " 00:00:00"
            # pro1= provider.objects.filter(provider_id=op1)
            # pro2= provider.objects.filter(provider_id=op2)
            queryset=pass_event.objects.all()

            # queryset=list(chain (pro1,pro2,query1 ))
            # queryset= pro1 | pro2 | query1
            return queryset
        
        except ValueError:
            raise InternalError()

    def list(self, request, *args, **kwargs):

        try:

            serializer = self.get_serializer(self.get_queryset(), many=True)

            try:
                serializer.data[0]
            except:
                raise NoData()


            newdata=serializer.data
            print(newdata)
            charges = [dict(item)['charge'] for item in newdata]

            numberPerOperator = {} 
            chargePerOperator = {}
            ##count
            for item in newdata:
                tagProvider=dict(item)['TagProvider']
                numberPerOperator[tagProvider]=0
                chargePerOperator[tagProvider]=0
            for item in newdata:
                tagProvider=dict(item)['TagProvider']
                charger=dict(item)['charge']
                numberPerOperator[tagProvider]=numberPerOperator[tagProvider]+1
                chargePerOperator[tagProvider]=chargePerOperator[tagProvider]+charger
            summer = sum(charges)
            counter= len(charges)
            mydatetime=datetime.now()
            timestamp=str(mydatetime)[:-7]
            objectLists=[]

            
            for (k,v), (k2,v2) in zip(numberPerOperator.items(), chargePerOperator.items()):
                myprovider = provider.objects.get(fullname=k)
                bidict={}
                bidict["VisitingOperator"]=myprovider.provider_id
                bidict["NumberOfPasses"] = v
                bidict["PassesCost"] = v2
                qdict = QueryDict("", mutable=True)
                qdict.update(bidict)
                objectLists.append(qdict)
            


            # change the data
            # serializer.data is the response that your serializer generates
            res = {
                "op_ID"    : self.kwargs["op"],
                "RequestTimestamp" : timestamp ,
                #"NumberOfPasses" : counter ,
                "PeriodFrom" : self.kwargs["startdate"]+" "+'00:00:00',
                "PeriodTo"  : self.kwargs["enddate"]+" "+'00:00:00',
                # "PassesList": serializer.data,
                # "merchant" : merchants,
                "PPOList" :objectLists        
            }

            return Response(res)


        except ValueError:
            raise InternalError()

    def counter(self):
        serializer=ChargesByPassSerializer(pass_event.objects.all())
        return serializer.data











class ChargesToBackend(generics.ListAPIView):
    serializer_class = ChargesToPassSerializer
    pagination_class=  None
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """

        try:
            # op1 = self.kwargs["op1"]
            op = self.kwargs["op"]
            startdate = self.kwargs["startdate"]
            enddate = self.kwargs["enddate"]
            startString = startdate[0:4] + startdate[4:6] + startdate[6:11] + " 00:00:00"
            finishString = enddate[0:4] + enddate[4:6] +  enddate[6:11] + " 23:59:59"

            check_dates(startdate,enddate)
            # startStrstartdateing = startdate[0:4] + "-" + startdate[4:6] + "-" + startdate[6:8] + " 00:00:00"
            # pro1= provider.objects.filter(provider_id=op1)
            # pro2= provider.objects.filter(provider_id=op2)
            queryset=pass_event.objects.all()

            # queryset=list(chain (pro1,pro2,query1 ))
            # queryset= pro1 | pro2 | query1
            return queryset
        
        except ValueError:
            raise InternalError()

    def list(self, request, *args, **kwargs):

        try:

            serializer = self.get_serializer(self.get_queryset(), many=True)

            try:
                serializer.data[0]
            except:
                raise NoData()


            newdata=serializer.data
            print(newdata)
            charges = [dict(item)['charge'] for item in newdata]

            numberPerOperator = {} 
            chargePerOperator = {}
            ##count
            for item in newdata:
                tagProvider=(dict(item)['stationRef'])[0:2]
                print(tagProvider)
                numberPerOperator[tagProvider]=0
                chargePerOperator[tagProvider]=0
            for item in newdata:
                tagProvider=(dict(item)['stationRef'])[0:2]
                charger=dict(item)['charge']
                numberPerOperator[tagProvider]=numberPerOperator[tagProvider]+1
                chargePerOperator[tagProvider]=chargePerOperator[tagProvider]+charger
            summer = sum(charges)
            counter= len(charges)
            mydatetime=datetime.now()
            timestamp=str(mydatetime)[:-7]
            objectLists=[]

            
            for (k,v), (k2,v2) in zip(numberPerOperator.items(), chargePerOperator.items()):
                print("MICROOOOOOOOOOOOOOOOOOOOOOOOOO")
                print(k)
                myprovider = provider.objects.get(provider_id=k)
                # print("MICROOOOOOOOOOOOOOOOOOOOOOOOOO")
                bidict={}
                bidict["VisitingOperator"]=myprovider.provider_id
                bidict["NumberOfPasses"] = v
                bidict["PassesCost"] = v2
                qdict = QueryDict("", mutable=True)
                qdict.update(bidict)
                objectLists.append(qdict)
            


            # change the data
            # serializer.data is the response that your serializer generates
            res = {
                "op_ID"    : self.kwargs["op"],
                "RequestTimestamp" : timestamp ,
                #"NumberOfPasses" : counter ,
                "PeriodFrom" : self.kwargs["startdate"]+" "+'00:00:00',
                "PeriodTo"  : self.kwargs["enddate"]+" "+'00:00:00',
                # "PassesList": serializer.data,
                # "merchant" : merchants,
                "PPOList" :objectLists        
            }

            return Response(res)


        except ValueError:
            raise InternalError()

    def counter(self):
        serializer=ChargesByPassSerializer(pass_event.objects.all())
        return serializer.data
