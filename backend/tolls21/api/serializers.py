from xmlrpc.client import DateTime
from rest_framework import serializers
from django.db.models import Avg, Count, Min, Sum
from rest_framework import pagination
from rest_framework.response import Response
from .models import *
from datetime import datetime

###for pagination purposes


def stringToDate(string):
    format = "%Y%m%d"

    start=datetime.strptime(string, format)
    return str(start)




def getOp1(string):
    return string[-25:-23]
def getOp1d(string):
    return string[-29:-27]
    
def getOp2(string):
    return string[-22:-20]
def getOp2d(string):
    return string[-26:-24]
    
    
def startdateFromString(string):
    return string[-19:-11] 
def startdateFromStringd(string):
    return string[-23:-13] 
    
def enddateFromString(string):
    return string[-10:-2] 
def enddateFromStringd(string):
    return string[-12:-2] 

class FilteredPassSerializer(serializers.ListSerializer):
    def to_representation(self,data):

        startdate = startdateFromString(str(self.context['request']))
        enddate = enddateFromString(str(self.context['request'])) 
        print(enddate)

        ##fix the date


        startString = stringToDate(startdate)
        finishString = stringToDate(enddate)
        
        # print(datetime.date(startdate))
        data = data.filter(timestamp__range=[startString, finishString])
    #    print(data

        return super(FilteredPassSerializer,  self).to_representation(data)


class PassSerializer(serializers.ModelSerializer):

    PassType= serializers.SerializerMethodField('get_passtype')
    TagProvider= serializers.SerializerMethodField('get_TagProvider')
    PassTimeStamp=serializers.SerializerMethodField('get_PassTimeStamp')

    PassIndex= serializers.SerializerMethodField('get_PassIndex')
    PassID= serializers.SerializerMethodField('get_PassID')
    VevicleID= serializers.SerializerMethodField('get_VevicleID')
    PassCharge= serializers.SerializerMethodField('get_PassCharge')

    class Meta:
        model=pass_event 
        list_serializer_class = FilteredPassSerializer
        fields=('PassIndex','PassID', 'PassTimeStamp', 'VevicleID','TagProvider','PassType','PassCharge')
        ordering = ['timestamp']



    def get_passtype(self, pass_event):
        vehiclepro=pass_event.vehicleRef.provider
        stationpro=pass_event.stationRef.provider

        if vehiclepro==stationpro:
            return "home"
        else:
            return "visitor"

    def get_TagProvider(self, pass_event) :
        vehiclepro=pass_event.vehicleRef.provider
        mypro=provider.objects.get(provider_id=vehiclepro.provider_id)

        return mypro.provider_id
    
    def get_PassTimeStamp(self, pass_event) :

        return str(pass_event.timestamp)[:19]



    def get_PassIndex(self, pass_event) :
        #TBD
        return -1

    def get_PassID(self, pass_event) :
        return pass_event.pass_id

    def get_VevicleID(self, pass_event) :
        return str(pass_event.vehicleRef)[-13:-1]

    def get_PassCharge(self, pass_event) :
        return pass_event.charge
        
    def get_Timestamp(self, pass_event) :
        
        return str(pass_event.timestamp)[0:19]




class StationSerializer(serializers.ModelSerializer):

    pass_event_set = PassSerializer(many=True,read_only=True)

    PeriodFrom= serializers.SerializerMethodField('get_startdate')

    PeriodTo= serializers.SerializerMethodField('get_enddate')

    RequestTimestamp= serializers.SerializerMethodField('get_timenow')

    # NumberOfPasses= serializers.SerializerMethodField('get_countpass')

    class Meta:
        model = station
        fields=  ("station_id", "station_name", "provider","RequestTimestamp","PeriodFrom","PeriodTo","pass_event_set")

    def get_timenow(self, station):
        mydatetime=datetime.now()
        return str(mydatetime)[:-7]

    def get_startdate(self, station):

        startdate = startdateFromString(str(self.context['request']))
        return startdate

    def get_enddate(self,station):

        enddate = enddateFromString(str(self.context['request'])) 
        return enddate


    















from xmlrpc.client import DateTime
from rest_framework import serializers
from .models import *
from datetime import datetime

class AnalysisFilteredPassSerializer(serializers.ListSerializer):
    def to_representation(self,data):

        

        startdate = startdateFromString(str(self.context['request']))
        enddate = enddateFromString(str(self.context['request'])) 


        op2=getOp2(str(self.context['request']))#[-26:-24]
        op1=getOp1(str(self.context['request']))#[-29:-27]



        ##fix the date

        startString = stringToDate(startdate)
        finishString = stringToDate(enddate)
        # print(datetime.date(startdate))
        data = data.filter(timestamp__range=[startString, finishString],vehicleRef__provider=op1,stationRef__provider=op2)
    #    print(data)

        return super(AnalysisFilteredPassSerializer,  self).to_representation(data)


