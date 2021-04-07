from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from .models import SessionModel, PlayerModel, ProducerModel, TransactionModel, BrokerModel
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SessionGameSerializer, SessionLobbySerializer, PlayerSerializer, SessionListSerializer, \
	TransactionSerializer, UserSerializer, ProducerSerializer, BrokerSerializer
from .permissions import IsInSession, IsThePlayer
from rest_framework.decorators import action
from game.services.normal.data_access.count_session import change_phase, start_session, count_session, create_player

from django.template import loader
from django.http import HttpResponse


# Декоратор @action. Дефолтные значениея:
# methods - GET
# url_path - НАЗВАНИЕ_МЕТОДА
# url_name - НАЗВАНИЕ-МЕТОДА
# detail - None; обязательное поле; устанавливает, применяется ли роут для retrieve (True) или list (False)

class SessionAdminViewSet(ModelViewSet):
	"""
	Обрабатывает сессии для администраторов
	"""
	queryset = SessionModel.objects.all()
	serializer_class = SessionLobbySerializer
	permission_classes = [IsAdminUser]

	@action(methods=['GET'], detail=True, url_path='start-session', permission_classes=[])
	def start_session(self, request, pk):
		"""
		Создаёт новую сессию
		"""
		session = SessionModel.objects.get(pk=pk)
		start_session(session)
		return Response({'detail': 'Session started'}, status=status.HTTP_200_OK)

	@action(methods=['GET', 'PUT'], detail=True, url_path='set-turn-phase', permission_classes=[])
	def set_turn_phase(self, request, pk):
		"""
		Устанавливает фазу хода в сессии
		"""
		session = SessionModel.objects.get(pk=pk)
		phase = request.data.get('phase')
		change_phase(session, phase)
		return Response({'detail': 'Phase updated'}, status=status.HTTP_200_OK)

	@action(methods=['GET'], detail=True, renderer_classes=[JSONRenderer], url_path='count-session', permission_classes=[])
	def count_session(self, request, pk):
		"""
		Запускает пересчёт хода
		"""
		session_instance = SessionModel.objects.get(pk=pk)
		if session_instance.status == 'initialized':
			return Response({'detail': 'Session is not started yet!'}, status=status.HTTP_400_BAD_REQUEST)
		if session_instance.status == 'finished':
			return Response({'detail': 'Session is already finished!'}, status=status.HTTP_400_BAD_REQUEST)
		count_session(session_instance)
		return Response({'detail': 'Session counted'}, status=status.HTTP_200_OK)


class SessionViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
	"""
	ViewSet для пользователей
	"""
	queryset = SessionModel.objects.all()
	serializer_class = SessionGameSerializer
	permission_classes = [IsAuthenticated]

	# def get_serializer_context(self):
	# 	"""
	# 	Передаёт сериализатору модель пользователя
	# 	"""
	# 	context = super(SessionViewSet, self).get_serializer_context()
	# 	context.update({'user': self.request.user})
	# 	return context
	#
	# def list(self, request, *args, **kwargs):
	# 	"""
	# 	?????????????????
	# 	"""
	# 	queryset = self.get_queryset().filter(status='initialized')
	# 	serializer = SessionListSerializer(queryset, many=True)
	# 	return Response(serializer.data, status=status.HTTP_200_OK)
	#
	# @action(detail=True)
	# def is_started(self, request, session_pk):
	# 	"""
	# 	Возвращает True если сессия запущена
	# 	"""
	# 	try:
	# 		is_started = self.queryset.get(pk=session_pk).status == 'started'
	# 	except SessionModel.DoesNotExist:
	# 		return Response({'detail': 'Session doesn\'t exist!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	return Response({'is_started': is_started}, status=status.HTTP_200_OK)


class PlayerViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsInSession]

	# @action(detail=True)
	# def get_self_user(self, request):
	# 	"""
	# 	Возвращает данные о пользователе, с которым связан игрок
	# 	"""
	# 	return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
	#
	# @action(methods=['PUT'], detail=True, permission_classes=[IsInSession])
	# def end_turn(self, request):
	# 	try:
	# 		player = request.user.player.get()
	# 	except PlayerModel.DoesNotExist:
	# 		return Response({'detail': 'You\'re not in any session!'}, status=status.HTTP_400_BAD_REQUEST)
	#
	# 	if player.ended_turn:
	# 		return Response({'detail': 'You\'ve already finished turn!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	player.ended_turn = True
	# 	player.save()
	# 	# finish_by_players(player.session)
	# 	return Response(status=status.HTTP_200_OK)
	#
	# @action(methods=['PUT'], detail=True, permission_classes=IsInSession)
	# def cancel_end_turn(self, request):
	# 	try:
	# 		player = request.user.player.get()
	# 	except PlayerModel.DoesNotExist:
	# 		return Response({'detail': 'You\'re not in any session!'}, status=status.HTTP_400_BAD_REQUEST)
	#
	# 	if not player.ended_turn:
	# 		return Response({'detail': 'You\'ve not finished turn yet!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	player.ended_turn = False
	# 	player.save()
	# 	return Response(status=status.HTTP_200_OK)
	#
	# @action(methods=['DELETE'], detail=True, permission_classes=[IsInSession])
	# def leave_session(self, request):
	# 	try:
	# 		request.user.player.get().delete()
	# 		return Response(status=status.HTTP_204_NO_CONTENT)
	# 	except PlayerModel.DoesNotExist:
	# 		return Response({'detail': 'You are not in any session!'}, status=status.HTTP_400_BAD_REQUEST)


