from rest_framework import serializers
from .models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели TelegramUser.
    Преобразует объекты модели в JSON и обратно.
    """
    
    class Meta:
        model = TelegramUser
        fields = [
            'id',
            'user_id', 
            'username',
            'first_name',
            'last_name',
            'created_at',
            'last_activity',
            'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'last_activity']
    
    def validate_user_id(self, value):
        """Валидация user_id"""
        if value <= 0:
            raise serializers.ValidationError("user_id должен быть положительным числом")
        return value
    
    def create(self, validated_data):
        """Создание нового пользователя"""
        user_id = validated_data.get('user_id')
        
        # Проверяем, существует ли пользователь с таким user_id
        existing_user = TelegramUser.objects.filter(user_id=user_id).first()
        if existing_user:
            # Если пользователь существует, обновляем его данные
            for attr, value in validated_data.items():
                setattr(existing_user, attr, value)
            existing_user.save()
            return existing_user
        
        # Если пользователь не существует, создаем нового
        return TelegramUser.objects.create(**validated_data)