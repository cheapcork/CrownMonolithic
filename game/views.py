from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel, TransactionModel
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SessionGameSerializer, SessionLobbySerializer,\
	PlayerSerializer, ProducerSerializer,\
	BrokerFullSerializer, BrokerLittleSerializer, TransactionSerializer
from .permissions import IsInSessionOrAdmin
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import action
from game.services.players_finished import players_finished

from django.template import loader
from django.http import HttpResponse

def test_ws(request):
	template = loader.get_template('ws_test.html')
	return HttpResponse(template.render({}, request))

class SessionLobbyViewSet(ModelViewSet):
	queryset = SessionModel.objects.all()
	serializer_class = SessionLobbySerializer
	permission_classes = [IsAuthenticated]

	@action(methods=['put'], detail=True,
			url_path='start', url_name='session_start', permission_classes=[IsAdminUser])
	def start(self, request, pk):
		session_instance = self.get_queryset().get(pk=pk)
		serializer = self.serializer_class(
			session_instance,
			data={
				"name": session_instance.name,
				"turn_count": session_instance.turn_count,
				"status": "created",
			})
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save()
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.data, status=status.HTTP_200_OK)


class SessionGameViewSet(viewsets.GenericViewSet,
					mixins.RetrieveModelMixin):
	queryset = SessionModel.objects.all()
	serializer_class = SessionGameSerializer
	permission_classes = [IsInSessionOrAdmin]

	def get_serializer_context(self):
		context = super(SessionGameViewSet, self).get_serializer_context()
		context.update({'user': self.request.user})
		return context



class PlayerViewSet(viewsets.GenericViewSet,
					mixins.RetrieveModelMixin):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAuthenticated]


class PlayerListViewSet(viewsets.GenericViewSet,
					mixins.ListModelMixin):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAdminUser]

# TODO: For what is that?
class GetOrUpdatePlayerViewSet(mixins.ListModelMixin,
							   mixins.RetrieveModelMixin,
							   mixins.UpdateModelMixin,
							   viewsets.GenericViewSet):
	queryset = PlayerModel.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [IsAuthenticated]


# class ProducerViewSet(ModelViewSet):
# 	queryset = ProducerModel.objects.all()
# 	serializer_class = ProducerSerializer
# 	permission_classes = [IsAdminUser]


# class BrokerViewSet(ModelViewSet):
# 	queryset = BrokerModel.objects.all()
# 	serializer_class = BrokerSerializer
# 	permission_classes = [IsAdminUser]

"""
Транзакции
"""
class TransactionViewSet(viewsets.GenericViewSet,
						 mixins.CreateModelMixin,
						 mixins.UpdateModelMixin,
						 mixins.ListModelMixin):
	queryset = TransactionModel.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = [IsInSessionOrAdmin]

	@action(methods=['PUT'], detail=True,
			url_name='deny_transaction', permission_classes=[IsAuthenticated])
	def deny(self, request, pk):
		transaction_instance = self.get_queryset().get(pk=pk)
		# FIXME: Optimise me, please
		if not request.user.player.exists():
			return Response({'detail': 'You\'re not a player'},
							status=status.HTTP_400_BAD_REQUEST)
		player = request.user.player.get()
		if player.role == 'unassigned':
			return Response({'detail': 'You\'ve no role!'},
							status=status.HTTP_400_BAD_REQUEST)
		elif not ((
					player.role == 'producer' and
					transaction_instance.producer != player.producer
				) or (
					player.role == 'broker' and
 					transaction_instance.broker != player.broker
				)):
			return Response({'detail': 'That\'s not your transaction!'},
							status=status.HTTP_400_BAD_REQUEST)
		elif transaction_instance.status == 'denied':
			return Response({'detail': 'Transaction is already denied!'},
							status=status.HTTP_400_BAD_REQUEST)
		elif transaction_instance.status == 'accepted':
			return Response({'detail': 'Transaction is already accepted!'},
							status=status.HTTP_400_BAD_REQUEST)
		transaction_instance.status = 'denied'
		transaction_instance.save()
		return Response(status=status.HTTP_200_OK)

	@action(methods=['PUT'], detail=True,
			url_name='accept_transaction', permission_classes=[IsAuthenticated])
	def accept(self, request, pk):
		transaction_instance = self.get_queryset().get(pk=pk)
		# FIXME: Optimise me, please
		if not request.user.player.exists():
			return Response({'detail': 'You\'re not a player'},
							status=status.HTTP_400_BAD_REQUEST)
		player = request.user.player.get()
		if player.role == 'unassigned':
			return Response({'detail': 'You\'ve no role!'},
							status=status.HTTP_400_BAD_REQUEST)
		elif not ((
						  player.role == 'producer' and
						  transaction_instance.producer != player.producer
				  ) or (
						  player.role == 'broker' and
						  transaction_instance.broker != player.broker
				  )):
			return Response({'detail': 'That\'s not your transaction!'},
							status=status.HTTP_400_BAD_REQUEST)
		elif transaction_instance.status == 'denied':
			return Response({'detail': 'Transaction is already denied!'},
							status=status.HTTP_400_BAD_REQUEST)
		elif transaction_instance.status == 'accepted':
			return Response({'detail': 'Transaction is already accepted!'},
							status=status.HTTP_400_BAD_REQUEST)
		# TODO: вставить реаизацию сделки
		transaction_instance.status = 'accept'
		transaction_instance.save()
		print(transaction_instance.status)
		print('accept')
		return Response(status=status.HTTP_200_OK)


"""
Пересчет хода
"""
@api_view(['PUT'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def count_turn_view(request, pk):
	session_instance = get_object_or_404(SessionModel, pk=pk)
	if session_instance.status == 'initialized':
		return Response({'detail': 'Session is not started yet!'}, status=status.HTTP_400_BAD_REQUEST)
	if session_instance.status == 'finished':
		return Response({'detail': 'Session is already finished!'},status=status.HTTP_400_BAD_REQUEST)
	session_instance.save()
	print(SessionLobbySerializer(session_instance).data)
	return Response(status=status.HTTP_200_OK)


"""
Войти/выйти в сессию
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_session_view(request, session_pk):
	session_instance = get_object_or_404(SessionModel, pk=session_pk)
	try:
		player_instance = PlayerModel.objects.get(user=request.user.id)
		if player_instance.session.id == session_instance.id:
			return Response({
				'detail': 'You\'ve already joined this session!'
			}, status=status.HTTP_400_BAD_REQUEST)
		elif not player_instance.session.id == 0:
			return Response({
				'detail': 'You\'ve already joined another session!'
			}, status=status.HTTP_400_BAD_REQUEST)
	except PlayerModel.DoesNotExist:
		print(session_instance)
		player_serialized = PlayerSerializer(data={
			'nickname': request.user.username,
			'user': request.user.id,
			'session': session_instance.id,
		})
		if not player_serialized.is_valid():
			return Response(player_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
		player_instance = player_serialized.save()
		return Response(player_serialized.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_session_view(request, session_pk):
	session_instance = get_object_or_404(SessionModel, pk=session_pk)
	if not session_instance.player.filter(user=request.user.id).exists():
		return Response({
			'detail': 'You\'re not in this session!',
		}, status=status.HTTP_400_BAD_REQUEST)

	try:
		session_instance.player.get(user=request.user.id).delete()
	except Exception as e:
		# TODO: Exception handler
		return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	return Response(status=status.HTTP_204_NO_CONTENT)


"""
Конец хода
"""
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def end_turn(request):
	try:
		player = request.user.player.get()
	except PlayerModel.DoesNotExist:
		return Response({'detail': 'You\'re not in any session!'}, status=status.HTTP_400_BAD_REQUEST)

	if player.ended_turn:
		return Response({'detail': 'You\'ve already finished turn!'}, status=status.HTTP_400_BAD_REQUEST)
	player.ended_turn = True
	player.save()
	players_finished(player.session)
	return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancel_end_turn(request):
	try:
		player = request.user.player.get()
	except PlayerModel.DoesNotExist:
		return Response({'detail': 'You\'re not in any session!'}, status=status.HTTP_400_BAD_REQUEST)

	if not player.ended_turn:
		return Response({'detail': 'You\'ve not finished turn yet!'}, status=status.HTTP_400_BAD_REQUEST)
	player.ended_turn = False
	player.save()
	return Response(status=status.HTTP_200_OK)