class ProducerViewSet(ModelViewSet):
	queryset = ProducerModel.objects.all()
	serializer_class = ProducerSerializer
	permission_classes = [IsInSession]

	# @action(methods=['POST'], detail=True, permission_classes=[IsThePlayer])
	# def produce(self, request):
	# 	"""
	# 	Отправляет запрос на производство
	# 	"""
	# 	try:
	# 		producer = ProducerModel.objects.get(player=request.user.player.get())
	# 	except PlayerModel.DoesNotExist:
	# 		return Response({'detail': 'You are not in session!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	except ProducerModel.DoesNotExist:
	# 		return Response({'detail': 'You are not a producer!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	# if producer.player.session.turn
	# 	if producer.billets_produced != 0:
	# 		return Response({'detail': 'You\'ve already produced at this turn'}, status=status.HTTP_400_BAD_REQUEST)
	# 	producer.billets_produced = request.data['produce']
	# 	producer.save()
	# 	return Response(status=status.HTTP_201_CREATED)


class BrokerViewSet(ModelViewSet):
	queryset = BrokerModel.objects.all()
	serializer_class = BrokerSerializer
	permission_classes = [IsInSession]

	# @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
	# def deny_transaction(self, request, pk):
	# 	transaction_instance = self.queryset.get(pk=pk)
	# 	# FIXME: Optimise me, please
	# 	if not request.user.player.exists():
	# 		return Response({'detail': 'You\'re not a player'}, status=status.HTTP_400_BAD_REQUEST)
	# 	player = request.user.player.get()
	# 	if not ((
	# 					player.role == 'producer' and
	# 					transaction_instance.producer != player.producer
	# 			) or (
	# 					player.role == 'broker' and
	# 					transaction_instance.broker != player.broker
	# 			)):
	# 		return Response({'detail': 'That\'s not your transaction!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	elif transaction_instance.status == 'denied':
	# 		return Response({'detail': 'Transaction is already denied!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	elif transaction_instance.status == 'accepted':
	# 		return Response({'detail': 'Transaction is already accepted!'}, status=status.HTTP_400_BAD_REQUEST)
	# 	transaction_instance.status = 'denied'
	# 	transaction_instance.save()
	# 	return Response(status=status.HTTP_200_OK)
	#
	# # Наследуются ли permission_classes от ViewSet к @action?
	# @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
	# def accept_transaction(self, request, pk):
	# 	transaction_instance = self.queryset.get(pk=pk)
	# 	# FIXME: Optimise me, please
	# 	if not request.user.player.exists():
	# 		return Response({'detail': 'You\'re not a player'},
	# 						status=status.HTTP_400_BAD_REQUEST)
	# 	player = request.user.player.get()
	# 	if player.role == 'unassigned':
	# 		return Response({'detail': 'You\'ve no role!'},
	# 						status=status.HTTP_400_BAD_REQUEST)
	# 	elif not ((
	# 					  player.role == 'producer' and
	# 					  transaction_instance.producer != player.producer
	# 			  ) or (
	# 					  player.role == 'broker' and
	# 					  transaction_instance.broker != player.broker
	# 			  )):
	# 		return Response({'detail': 'That\'s not your transaction!'},
	# 						status=status.HTTP_400_BAD_REQUEST)
	# 	elif transaction_instance.status == 'denied':
	# 		return Response({'detail': 'Transaction is already denied!'},
	# 						status=status.HTTP_400_BAD_REQUEST)
	# 	elif transaction_instance.status == 'accepted':
	# 		return Response({'detail': 'Transaction is already accepted!'},
	# 						status=status.HTTP_400_BAD_REQUEST)
	# 	transaction_instance.status = 'accept'
	# 	transaction_instance.save()
	# 	return Response(status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
						 mixins.ListModelMixin):
	queryset = TransactionModel.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = [IsInSession]


class LobbyViewSet(viewsets.GenericViewSet):
	queryset = SessionModel.objects.all()
	serializer_class = SessionLobbySerializer

	@action(methods=['post'], detail=True, url_path='join')
	def join_session(self, request, session_id):
		session_instance = SessionModel.objects.get(id=session_id)
		nickname = request.data.get('nickname')
		create_player(session_instance, nickname)
		return Response({'detail': 'Player successfully created'}, status=status.HTTP_201_CREATED)

	@action(methods=['delete'], detail=True, url_path='leave')
	def leave_session(self, request):
		pass


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def join_session_view(request, session_pk):
# 	session_instance = get_object_or_404(SessionModel, pk=session_pk)
# 	try:
# 		player_instance = PlayerModel.objects.get(user=request.user)
# 	except PlayerModel.DoesNotExist:
# 		if not session_instance.status == 'initialized':
# 			return Response({'detail': 'Session is started or finished!'}, status=status.HTTP_400_BAD_REQUEST)
# 		print(session_instance)
# 		player_serialized = PlayerSerializer(data={
# 			'nickname': request.user.username,
# 			'user': request.user.id,
# 			'session': session_instance.id,
# 		})
# 		if not player_serialized.is_valid():
# 			return Response(player_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
# 		player_serialized.save()
# 		try:
# 			create_session(session_instance)
# 		except Exception:
# 			pass
# 		return Response(player_serialized.data, status=status.HTTP_200_OK)
