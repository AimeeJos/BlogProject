from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer

from django.http import JsonResponse

from base.models import Room


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET/api',
        'GET/api/rooms',
        'GET/api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):

    rooms=Room.objects.all() #python objects
    serializer = RoomSerializer(rooms,many=True) #multiple objects many true

    return Response(serializer.data)              # python object cannot be passed
                                        # thus serializer is used.


@api_view(['GET'])
def getRoom(request,pk):
    room=Room.objects.get(id=pk) #python object
    serializer = RoomSerializer(room, many=False) #single object many false

    return Response(serializer.data)              # python object cannot be passed
                                        # thus serializer is used.


