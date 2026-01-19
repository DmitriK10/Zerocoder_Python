from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError

from .models import TelegramUser
from .serializers import TelegramUserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Регистрация нового пользователя Telegram.
    
    Принимает POST запрос с JSON телом:
    {
        "user_id": 123456789,
        "username": "example",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    Возвращает:
    - 201 Created: если пользователь успешно создан
    - 200 OK: если пользователь уже существует (обновляются данные)
    - 400 Bad Request: если данные невалидны
    """
    try:
        # Получаем данные из запроса
        data = request.data
        
        # Проверяем обязательное поле user_id
        if 'user_id' not in data:
            return Response(
                {'error': 'Поле user_id обязательно'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаем или обновляем пользователя
        user, created = TelegramUser.objects.update_or_create(
            user_id=data['user_id'],
            defaults={
                'username': data.get('username', ''),
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'is_active': True
            }
        )
        
        # Сериализуем данные пользователя
        serializer = TelegramUserSerializer(user)
        
        if created:
            # Пользователь создан
            return Response(
                {
                    'status': 'success',
                    'message': 'Пользователь успешно зарегистрирован',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            # Пользователь обновлен
            return Response(
                {
                    'status': 'success',
                    'message': 'Данные пользователя обновлены',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
            
    except ValidationError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Внутренняя ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_info(request, user_id):
    """
    Получение информации о пользователе по его user_id.
    
    Возвращает:
    - 200 OK: если пользователь найден
    - 404 Not Found: если пользователь не найден
    """
    try:
        user = TelegramUser.objects.get(user_id=user_id, is_active=True)
        serializer = TelegramUserSerializer(user)
        
        return Response(
            {
                'status': 'success',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except TelegramUser.DoesNotExist:
        return Response(
            {
                'status': 'error',
                'message': 'Пользователь не найден'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {
                'status': 'error',
                'message': f'Внутренняя ошибка сервера: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users(request):
    """
    Получение списка всех зарегистрированных пользователей.
    
    Возвращает:
    - 200 OK: список пользователей
    """
    try:
        users = TelegramUser.objects.filter(is_active=True).order_by('-created_at')
        serializer = TelegramUserSerializer(users, many=True)
        
        return Response(
            {
                'status': 'success',
                'count': len(serializer.data),
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {
                'status': 'error',
                'message': f'Внутренняя ошибка сервера: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request, user_id):
    """
    Удаление пользователя по его user_id.
    
    Возвращает:
    - 200 OK: если пользователь успешно удален
    - 404 Not Found: если пользователь не найден
    """
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        user.delete()
        
        return Response(
            {
                'status': 'success',
                'message': 'Пользователь успешно удален'
            },
            status=status.HTTP_200_OK
        )
        
    except TelegramUser.DoesNotExist:
        return Response(
            {
                'status': 'error',
                'message': 'Пользователь не найден'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {
                'status': 'error',
                'message': f'Внутренняя ошибка сервера: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )