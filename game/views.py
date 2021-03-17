from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SessionSerializer, PlayerSerializer, ProducerSerializer, BrokerSerializer
from game.services.db_logic_interface import change_game_parameters


class SessionViewSet(ModelViewSet):
	queryset = SessionModel.objects.all()
	serializer_class = SessionSerializer
	permission_classes = [IsAdminUser]


# class SessionListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
# 	queryset = Session.objects.all()
# 	serializer_class = SessionSerializer
# 	permission_classes = [IsAuthenticated]


class PlayerViewSet(ModelViewSet):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAdminUser]


class GetOrUpdatePlayerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
																				viewsets.GenericViewSet):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAuthenticated]


class ProducerViewSet(ModelViewSet):
	queryset = ProducerModel.objects.all()
	serializer_class = ProducerSerializer
	permission_classes = [IsAdminUser]


class BrokerViewSet(ModelViewSet):
	queryset = BrokerModel.objects.all()
	serializer_class = BrokerSerializer
	permission_classes = [IsAdminUser]
