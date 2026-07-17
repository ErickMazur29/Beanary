from rest_framework import serializers
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    can_allow = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'phone', 'max_loan_allowed', 'can_allow']

    def get_can_allow(self, obj):
        return obj.can_allow

    def get_name(self, obj):
        return obj.user.username

    def validate_can_allow(self, value):
        if value <= 0:
            raise serializers.ValidationError("Você atingiu o limite de livros para alugar.")
        return value
