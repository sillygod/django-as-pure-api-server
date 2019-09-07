from rest_framework import serializers
from .models import Message
from rest_framework.relations import RelatedField


# TODO: implement show the reply
class MessageSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()

    class Meta:

        model = Message
        fields = (
            'id',
            'user',
            'message',
            'replies',
            'created_at',
        )

    def get_replies(self, message):
        return message.replies.values()


class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:

        model = Message
        fields = (
            'message',
            'created_at',
        )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    """
    message = serializers.CharField(max_length=1024,
                                    error_messages={
                                        'blank':
                                        'a blank message is not allowed',
                                        'max_length':
                                        'exceed the maximum length',
                                    })

    class Meta:

        model = Message
        fields = ('message', )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = Message.objects.create(**validated_data)
        return instance


class MessageReplySerializer(serializers.ModelSerializer):

    ""
    ""

    message = serializers.CharField(max_length=1024,
                                    error_messages={
                                        'blank':
                                        'a blank message is not allowed',
                                        'max_length':
                                        'exceed the maximum length',
                                    })

    class Meta:

        model = Message
        fields = ('subject', 'message')

    def validate(self, attrs):
        kwargs = self.context['kwargs']
        value = kwargs['pk']
        if not Message.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                'this message subject does not exist')

        attrs['subject'] = Message.objects.get(id=value)
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = Message.objects.create(**validated_data)
        return instance
