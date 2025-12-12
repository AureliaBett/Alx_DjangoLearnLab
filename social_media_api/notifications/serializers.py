from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'recipient_username',
            'actor',
            'actor_username',
            'verb',
            'target_type',
            'target_content_type',
            'target_object_id',
            'timestamp',
            'read'
        ]

    def get_target_type(self, obj):
        """
        Returns the model name of the target object for easy display
        """
        if obj.target:
            return obj.target._meta.model_name
        return None