class AnalysisPassSerializer(serializers.ModelSerializer):

    TimeStamp=serializers.SerializerMethodField('get_PassTimeStamp')

    PassIndex= serializers.SerializerMethodField('get_PassIndex')
    PassID= serializers.SerializerMethodField('get_PassID')
    VevicleID= serializers.SerializerMethodField('get_VevicleID')
    Charge= serializers.SerializerMethodField('get_PassCharge')
    StationID= serializers.SerializerMethodField('get_StationID')


    class Meta:
        model=pass_event 
        list_serializer_class = AnalysisFilteredPassSerializer
        fields=('PassIndex','PassID','StationID', 'TimeStamp', 'VevicleID','Charge')

    def get_passtype(self, pass_event):
        vehiclepro=pass_event.vehicleRef.provider
        stationpro=pass_event.stationRef.provider

        if vehiclepro==stationpro:
            return "home"
        else:
            return "visitor"

    def get_TagProvider(self, pass_event) :
        vehiclepro=pass_event.vehicleRef.provider
        mypro=provider.objects.get(provider_id=vehiclepro.provider_id)

        return mypro.provider_id
    
    def get_PassTimeStamp(self, pass_event) :

        return str(pass_event.timestamp)[:19]



    def get_PassIndex(self, pass_event) :
        #TBD
        return -1

    def get_PassID(self, pass_event) :
        return pass_event.pass_id

    def get_StationID(self, pass_event) :
        return str(pass_event.vehicleRef)[-13:-1]

    def get_VevicleID(self, pass_event) :
        return str(pass_event.vehicleRef)[-13:-1]

    def get_PassCharge(self, pass_event) :
        return pass_event.charge




class AnalysisStationSerializer(serializers.ModelSerializer):


    pass_event_set = AnalysisPassSerializer(many=True,read_only=True)

    RequestTimestamp= serializers.SerializerMethodField('get_timenow')

    class Meta:

        model = pass_event
        fields=  ("pass_event_set","RequestTimestamp")

    

    def get_timenow(self, station):
        mydatetime=datetime.now()

        return str(mydatetime)[:-7]
    



















### 3 











# class ChargesByFilteredPassSerializer(serializers.ListSerializer):
#     def to_representation(self,data):

        
#         startdate = str(self.context['request'])[-12:-2]  


#         print( "request is ",str(self.context['request'])[-12:-2])
#         # .GET.get('startdate')
#         enddate = str(self.context['request'])[-23:-13]
#         op2=str(self.context['request'])[-26:-24]
#         op1=str(self.context['request'])[-29:-27]

#         print("op1 =",op1, "op2=", op2)

#         print(enddate)

#         ##fix the date
#         startString = startdate[0:4] + startdate[4:6] + startdate[6:11] + " 00:00:00"
#         finishString = enddate[0:4] + enddate[4:6] +  enddate[6:11] + " 23:59:59"
#         # print(datetime.date(startdate))
#         data = data.filter(timestamp__range=[startString, finishString],vehicleRef__provider=op1,stationRef__provider=op2)
#     #    print(data)
#         data=data.annotate(average_rating=Avg('charge') )

#         return super(ChargesByFilteredPassSerializer,  self).to_representation(data)


# class ChargesByPassSerializer(serializers.ModelSerializer):

#     Passtype= serializers.SerializerMethodField('get_passtype')
#     TagProvider= serializers.SerializerMethodField('get_TagProvider')


#     class Meta:
#         model=pass_event 
#         list_serializer_class = ChargesByFilteredPassSerializer
#         fields=('pass_id', 'timestamp', 'vehicleRef',"charge",'Passtype','TagProvider','stationRef','charge')

#     def get_passtype(self, pass_event):
#         vehiclepro=pass_event.vehicleRef.provider
#         stationpro=pass_event.stationRef.provider

#         if vehiclepro==stationpro:
#             return "home"
#         else:
#             return "visitor"

#     def get_TagProvider(self, pass_event) :
#         vehiclepro=pass_event.vehicleRef.provider
#         mypro=provider.objects.get(provider_id=vehiclepro.provider_id)

#         return mypro.fullname





# class ChargesByStationSerializer(serializers.ModelSerializer):


#     pass_event_set = AnalysisPassSerializer(many=True,read_only=True)

