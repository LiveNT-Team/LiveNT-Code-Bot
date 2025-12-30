# Установка и запуск
## Установка
1. Склонируйте репозиторий.
  ```bash
  git clone https://github.com/LiveNT-Team/LiveNT-Code-Bot.git
  ```

2. Перейдите в каталог репозитория.
  ```bash
  cd LiveNT-Code-Bot
  ```

3. Создайте `.env` файл на основе файла `template.env`.
  ```bash
  mv template.env .env
  ```

4. Заполните файл `.env`. Документацию по `.env` файлу можете найти [тут](./env.md).

5. Соберите проект.
  ```bash
  docker compose build
  ```
## Запуск
Убедитесь что вы используете Docker V2.
### Запуск проекта в режиме разработки
Режим разработки включает в себя запуск тестового сервера `mysql`, `phpMyAdmin` для администрирования СУБД и самого бота.
1. Запустите контейнеры.
  ```bash
  docker compose up
  ```

> [!NOTE]
> Если вы не планируете использовать `phpMyAdmin`, следует выполнить команду `docker compose up bot dev-mysql` (запустит все контейнеры кроме `phpMyAdmin`).

### Запуск проекта в режиме продукта

1. Запустите контейнер.
  ```bash
  docker compose up bot
  ```

> [!NOTE]
> Для запуска контейнера в фоновом режиме добавьте флаг -d: `docker compose up -d`