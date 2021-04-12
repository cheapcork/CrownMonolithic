# from rest_framework import serializers
# from CrownMonolithic.utils import get_player_model
#
#
# class PlayerWithTokenSerializer(serializers.ModelSerializer):
#     nickname = serializers.CharField(max_length=100)
#     auth_token = serializers.CharField(source='token.key', max_length=100, read_only=True)
#
#     class Meta:
#         model = get_player_model()
#         fields = [
#             'id',
#             'nickname',
#             'session',
#             'auth_token',
#         ]
#
#
# class PlayerSerializer(serializers.ModelSerializer):
#     nickname = serializers.CharField(max_length=100)
#
#     class Meta:
#         model = get_player_model()
#         fields = [
#             'id',
#             'nickname',
#             'session',
#         ]
