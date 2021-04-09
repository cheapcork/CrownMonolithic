from django.shortcuts import render
from .serializers import PlayerWithTokenSerializer, PlayerCreateSerializer,\
    PlayerSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsPlayer
from django.conf import settings


@api_view(['POST'])
def create_player(request):
    if hasattr(request, 'player'):
        return Response({'detail': 'You\'re already a player!'},
                        status=status.HTTP_400_BAD_REQUEST)
    player_serializer = PlayerCreateSerializer(data=request.data)
    if not player_serializer.is_valid():
        return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(player_serializer.save(), status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsPlayer])
def me(request):
    return Response(PlayerSerializer(request.player).data, status=status.HTTP_200_OK)
