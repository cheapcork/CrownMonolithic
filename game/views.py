from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets
from .models import Session, Player, Producer, Broker
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SessionSerializer, PlayerSerializer, ProducerSerializer, BrokerSerializer


class SessionViewSet(ModelViewSet):
	queryset = Session.objects.all()
	serializer_class = SessionSerializer
	permission_classes = [IsAdminUser]


class PlayerViewSet(ModelViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAdminUser]


class GetOrUpdatePlayerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
																				viewsets.GenericViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAuthenticated]


class ProducerViewSet(ModelViewSet):
	queryset = Producer.objects.all()
	serializer_class = ProducerSerializer
	permission_classes = [IsAdminUser]


class BrokerViewSet(ModelViewSet):
	queryset = Broker.objects.all()
	serializer_class = BrokerSerializer
	permission_classes = [IsAdminUser]
