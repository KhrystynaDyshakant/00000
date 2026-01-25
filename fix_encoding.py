# -*- coding: utf-8 -*-
"""
Виправлення кодування
python manage.py shell
exec(open('fix_encoding.py', encoding='utf-8').read())
"""

from employees.models import Employee

# Виправити Івана Сидоренка
ivan = Employee.objects.filter(email='ivan@test.com').first()
if ivan:
    ivan.first_name = 'Іван'
    ivan.last_name = 'Сидоренко'
    ivan.save()
    print(f"Виправлено: {ivan.first_name} {ivan.last_name}")

# Перевірити всіх
for emp in Employee.objects.all():
    print(f"  - {emp.first_name} {emp.last_name} ({emp.email})")

print("\nГотово!")
