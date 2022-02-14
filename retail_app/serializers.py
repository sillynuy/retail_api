from rest_framework import serializers
from retail_app.models import Store


class StoreSerializerListed(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ['product']


class StoreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    store_name = serializers.CharField()
    remains = serializers.StringRelatedField(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
