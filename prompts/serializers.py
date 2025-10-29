from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Prompt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        
        return data

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = '__all__'
        read_only_fields = ('id', 'created')

class PromptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ('username', 'title', 'tagline', 'text', 'model', 'image')
