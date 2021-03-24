from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from .models import SessionModel, PlayerModel, ProducerModel, BrokerModel, TransactionModel
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SessionSerializer, PlayerSerializer, ProducerSerializer, BrokerSerializer, \
	TransactionSerializer
from django.views.decorators.http import require_http_methods


class SessionViewSet(ModelViewSet):
	queryset = SessionModel.objects.all()
	serializer_class = SessionSerializer
	permission_classes = [IsAdminUser]


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


class TransactionViewSet(ModelViewSet):
	queryset = TransactionModel.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = [IsAdminUser]


@api_view(['PUT'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def count_turn_view(request, pk):
	session_instance = get_object_or_404(SessionModel, pk=pk)
	if request.method == 'PUT':
		session_instance.save()
		return Response(status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def join_session_view(request, session_pk):
	session_instance = get_object_or_404(SessionModel, pk=session_pk)
	if session_instance.player.filter(user=request.user.id).exists():
		return Response({
			'error': 'You\'ve already joined this session!',
			'players': PlayerSerializer(session_instance.player, many=True).data,
		}, status=status.HTTP_400_BAD_REQUEST)

	player_serialized = PlayerSerializer(data={
		'nickname': request.user.username,
		'user': request.user.id,
		'session': session_instance.id,
	})

	if not player_serialized.is_valid():
		return Response(player_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
	player_serialized.save()

	return Response(PlayerSerializer(session_instance.player, many=True).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def leave_session_view(request, session_pk):
	session_instance = get_object_or_404(SessionModel, pk=session_pk)
	if not session_instance.player.filter(user=request.user.id).exists():
		return Response({
			'error': 'You\'re not in this session!',
			'players': PlayerSerializer(session_instance.player, many=True).data,
		}, status=status.HTTP_400_BAD_REQUEST)

	try:
		session_instance.player.get(user=request.user.id).delete()
	except Exception as e:
		# TODO: Exception handler
		print(e)
		return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	return Response(status=status.HTTP_204_NO_CONTENT)

