"""
Скрипт для наповнення бази тестовими даними
Запуск: python manage.py shell < populate_db.py
Або: python manage.py shell, потім exec(open('populate_db.py').read())
"""

from datetime import date, timedelta
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

from users.models import User
from employees.models import Employee, FixedSalaryStrategy, BonusSalaryStrategy
from requests.models import Request, PendingState, ApprovedState, RejectedState
from notifications.models import Notification
from timetracking.models import TimeRecord
from documents.models import Contract, LeaveRequest

print("Створення тестових даних...")

# 1. Створення станів заявок
pending_state, _ = PendingState.objects.get_or_create(pk=1)
approved_state, _ = ApprovedState.objects.get_or_create(pk=1)
rejected_state, _ = RejectedState.objects.get_or_create(pk=1)
print("Стани заявок створено")

# 2. Створення стратегій зарплати
fixed_strategy, _ = FixedSalaryStrategy.objects.get_or_create(
    pk=1,
    defaults={'monthly_amount': Decimal('25000.00')}
)
bonus_strategy, _ = BonusSalaryStrategy.objects.get_or_create(
    pk=1,
    defaults={'base_salary': Decimal('20000.00'), 'bonus_percentage': Decimal('15.00')}
)
print("Стратегії зарплати створено")

# 3. Створення користувачів
user_maria, created = User.objects.get_or_create(
    username='maria',
    defaults={
        'email': 'maria@test.com',
        'role': 'employee',
        'first_name': 'Марія',
        'last_name': 'Іваненко'
    }
)
if created:
    user_maria.set_password('admin123')
    user_maria.save()

user_olga, created = User.objects.get_or_create(
    username='olga_hr',
    defaults={
        'email': 'olga@test.com',
        'role': 'hr',
        'first_name': 'Ольга',
        'last_name': 'Петренко'
    }
)
if created:
    user_olga.set_password('admin123')
    user_olga.save()

user_ivan, created = User.objects.get_or_create(
    username='ivan',
    defaults={
        'email': 'ivan@test.com',
        'role': 'employee',
        'first_name': 'Іван',
        'last_name': 'Сидоренко'
    }
)
if created:
    user_ivan.set_password('admin123')
    user_ivan.save()

print("Користувачів створено")

# 4. Створення співробітників
fixed_ct = ContentType.objects.get_for_model(FixedSalaryStrategy)
bonus_ct = ContentType.objects.get_for_model(BonusSalaryStrategy)

emp_maria, _ = Employee.objects.get_or_create(
    email='maria@test.com',
    defaults={
        'first_name': 'Марія',
        'last_name': 'Іваненко',
        'phone': '+380501234567',
        'position': 'Розробник',
        'department': 'IT',
        'hire_date': date(2023, 1, 15),
        'salary_strategy_type': fixed_ct,
        'salary_strategy_id': fixed_strategy.id
    }
)

emp_olga, _ = Employee.objects.get_or_create(
    email='olga@test.com',
    defaults={
        'first_name': 'Ольга',
        'last_name': 'Петренко',
        'phone': '+380502345678',
        'position': 'HR Менеджер',
        'department': 'HR',
        'hire_date': date(2022, 6, 1),
        'salary_strategy_type': bonus_ct,
        'salary_strategy_id': bonus_strategy.id
    }
)

emp_ivan, _ = Employee.objects.get_or_create(
    email='ivan@test.com',
    defaults={
        'first_name': 'Іван',
        'last_name': 'Сидоренко',
        'phone': '+380503456789',
        'position': 'Дизайнер',
        'department': 'Design',
        'hire_date': date(2023, 3, 20),
        'salary_strategy_type': fixed_ct,
        'salary_strategy_id': fixed_strategy.id
    }
)

print("Співробітників створено")

# 5. Створення тестових заявок
pending_ct = ContentType.objects.get_for_model(PendingState)
approved_ct = ContentType.objects.get_for_model(ApprovedState)

if Request.objects.count() == 0:
    Request.objects.create(
        employee=emp_maria,
        request_type='vacation',
        reason='Сімейні обставини',
        start_date=date.today() + timedelta(days=7),
        end_date=date.today() + timedelta(days=14),
        current_state_type=pending_ct,
        current_state_id=pending_state.id
    )
    
    Request.objects.create(
        employee=emp_ivan,
        request_type='sick',
        reason='Застуда',
        start_date=date.today() - timedelta(days=2),
        end_date=date.today(),
        current_state_type=approved_ct,
        current_state_id=approved_state.id
    )
    print("Заявки створено")

# 6. Створення тестових сповіщень
if Notification.objects.count() == 0:
    Notification.objects.create(
        recipient=emp_maria,
        notification_type='system',
        message='Ласкаво просимо до HRM System!',
        is_sent=True
    )
    print("Сповіщення створено")

print("\n" + "="*50)
print("ГОТОВО! Тестові дані створено.")
print("="*50)
print("\nТестові акаунти:")
print("  Співробітник: maria / admin123")
print("  HR Менеджер:  olga_hr / admin123")
print("  Співробітник: ivan / admin123")
print("="*50)
