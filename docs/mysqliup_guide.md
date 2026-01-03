# Документация MySqliUp

```python3
async def test_all_methods():
	
	db = MySqliUp()
	
	# 1. connect
	await db.connect()
	print("connect - подключение установлено")
	
	# 2. _validate_identifier
	valid = db._validate_identifier("test_table")
	print(f"_validate_identifier - валидация работает: {valid}")
	
	# 3. create_data_base
	await db.create_data_base("test_db")
	print("create_data_base - база создана")
	
	# 4. create_table
	columns = {
		"id": "INT AUTO_INCREMENT PRIMARY KEY",
		"name": "VARCHAR(100)",
		"age": "INT",
		"email": "VARCHAR(255)"
	}
	await db.create_table("userssz", columns)
	print("create_table - таблица создана")
	
	# 5. create_column
	await db.create_column("userssz", "status", "VARCHAR(50)")
	print("create_column - колонка добавлена")
	
	# 6. create_row
	user_data = {"name": "Иван", "age": 30, "email": "ivan@test.ru"}
	await db.create_row("userssz", user_data)
	await db.create_row("userssz", {"name": "Петр", "age": 25, "email": "petr@test.ru"})
	await db.create_row("userssz", {"name": "Мария", "age": 28, "email": "maria@test.ru"})
	print("create_row - строки добавлены")
	
	# 7. select_all_row
	row = await db.select_all_row("userssz", "id = %s", (1,))
	print(f"select_all_row - выбрана строка: {row}")
	
	# 8. select_row
	row = await db.select_row("userssz", ["name", "email"], "id = %s", (1,))
	print(f"select_row - выбраны колонки: {row}")
	
	# 9. select_count_all_row
	count = await db.select_count_all_row("userssz")
	print(f"select_count_all_row - количество строк: {count}")
	
	# 10. select_count_row
	count = await db.select_count_row("userssz", "name")
	print(f"select_count_row - уникальных значений: {count}")
	
	# 11. select_all_array
	names = await db.select_all_array("userssz", "name")
	print(f"select_all_array - массив: {names}")
	
	# 12. select_order_row
	ordered = await db.select_order_row("userssz", ["name", "age"], "age", "DESC")
	print(f"select_order_row - сортировка: {ordered}")
	
	# 13. update_row
	await db.update_row("userssz", {"age": 31}, "id = %s", (1,))
	print("update_row - строка обновлена")
	
	# 14-16. Транзакции: begin, commit, rollback
    await db.begin()              
        try:            
            await db.commit()           
        except Exception as e:
            await db.rollback()
            raise
	
	# 17. delete_row
	await db.delete_row("userssz", "name = %s", ("Коммит",))
	print("delete_row - строка удалена")
	
	# 18. delete_column
	await db.delete_column("userssz", "status")
	print("delete_column - колонка удалена")
	
	# 19. delete_table
	await db.delete_table("userssz")
	print("delete_table - таблица удалена")
	
	20. delete_data_base
	await db.delete_data_base("test_db")
	print("delete_data_base - база удалена")
	
	# 21. close
	await db.close()
	print("close - соединение закрыто")
	
	# 22-23. Контекстный менеджер: __aenter__, __aexit__
	async with MySqliUp() as db_ctx:
		print("__aenter__ - вход в контекст")
	print("__aexit__ - выход из контекста")


if __name__ == "__main__":
	import asyncio
	asyncio.run(test_all_methods())
```