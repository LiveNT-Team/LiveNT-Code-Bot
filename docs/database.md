# 1. Структура базы данных

## 1.1 users

- `id: int`
- `discord_gid: int`
- `discord_uid: int`
- `ai_per_name: str`

discord_gid и discord_uid - уникальная пара значений

## 1.2 guilds

- `id: int`
- `discord_gid: int`
- `developer_role_id: int`