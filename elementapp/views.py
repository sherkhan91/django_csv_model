from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import information
from .serializers import information_serializer
from .csv_to_model import main


# Create your views here.

def index(request):
    return HttpResponse("Greetings! Welcome to the elements assignment for candidate Sher Khan Mari")

@api_view(['GET'])
def getinformation(request):
    """ this functions lists all the information available in db """
    all_information_objects = information.objects.all()
    serializer =  information_serializer(all_information_objects, many=True)
    return JsonResponse ({'message':serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getinformationbyid(request,pk):
    """ check if incoming argument is a valid number """
    """ by default Django handle pk very well and does not let go through but still we added check """
    if str(type(pk))=="<class 'int'>":
        pkid = pk 
    else:
        return JsonResponse ({'message':'Sorry unsupported argument type'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if information.objects.filter(id=pkid).exists():
        all_information_objects = information.objects.get(id=pkid)
        serializer =  information_serializer(all_information_objects)
        return JsonResponse ({'message':serializer.data}, status=status.HTTP_200_OK)
    else:
        return JsonResponse ({'message':'Sorry, the provided id is invalid!'}, status=status.HTTP_404_NOT_FOUND)
    

""" this functions needs to be called one time and then it periodically runs automatically and save data in db """
@api_view(['GET'])
def readinformation(request):
    main()
    return JsonResponse ({'message':'reading information has been triggered!'}, status=status.HTTP_200_OK)
    