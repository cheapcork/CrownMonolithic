from rest_framework import serializers

from authorization.models import TokenModel


class TokenSerializer(serializers.ModelSerializer):
	class Meta:
		model = TokenModel
		fields = '__all__'
		read_only = '__all__'
