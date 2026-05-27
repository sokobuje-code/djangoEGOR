Проект Django — учебный пример

Как запустить локально:

1. Создайте виртуальное окружение и активируйте его (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Установите зависимости:

```powershell
pip install -r requirements.txt
```

3. Примените миграции и создайте суперпользователя:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Запустите сервер разработки:

```powershell
python manage.py runserver
```

Админ-панель: http://127.0.0.1:8000/admin/