#     RequestTimestamp= serializers.SerializerMethodField('get_timenow')

#     class Meta:

#         model = pass_event
#         fields=  ("pass_event_set","RequestTimestamp")

    

#     def get_timenow(self, station):
#         mydatetime=datetime.now()

#         return str(mydatetime)[:-7]










#### 4


class ChargesToFilteredPassSerializer(serializers.ListSerializer):
    def to_representation(self,data):

        
        startdate = startdateFromString(str(self.context['request']))
        enddate = enddateFromString(str(self.context['request'])) 

        op=getOp2(str(self.context['request']))#[-26:-24]
        # print("op1 =",op1, "op2=", op2)

        print(enddate)

        ##fix the date

        startString = stringToDate(startdate)
        finishString = stringToDate(enddate)
        # print(datetime.date(startdate))
        data = data.filter(timestamp__range=[startString, finishString],vehicleRef__provider=op)
        #exclude the passes of tags of op1 in stations of
        data=data.exclude(stationRef__provider=op)  
    #    print(data)

        return super(ChargesToFilteredPassSerializer,  self).to_representation(data)



class ChargesToPassSerializer(serializers.ModelSerializer):

    Passtype= serializers.SerializerMethodField('get_passtype')
    TagProvider= serializers.SerializerMethodField('get_TagProvider')


    class Meta:
        model=pass_event 
        list_serializer_class = ChargesToFilteredPassSerializer
        fields=('pass_id', 'timestamp', 'vehicleRef',"charge",'Passtype','TagProvider','stationRef','charge')

    def get_passtype(self, pass_event):
        vehiclepro=pass_event.vehicleRef.provider
        stationpro=pass_event.stationRef.provider

        if vehiclepro==stationpro:
            return "home"
        else:
            return "visitor"

    def get_TagProvider(self, pass_event) :
        vehiclepro=pass_event.vehicleRef.provider
        mypro=provider.objects.get(provider_id=vehiclepro.provider_id)

        return mypro.fullname




class ChargesToStationSerializer(serializers.ModelSerializer):


    pass_event_set = AnalysisPassSerializer(many=True,read_only=True)

    RequestTimestamp= serializers.SerializerMethodField('get_timenow')

    class Meta:

        model = pass_event
        fields=  ("pass_event_set","RequestTimestamp")

    

    def get_timenow(self, station):
        mydatetime=datetime.now()

        return str(mydatetime)[:-7]











###csv file serializer



class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)






# class CustomFailStatusSerializer(serializers.Serializer):
#     failed= serializers.















class ChargesByFilteredPassSerializer(serializers.ListSerializer):
    def to_representation(self,data):

        
        
        startdate = startdateFromString(str(self.context['request']))
        enddate = enddateFromString(str(self.context['request'])) 

        op=getOp2(str(self.context['request']))#[-26:-24]
        # print("op1 =",op1, "op2=", op2)

        print(enddate)

        ##fix the date
        startString = stringToDate(startdate)
        finishString = stringToDate(enddate)
        # print(datetime.date(startdate))
        data = data.filter(timestamp__range=[startString, finishString],stationRef__provider=op)
        #exclude the passes of tags of op1 in stations of
        data=data.exclude(vehicleRef__provider=op)  
    #    print(data)

        return super(ChargesByFilteredPassSerializer,  self).to_representation(data)

class ChargesByPassSerializer(serializers.ModelSerializer):

    Passtype= serializers.SerializerMethodField('get_passtype')
    TagProvider= serializers.SerializerMethodField('get_TagProvider')


    class Meta:
        model=pass_event 
        list_serializer_class = ChargesByFilteredPassSerializer
        fields=('pass_id', 'timestamp', 'vehicleRef',"charge",'Passtype','TagProvider','stationRef','charge')

    def get_passtype(self, pass_event):
        vehiclepro=pass_event.vehicleRef.provider
        stationpro=pass_event.stationRef.provider

        if vehiclepro==stationpro:
            return "home"
        else:
            return "visitor"

    def get_TagProvider(self, pass_event) :
        vehiclepro=pass_event.vehicleRef.provider
        mypro=provider.objects.get(provider_id=vehiclepro.provider_id)

        return mypro.fullname




class ChargesByStationSerializer(serializers.ModelSerializer):


    pass_event_set = AnalysisPassSerializer(many=True,read_only=True)

    RequestTimestamp= serializers.SerializerMethodField('get_timenow')

    class Meta:

        model = pass_event
        fields=  ("pass_event_set","RequestTimestamp")

    

    def get_timenow(self, station):
        mydatetime=datetime.now()

        return str(mydatetime)[:-7]


