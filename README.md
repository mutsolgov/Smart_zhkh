# Smart ЖКХ - Ezdel

# 🏠 Smart ЖКХ

Smart ЖКХ — веб-приложение для управления ЖКХ-сервисами: лицевыми счетами, начислениями, платежами и авторизацией пользователей с поддержкой OAuth2 / OpenID Connect.

## 🚀 Стек технологий

- Django 5
- Django REST Framework (DRF)
- PostgreSQL
- OIDC Provider (встроенный)
- Docker + Docker Compose
- Gunicorn (продакшн-сервер)

---

## 📦 Установка и запуск (через Docker)

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/mutsolgov/Smart_zhkh.git
cd smartzhkh
```


2. Создайте файл .env 


3. Сделайте скрипт entrypoint.sh исполняемым
```bash
chmod +x entrypoint.sh
```
⚠️ Этот шаг обязателен, иначе контейнер не запустится (ошибка: permission denied).

1. Соберите и запустите проект
```bash
docker compose up --build
```


📥 Доступ к админке
Перейдите на http://localhost:8000/admin/


