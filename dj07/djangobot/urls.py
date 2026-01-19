from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import json

def home_view(request):
    """Домашняя страница с информацией об API"""
    if request.method == 'GET':
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Django + Telegram Bot API</title>
            <meta charset="UTF-8">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .api-endpoint {
                    background: #f8f9fa;
                    border-left: 4px solid #007bff;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 5px;
                }
                .method {
                    display: inline-block;
                    padding: 5px 10px;
                    color: white;
                    border-radius: 3px;
                    font-weight: bold;
                    margin-right: 10px;
                }
                .post { background: #28a745; }
                .get { background: #007bff; }
                .url {
                    font-family: monospace;
                    color: #495057;
                }
                .status {
                    float: right;
                    padding: 3px 8px;
                    background: #6c757d;
                    color: white;
                    border-radius: 3px;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Django + Telegram Bot API</h1>
                <p>Проект демонстрирует интеграцию Django REST API с Telegram-ботом.</p>
                
                <h2>📡 Доступные API эндпоинты:</h2>
                
                <div class="api-endpoint">
                    <span class="method post">POST</span>
                    <span class="url">/api/register/</span>
                    <span class="status">201 Created</span>
                    <p>Регистрация нового пользователя Telegram. Принимает JSON с user_id и username.</p>
                </div>
                
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="url">/api/user/{id}/</span>
                    <span class="status">200 OK</span>
                    <p>Получение информации о пользователе по его ID.</p>
                </div>
                
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="url">/api/users/</span>
                    <span class="status">200 OK</span>
                    <p>Получение списка всех зарегистрированных пользователей.</p>
                </div>
                
                <h2>🔗 Быстрые ссылки:</h2>
                <ul>
                    <li><a href="/api/users/">Просмотр всех пользователей</a></li>
                    <li><a href="/admin/">Административная панель Django</a></li>
                    <li><a href="https://core.telegram.org/bots/api">Telegram Bot API</a></li>
                </ul>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_content)
    return HttpResponse(status=405)

def api_info(request):
    """Информация об API в JSON формате"""
    api_info = {
        "project": "Django + Telegram Bot Integration",
        "version": "1.0.0",
        "endpoints": {
            "register": {
                "method": "POST",
                "url": "/api/register/",
                "description": "Register a new Telegram user",
                "request_body": {
                    "user_id": "integer (required)",
                    "username": "string (optional)"
                }
            },
            "get_user": {
                "method": "GET",
                "url": "/api/user/{id}/",
                "description": "Get user information by ID"
            },
            "get_users": {
                "method": "GET",
                "url": "/api/users/",
                "description": "Get all registered users"
            }
        },
        "telegram_bot": {
            "commands": ["/start", "/myinfo", "/help"]
        }
    }
    return HttpResponse(json.dumps(api_info, indent=2), content_type="application/json")

urlpatterns = [
    path('', home_view, name='home'),
    path('api-info/', api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/', include('bot.urls')),
]