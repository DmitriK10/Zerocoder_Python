from django.test import TestCase, Client as TestClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from django.core import mail
from django.test import override_settings
from django.core.management import call_command
from io import StringIO
from .models import Client, Task, MoodEntry, Goal

User = get_user_model()

class MoodEntryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.client_user = TestClient()
        self.client_user.login(username='testuser', password='12345')
        self.client_obj = Client.objects.create(user=self.user, name='Иван Петров')

    def test_add_mood_entry(self):
        # Создаём POST-запрос на добавление отметки
        response = self.client_user.post(
            reverse('core:mood_add', args=[self.client_obj.pk]),
            {
                'date': date.today().isoformat(),
                'mood_score': 8,
                'notes': 'Хорошее настроение'
            }
        )
        # Проверяем редирект на страницу клиента
        self.assertRedirects(response, reverse('core:client_detail', args=[self.client_obj.pk]))
        # Проверяем, что отметка создана
        self.assertTrue(MoodEntry.objects.filter(client=self.client_obj, date=date.today()).exists())

    def test_mood_entry_protected(self):
        # Неавторизованный пользователь не должен иметь доступа
        self.client_user.logout()
        response = self.client_user.post(
            reverse('core:mood_add', args=[self.client_obj.pk]),
            {'date': date.today().isoformat(), 'mood_score': 5}
        )
        # Должен быть редирект на логин
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)


class ClientDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.client_user = TestClient()
        self.client_user.login(username='testuser', password='12345')
        self.client_obj = Client.objects.create(user=self.user, name='Иван Петров')

        # Создаём несколько задач
        Task.objects.create(user=self.user, client=self.client_obj, title='Задача 1', due_date=timezone.now() + timedelta(days=1), completed=True)
        Task.objects.create(user=self.user, client=self.client_obj, title='Задача 2', due_date=timezone.now() + timedelta(days=2), completed=False)
        Task.objects.create(user=self.user, client=self.client_obj, title='Задача 3', due_date=timezone.now() - timedelta(days=1), completed=False)

        # Создаём несколько отметок настроения
        MoodEntry.objects.create(client=self.client_obj, date=date.today() - timedelta(days=1), mood_score=7)
        MoodEntry.objects.create(client=self.client_obj, date=date.today() - timedelta(days=2), mood_score=6)

    def test_client_detail_view_status(self):
        response = self.client_user.get(reverse('core:client_detail', args=[self.client_obj.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иван Петров')

    def test_client_detail_progress(self):
        response = self.client_user.get(reverse('core:client_detail', args=[self.client_obj.pk]))
        # Всего задач 3, выполнена 1
        self.assertEqual(response.context['total_tasks'], 3)
        self.assertEqual(response.context['completed_tasks'], 1)
        self.assertEqual(response.context['task_progress_percent'], 33)  # 1/3 = 33.33 -> int

    def test_client_detail_mood_data(self):
        response = self.client_user.get(reverse('core:client_detail', args=[self.client_obj.pk]))
        mood_data = response.context['mood_data']
        self.assertEqual(len(mood_data), 2)  # две отметки
        # Проверяем, что данные отсортированы по дате
        self.assertEqual(mood_data[0]['date'].isoformat(), (date.today() - timedelta(days=2)).isoformat())
        self.assertEqual(mood_data[1]['date'].isoformat(), (date.today() - timedelta(days=1)).isoformat())


class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='12345', email='testuser2@example.com')
        self.client.login(username='testuser2', password='12345')
        self.client_obj = Client.objects.create(user=self.user, name='Клиент для теста')
        # Проверим, что настройки созданы и по умолчанию включены
        self.assertIsNotNone(self.user.notification_settings)
        self.assertTrue(self.user.notification_settings.receive_emails)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_task_creation_sends_email(self):
        # Создаём задачу с датой в будущем
        future_date = timezone.now() + timedelta(days=1)
        response = self.client.post(reverse('core:task_create'), {
            'client': self.client_obj.pk,
            'title': 'Тестовая задача',
            'description': 'Описание',
            'due_date': future_date.strftime('%Y-%m-%d %H:%M:%S'),
            'priority': 'medium',
        })
        self.assertEqual(response.status_code, 302)  # redirect
        # Проверяем, что письмо отправлено
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Тестовая задача', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to[0], self.user.email)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_task_creation_no_email_for_past_date(self):
        # Создаём задачу с датой в прошлом
        past_date = timezone.now() - timedelta(days=1)
        response = self.client.post(reverse('core:task_create'), {
            'client': self.client_obj.pk,
            'title': 'Просроченная задача',
            'description': 'Описание',
            'due_date': past_date.strftime('%Y-%m-%d %H:%M:%S'),
            'priority': 'medium',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_task_creation_respects_user_settings(self):
        # Отключаем уведомления для пользователя
        settings = self.user.notification_settings
        settings.receive_emails = False
        settings.save()

        future_date = timezone.now() + timedelta(days=1)
        response = self.client.post(reverse('core:task_create'), {
            'client': self.client_obj.pk,
            'title': 'Задача без уведомления',
            'description': 'Описание',
            'due_date': future_date.strftime('%Y-%m-%d %H:%M:%S'),
            'priority': 'medium',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)


class GoalTests(TestCase):
    """Тесты для функциональности целей клиента"""

    def setUp(self):
        self.user = User.objects.create_user(username='goaluser', password='12345', email='goaluser@example.com')
        self.client_user = TestClient()
        self.client_user.login(username='goaluser', password='12345')
        self.client_obj = Client.objects.create(user=self.user, name='Клиент с целями')

    def test_goal_creation(self):
        """Проверка создания цели через ORM"""
        goal = Goal.objects.create(
            client=self.client_obj,
            title='Тестовая цель',
            description='Описание цели',
            target_date=date.today() + timedelta(days=30)
        )
        self.assertEqual(goal.title, 'Тестовая цель')
        self.assertEqual(goal.client, self.client_obj)
        self.assertEqual(goal.target_date, date.today() + timedelta(days=30))

    def test_goal_create_view(self):
        """Проверка представления создания цели"""
        response = self.client_user.post(
            reverse('core:goal_create', args=[self.client_obj.pk]),
            {
                'title': 'Новая цель',
                'description': 'Описание',
                'target_date': (date.today() + timedelta(days=10)).isoformat()
            }
        )
        # Должен быть редирект на страницу клиента
        self.assertRedirects(response, reverse('core:client_detail', args=[self.client_obj.pk]))
        # Проверяем, что цель создана
        self.assertTrue(Goal.objects.filter(title='Новая цель', client=self.client_obj).exists())

    def test_goal_update_view(self):
        """Проверка представления редактирования цели"""
        goal = Goal.objects.create(client=self.client_obj, title='Старая цель')
        response = self.client_user.post(
            reverse('core:goal_update', args=[goal.pk]),
            {
                'title': 'Обновлённая цель',
                'description': 'Новое описание',
                'target_date': (date.today() + timedelta(days=20)).isoformat()
            }
        )
        self.assertRedirects(response, reverse('core:client_detail', args=[self.client_obj.pk]))
        goal.refresh_from_db()
        self.assertEqual(goal.title, 'Обновлённая цель')
        self.assertEqual(goal.description, 'Новое описание')
        self.assertEqual(goal.target_date, date.today() + timedelta(days=20))

    def test_goal_delete_view(self):
        """Проверка представления удаления цели"""
        goal = Goal.objects.create(client=self.client_obj, title='Цель для удаления')
        response = self.client_user.post(reverse('core:goal_delete', args=[goal.pk]))
        self.assertRedirects(response, reverse('core:client_detail', args=[self.client_obj.pk]))
        self.assertFalse(Goal.objects.filter(pk=goal.pk).exists())

    def test_goal_progress_calculation(self):
        """Проверка расчёта прогресса цели (процент выполненных задач)"""
        goal = Goal.objects.create(client=self.client_obj, title='Цель с задачами')
        # Создаём задачи, привязанные к цели
        Task.objects.create(
            user=self.user,
            client=self.client_obj,
            goal=goal,
            title='Задача 1',
            due_date=timezone.now() + timedelta(days=1),
            completed=True
        )
        Task.objects.create(
            user=self.user,
            client=self.client_obj,
            goal=goal,
            title='Задача 2',
            due_date=timezone.now() + timedelta(days=2),
            completed=False
        )
        # Прогресс должен быть 50% (1 из 2)
        # Получаем страницу клиента, где в контексте есть цели с вычисленным progress_percent
        response = self.client_user.get(reverse('core:client_detail', args=[self.client_obj.pk]))
        goals_in_context = response.context['goals']
        self.assertEqual(len(goals_in_context), 1)
        self.assertEqual(goals_in_context[0].progress_percent, 50)

    def test_goal_access_control(self):
        """Проверка, что пользователь не может видеть/редактировать чужие цели"""
        other_user = User.objects.create_user(username='other', password='12345', email='other@example.com')
        other_client = Client.objects.create(user=other_user, name='Чужой клиент')
        other_goal = Goal.objects.create(client=other_client, title='Чужая цель')

        # Попытка получить страницу редактирования чужой цели
        response = self.client_user.get(reverse('core:goal_update', args=[other_goal.pk]))
        # Должен быть 404, так как в get_queryset фильтруется по client__user
        self.assertEqual(response.status_code, 404)

        # Попытка удалить чужую цель
        response = self.client_user.post(reverse('core:goal_delete', args=[other_goal.pk]))
        self.assertEqual(response.status_code, 404)

        # Проверка, что цель не исчезла
        self.assertTrue(Goal.objects.filter(pk=other_goal.pk).exists())


class ReminderCommandTests(TestCase):
    """Тесты для команды периодических напоминаний"""

    def setUp(self):
        self.user = User.objects.create_user(username='reminderuser', password='12345', email='reminder@example.com')
        self.client_obj = Client.objects.create(user=self.user, name='Клиент для напоминаний')
        # Включаем уведомления
        self.user.notification_settings.receive_emails = True
        self.user.notification_settings.save()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reminder_sent_for_task_due_in_one_hour(self):
        # Создаём задачу с due_date через 59 минут (попадает в интервал)
        due = timezone.now() + timedelta(minutes=59)
        task = Task.objects.create(
            user=self.user,
            client=self.client_obj,
            title='Тестовая задача',
            due_date=due,
            completed=False,
            reminder_sent=False
        )
        out = StringIO()
        call_command('send_task_reminders', stdout=out)
        self.assertIn('Successfully sent 1 reminders', out.getvalue())
        task.refresh_from_db()
        self.assertTrue(task.reminder_sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Напоминание', mail.outbox[0].subject)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reminder_not_sent_if_already_sent(self):
        due = timezone.now() + timedelta(minutes=59)
        task = Task.objects.create(
            user=self.user,
            client=self.client_obj,
            title='Тест',
            due_date=due,
            completed=False,
            reminder_sent=True
        )
        out = StringIO()
        call_command('send_task_reminders', stdout=out)
        self.assertIn('Successfully sent 0 reminders', out.getvalue())
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reminder_not_sent_if_user_disabled(self):
        self.user.notification_settings.receive_emails = False
        self.user.notification_settings.save()
        due = timezone.now() + timedelta(minutes=59)
        task = Task.objects.create(
            user=self.user,
            client=self.client_obj,
            title='Тест',
            due_date=due,
            completed=False,
            reminder_sent=False
        )
        out = StringIO()
        call_command('send_task_reminders', stdout=out)
        self.assertIn('Successfully sent 0 reminders', out.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        task.refresh_from_db()
        self.assertFalse(task.reminder_sent)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reminder_not_sent_for_past_task(self):
        # Задача с due_date в прошлом не должна подхватываться
        due = timezone.now() - timedelta(minutes=30)
        task = Task.objects.create(
            user=self.user,
            client=self.client_obj,
            title='Просроченная',
            due_date=due,
            completed=False,
            reminder_sent=False
        )
        out = StringIO()
        call_command('send_task_reminders', stdout=out)
        self.assertIn('Successfully sent 0 reminders', out.getvalue())
        self.assertEqual(len(mail.outbox), 0)