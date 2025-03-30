from rest_framework import serializers
from .models import User ,UserInfo, ScoreMatchResult

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # ✅ Hash password
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ScoreMatchResultSerializer(serializers.ModelSerializer):
    candidate = UserSerializer(read_only=True)  # Nested candidate details
    expert = UserSerializer(read_only=True)  # Nested expert details

    class Meta:
        model = ScoreMatchResult
        fields = ['id', 'candidate', 'expert', 'education_score', 'skills_score', 'experience_score', 'project_score', 'total_score', 'created_at']