# -*- coding: utf-8 -*-
"""
Скрипт для виправлення даних
Запуск: python manage.py shell < fix_data.py
"""

from datetime import date, timedelta
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

from users.models import User
from employees.models import Employee, FixedSalaryStrategy, BonusSalaryStrategy
from requests.models import Request, PendingState, ApprovedState, RejectedState
from notifications.models import Notification

print("Виправлення даних...")

# 1. Стани заявок
pending_state, _ = PendingState.objects.get_or_create(pk=1)
approved_state, _ = ApprovedState.objects.get_or_create(pk=1)
rejected_state, _ = RejectedState.objects.get_or_create(pk=1)
print("Стани OK")

# 2. Стратегії зарплати
fixed_strategy, _ = FixedSalaryStrategy.objects.get_or_create(
    pk=1,
    defaults={'monthly_amount': Decimal('25000.00')}
)
bonus_strategy, _ = BonusSalaryStrategy.objects.get_or_create(
    pk=1,
    defaults={'base_salary': Decimal('20000.00'), 'bonus_percentage': Decimal('15.00')}
)
print("Стратегії OK")

# 3. ContentType для стратегій
fixed_ct = ContentType.objects.get_for_model(FixedSalaryStrategy)
bonus_ct = ContentType.objects.get_for_model(BonusSalaryStrategy)
pending_ct = ContentType.objects.get_for_model(PendingState)
approved_ct = ContentType.objects.get_for_model(ApprovedState)

# 4. Прив'язати стратегію до співробітників
for emp in Employee.objects.all():
    if not emp.salary_strategy_type:
        emp.salary_strategy_type = fixed_ct
        emp.salary_strategy_id = fixed_strategy.id
        emp.save()
        print(f"  Прив'язано стратегію до {emp.first_name} {emp.last_name}")

# 5. Видалити старі сповіщення з кракозябрами
Notification.objects.all().delete()
print("Старі сповіщення видалено")

# 6. Створити нове сповіщення
emp_maria = Employee.objects.filter(email='maria@test.com').first()
if emp_maria:
    Notification.objects.create(
        recipient=emp_maria,
        notification_type='system',
        message='Ласкаво просимо до HRM System!',
        is_sent=True
    )
    print("Нове сповіщення створено")

# 7. Створити тестові заявки якщо немає
if Request.objects.count() == 0:
    if emp_maria:
        Request.objects.create(
            employee=emp_maria,
            request_type='vacation',
            reason='Simeinyi obstavyny',
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=14),
            current_state_type=pending_ct,
            current_state_id=pending_state.id
        )
        print("Заявка створена")

print("\n" + "="*50)
print("ГОТОВО!")
print("="*50)
