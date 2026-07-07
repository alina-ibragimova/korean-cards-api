# Korean Cards API

Бэкенд для изучения корейских слов с использованием алгоритма интервального повторения (SM-2).

## Возможности

- Регистрация и авторизация пользователей (JWT)
- CRUD для карточек (корейское слово + перевод + пример)
- Алгоритм SM-2: карточки показываются именно тогда, когда их пора повторить
- Статистика прогресса
- Простой веб-интерфейс

## Технологии

- **FastAPI** — фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **Pydantic** — валидация данных
- **JWT** — авторизация
- **Docker + docker-compose** — запуск


<p align="center">
  <img src="screenshots/image1.png" width="1000">
  <br><em>Экран входа / регистрации</em>
</p>
<p align="center">
  <img src="screenshots/image2.png" width="1000">
  <br><em>Экран входа / регистрации с ошибкой</em>
</p>
<p align="center">
  <img src="screenshots/image3.png" width="1000">
  <br><em>Добавление новой карточки</em>
</p>
<p align="center">
  <img src="screenshots/image4.png" width="1000">
  <br><em>Повторение новой карточки</em>
</p>
<p align="center">
  <img src="screenshots/image5.png" width="1000">
  <br><em>Список карточек</em>
</p>
<p align="center">
  <img src="screenshots/image6.png" width="1000">
  <br><em>Документация</em>
</p>