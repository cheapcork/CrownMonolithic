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
from game.services.normal.data_access.count_session import change_phase, start_session, count_session, create_player, \
	produce_billets, send_trade, cancel_trade, end_turn, cancel_end_turn, accept_transaction, deny_transaction

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
		session_instance = SessionModel.objects.get(pk=pk)
		assert session_instance.status == 'initialized'
		nickname = request.data.get('nickname')
		# FIXME ????????????????????????
		create_player(session_instance, nickname)
		return Response(
			{
				'detail': f'Player {nickname} successfully created',
				'player': serializers.PlayerSerializer(PlayerModel.objects.get(session_id=pk, nickname=nickname)).data},
			status=status.HTTP_201_CREATED
		)

	@action(methods=['delete'], detail=True, url_path='leave')
	def leave_session(self, request, pk):
		"""
		Выкидывает игрока из сессии
		"""
		session_instance = SessionModel.objects.get(pk=pk)
		player_id = request.data.get('id')
		player = PlayerModel.objects.get(pk=player_id, session_id=pk)
		assert player.session.id == session_instance.id, "Вы не в той сессии"
		player.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class PlayerViewSet(viewsets.ModelViewSet):
	queryset = PlayerModel.objects.all()
	serializer_class = serializers.PlayerSerializer


class ProducerViewSet(ModelViewSet):
	queryset = ProducerModel.objects.all()
	serializer_class = serializers.ProducerSerializer

	@action(methods=['POST'], detail=True)
	def produce(self, request, pk):
		"""
		Отправляет запрос на производство заготовок
		"""
		producer = ProducerModel.objects.get(player_id=pk)
		quantity = request.data.get('quantity')
		produce_billets(producer, quantity)
		return Response(
			{
				'detail': f'Произведено {quantity} заготовок для производителя {producer.player.nickname}.',
				'stash': serializers.ProducerSerializer(producer).data
			},
			status=status.HTTP_200_OK
		)

	@action(methods=['POST'], detail=True)
	def trade(self, request, pk):
		"""
		Отправляет маклеру предложение о сделке
		"""
		producer = ProducerModel.objects.get(id=pk)
		broker = BrokerModel.objects.get(id=request.data.get('broker'))
		terms = request.data.get('terms')
		send_trade(producer, broker, terms)
		return Response(
			{
				'detail': f'Отправлена сделка от {producer.player.nickname} к {broker.player.nickname}',
				'terms': terms
			},
			status=status.HTTP_201_CREATED
		)

	@action(methods=['delete'], detail=True, url_path='cancel-trade')
	def cancel_trade(self, request, pk):
		"""
		Отменяет сделку с маклером
		"""
		producer = ProducerModel.objects.get(id=pk)
		broker = BrokerModel.objects.get(id=request.data.get('broker'))
		cancel_trade(producer, broker)
		return Response(
			{
				'detail': f'Сделка между {producer.player.nickname} и {broker.player.nickname} отменена'
			},
			status=status.HTTP_204_NO_CONTENT
		)

	@action(detail=True)
	def me(self, request, pk):
		"""
		Отправляет полные данные о текущем игроке
		"""
		producer = ProducerModel.objects.get(pk=pk)
		return Response(
			serializers.FullProducerInfoSerializer(producer).data,
			status=status.HTTP_200_OK
		)

	@action(methods=['put'], detail=True, url_path='end-turn')
	def end_turn(self, request, pk):
		"""
		Завершает ход
		"""
		player = ProducerModel.objects.get(id=pk).player
		end_turn(player)
		return Response(
			{
				'detail': f'Игрок {player.nickname} завершил ход',
			},
			status=status.HTTP_200_OK
		)

	@action(methods=['put'], detail=True, url_path='cancel-end-turn')
	def cancel_end_turn(self, request, pk):
		"""
		Отменяет завершение хода
		"""
		player = ProducerModel.objects.get(id=pk).player
		cancel_end_turn(player)
		return Response(
			{
				'detail': f'Игрок {player.nickname} отменил завершение хода'
			},
			status=status.HTTP_200_OK
		)

	@action(detail=True, url_path='balance-detail')
	def balance_detail(self, request, pk):
		"""
		Показывает детализацию баланса за предыдущий ход
		"""
		pass

	@action(detail=True, url_path='balance-history')
	def balance_history(self, request, pk):
		"""
		Показывает детализацию баланса за игру
		"""
		pass

	@action(methods=[''], detail=True, url_path='accept-show-balace')
	def accept_show_balance(self, request, pk):
		"""
		Подтверждает показ баланса маклеру
		"""
		pass

	@action(methods=[''], detail=True, url_path='deny-show-balance')
	def deny_show_balance(self, request, pk):
		"""
		Отклоняет запрос на показ баланса
		"""
		pass


class BrokerViewSet(ModelViewSet):
	queryset = BrokerModel.objects.all()
	serializer_class = serializers.BrokerSerializer

	# permission_classes = [IsInSession]

	@action(detail=True)
	def me(self, request, pk):
		"""
		Отправляет полные данные о текущем игроке
		"""
		broker = BrokerModel.objects.get(id=pk)
		return Response(
			serializers.BrokerSerializer(broker).data,
			status=status.HTTP_200_OK
		)

	@action(methods=['put'], detail=True, url_path='accept')
	def accept_transaction(self, request, pk):
		"""
		Одобряет сделку с производителем
		"""
		producer = ProducerModel.objects.get(request.data.get('producer'))
		broker = BrokerModel.objects.get(id=pk)
		accept_transaction(producer, broker)
		return Response(
			{
				'detail': f'Маклер {broker.player.nickname} одобрил сделку с {producer.player.nickname}'
			},
			status=status.HTTP_200_OK
		)

	@action(methods=['put'], detail=True, url_path='deny')
	def deny_transaction(self, request, pk):
		"""
		Отклоняет сделку с производителем
		"""
		producer = ProducerModel.objects.get(request.data.get('producer'))
		broker = BrokerModel.objects.get(id=pk)
		deny_transaction(producer, broker)
		return Response(
			{
				'detail': f'Маклер {broker.player.nickname} отклонил сделку с {producer.player.nickname}'
			},
			status=status.HTTP_200_OK
		)

	@action(methods=['put'], detail=True, url_path='end-turn')
	def end_turn(self, request, pk):
		"""
		Завершает ход
		"""
		player = BrokerModel.objects.get(pk=pk).player
		end_turn(player)
		return Response(
			{
				'detail': f'Игрок {player.nickname} завершил ход',
			},
			status=status.HTTP_200_OK
		)

	@action(methods=['put'], detail=True, url_path='cancel-end-turn')
	def cancel_end_turn(self, request, pk):
		"""
		Отменяет завершение хода
		"""
		player = BrokerModel.objects.get(pk=pk).player
		cancel_end_turn(player)
		return Response(
			{
				'detail': f'Игрок {player.nickname} отменил завершение хода'
			},
			status=status.HTTP_200_OK
		)

	@action(methods=['get'], detail=True, url_path='request-balance')
	def request_balance(self, request, pk):
		"""
		Запрашивает баланс производителя
		"""
		pass


class TransactionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
						 mixins.ListModelMixin):
	queryset = TransactionModel.objects.all()
	serializer_class = serializers.TransactionSerializer
	permission_classes = [IsInSession]
