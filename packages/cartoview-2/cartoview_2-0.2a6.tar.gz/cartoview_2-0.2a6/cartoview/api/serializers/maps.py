import json

from rest_framework import serializers

from cartoview.maps.models import Map

from .base_resource import BaseModelSerializer


class CenterField(serializers.CharField):

    def to_representation(self, value):
        data = None
        data = json.loads(value)
        return data

    def to_internal_value(self, data):
        if isinstance(data, list):
            return json.dumps(data)
        return data


class MapSerializer(BaseModelSerializer):
    center = CenterField()
    owner = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Map
        fields = '__all__'
