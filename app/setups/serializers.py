from rest_framework import serializers

from .models import Setup


class SetupSerializer(serializers.ModelSerializer):
    """Serializer for Setup object"""

    class Meta:
        model = Setup
        fields = ('scheduled_time',)
        read_only_fields = ('scheduled_time',)

    def create(self, validated_data):
        user = self.context['request'].user
        hour = self.context['view'].kwargs.get('hour')
        obj, created = Setup.objects.get_or_create(user=user, scheduled_time=int(hour))

        return obj
