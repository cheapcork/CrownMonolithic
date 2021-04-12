from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import SessionModel, PlayerModel, ProducerModel, TransactionModel, \
	BrokerModel
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import serializers
from .permissions import IsInSession, IsThePlayer
from rest_framework.decorators import action
from game.services.normal.data_access.count_session import change_phase, \
	start_session, count_session
from authorization.services.create_player import create_player
from authorization.permissions import IsPlayer
from authorization.serializers import PlayerWithTokenSerializer

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
	serializer_class = serializers.SessionAdminSerializer
	permission_classes = [IsAdminUser]

	@action(methods=['GET'], detail=True, url_path='start-session', permission_classes=[])
	def start_session(self, request, pk):
		"""
		Создаёт новую сессию
		"""
		session = SessionModel.objects.get(pk=pk)
		start_session(session)
		return Response({'detail': 'Session started'}, status=status.HTTP_200_OK)

	@action(methods=['PUT'], detail=True, url_path='set-turn-phase', permission_classes=[])
	def set_turn_phase(self, request, pk):
		"""
		Устанавливает фазу хода в сессии
		"""
		session = SessionModel.objects.get(pk=pk)
		phase = request.data.get('phase')
		change_phase(session, phase)
		return Response({'detail': 'Phase updated'}, status=status.HTTP_200_OK)

	@action(methods=['GET'], detail=True, renderer_classes=[JSONRenderer], url_path='count-session',
			permission_classes=[])
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


class LobbyViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
	"""
	Для просмотра списка лобби и операциями с единичным лобби
	"""
	queryset = SessionModel.objects.all()
	serializer_class = serializers.LobbySerializer

	# permission_classes = [IsAuthenticated]

	def list(self, request, *args, **kwargs):
		"""
		Выдаёт список с созданными администратором сессиями
		"""
		queryset = self.get_queryset().filter(status='initialized')
		serializer = serializers.LobbySerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def retrieve(self, request, *args, **kwargs):
		"""
		Выдаёт информацию о конкретном лобби
		"""
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		players_in_lobby = PlayerModel.objects.filter(session_id=instance.id)
		return Response(
			{
				'lobby': serializer.data,
				'players': serializers.PlayerSerializer(players_in_lobby, many=True).data
			},
			status=status.HTTP_200_OK
		)

	@action(methods=['post'], detail=True, url_path='join')
	def join_session(self, request, pk):
		"""
		Даёт игроку авторизоваться и присоединиться к сессии
		"""
		if hasattr(request, 'player'):
			return Response({'detail': 'You\'re already a player!'},
							status=status.HTTP_400_BAD_REQUEST)

		try:
			session = SessionModel.objects.get(id=pk)
			assert session.status == 'initialized'
			nickname = request.data.get('nickname')
			player = create_player(session, nickname)
			return Response(PlayerWithTokenSerializer(player).data,
							status=status.HTTP_201_CREATED)
		except SessionModel.DoesNotExist:
			return Response({'detail': 'No such session!'},
							status=status.HTTP_400_BAD_REQUEST)
		except AssertionError:
			return Response({'detail': 'Session is already started!'},
							status=status.HTTP_400_BAD_REQUEST)


	@action(methods=['delete'], detail=True, url_path='leave',
			permission_classes=[IsPlayer])
	def leave_session(self, request, pk):
		"""
		Выкидывает игрока из сессии
		"""
		try:
			session_instance = SessionModel.objects.get(pk=pk)
			assert request.player.session.id == session_instance.id, "Вы не в той сессии"
			request.player.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		except SessionModel.DoesNotExist:
			return Response({'detail': 'No such session'},
							status=status.HTTP_400_BAD_REQUEST)
		except AssertionError:
			return Response({'detail': 'You\'re not in this session'},
							status=status.HTTP_400_BAD_REQUEST)

class PlayerViewSet(viewsets.ModelViewSet):
	queryset = PlayerModel.objects.all()
	serializer_class = serializers.PlayerSerializer

	@action(methods=['GET'], permission_classes=[IsPlayer],	detail=False)
	def me(self, request):
		print(self.get_serializer(), type(request.player))
		return Response(self.get_serializer(request.player).data,
						status=status.HTTP_200_OK)


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
	serializer_class = serializers.ProducerSerializer
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
	serializer_class = serializers.BrokerSerializer
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
	serializer_class = serializers.TransactionSerializer
	permission_classes = [IsInSession]

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
