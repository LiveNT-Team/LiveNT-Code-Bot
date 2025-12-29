import mysql.connector
import os
import re
from ...core.configuration import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD
from typing import Optional, Union, List, Dict, Any

class MySqliUp:
	def __init__(self, name: str):
		self._file = mysql.connector.connect(
			host=MYSQL_HOST,
			user=MYSQL_USERNAME,
			password=MYSQL_PASSWORD,
			database=self._validate_identifier(name)
		)
		self._cursor = self._file.cursor(dictionary=True)

	def _validate_identifier(self, identifier: str) -> str:
		if not re.match(r'^[a-zA-Z0-9_]+$', identifier):
			raise ValueError(f"Недопустимое имя идентификатора: {identifier}")
		if len(identifier) > 64:
			raise ValueError("Имя идентификатора слишком длинное (макс. 64 символа)")
		return identifier

	def _execute(self, query: str, params: tuple = (), fetch: str = None) -> Any:
		try:
			self._cursor.execute(query, params)
			if fetch == 'one':
				res = self._cursor.fetchone()
				return res if res is not None else False
			if fetch == 'all':
				return self._cursor.fetchall()
			self._file.commit()
		except mysql.connector.Error as e:
			self._file.rollback()
			raise

	def create_data_base(self, database: str) -> None:
		database = self._validate_identifier(database)
		self._execute(f"CREATE DATABASE IF NOT EXISTS `{database}`")

	def delete_data_base(self, database: str) -> None:
		database = self._validate_identifier(database)
		self._execute(f"DROP DATABASE IF EXISTS `{database}`")

	def create_table(self, table: str, columns: Dict[str, str]) -> None:
		table = self._validate_identifier(table)
		column_defs = []
		for col_name, col_type in columns.items():
			validated_name = self._validate_identifier(col_name)
			if not re.match(r'^[A-Z]+(([0-9,]+))?(s+(NOTs+NULL|NULL|AUTO_INCREMENT|PRIMARYs+KEY|UNIQUE))*$', col_type, re.IGNORECASE):
				raise ValueError(f"Недопустимый тип колонки: {col_type}")
			column_defs.append(f"`{validated_name}` {col_type}")
		
		columns_sql = ", ".join(column_defs)
		self._execute(f"CREATE TABLE IF NOT EXISTS `{table}` ({columns_sql})")

	def delete_table(self, table: str) -> None:
		table = self._validate_identifier(table)
		self._execute(f"DROP TABLE IF EXISTS `{table}`")

	def create_column(self, table: str, column: str, column_type: str) -> None:
		table = self._validate_identifier(table)
		column = self._validate_identifier(column)
		if not re.match(r'^[A-Z]+(([0-9,]+))?(s+(NOTs+NULL|NULL|AUTO_INCREMENT|UNIQUE))*$', column_type, re.IGNORECASE):
			raise ValueError(f"Недопустимый тип колонки: {column_type}")
		self._execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {column_type}")

	def delete_column(self, table: str, column: str) -> None:
		table = self._validate_identifier(table)
		column = self._validate_identifier(column)
		self._execute(f"ALTER TABLE `{table}` DROP COLUMN `{column}`")

	def create_string(self, table: str, data: Dict[str, Any]) -> None:
		table = self._validate_identifier(table)
		columns = [self._validate_identifier(col) for col in data.keys()]
		values = tuple(data.values())
		
		columns_sql = ", ".join([f"`{col}`" for col in columns])
		placeholders = ", ".join(["%s"] * len(values))
		
		self._execute(f"INSERT INTO `{table}` ({columns_sql}) VALUES ({placeholders})", values)

	def delete_string(self, table: str, where: Optional[str] = None, params: tuple = ()) -> None:
		table = self._validate_identifier(table)
		sql = f"DELETE FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		self._execute(sql, params)

	def update_string(self, table: str, updates: Dict[str, Any], where: str, where_params: tuple) -> None:
		table = self._validate_identifier(table)
		set_parts = []
		values = []
		
		for col, val in updates.items():
			validated_col = self._validate_identifier(col)
			set_parts.append(f"`{validated_col}` = %s")
			values.append(val)
		
		set_clause = ", ".join(set_parts)
		params = tuple(values) + where_params
		
		self._execute(f"UPDATE `{table}` SET {set_clause} WHERE {where}", params)

	def select_all_string(self, table: str, where: Optional[str] = None, params: tuple = ()) -> Union[Dict, bool]:
		table = self._validate_identifier(table)
		sql = f"SELECT * FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return self._execute(sql, params, 'one')

	def select_string(self, table: str, columns: List[str], where: Optional[str] = None, params: tuple = ()) -> Union[Dict, bool]:
		table = self._validate_identifier(table)
		validated_columns = [self._validate_identifier(col) for col in columns]
		columns_sql = ", ".join([f"`{col}`" for col in validated_columns])
		
		sql = f"SELECT {columns_sql} FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return self._execute(sql, params, 'one')

	def select_count_all_string(self, table: str, as_dict: bool = True, where: Optional[str] = None, params: tuple = ()) -> Any:
		table = self._validate_identifier(table)
		alias = " as count" if as_dict else ""
		sql = f"SELECT COUNT(*){alias} FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return self._execute(sql, params, 'one')

	def select_count_string(self, table: str, column: str, as_dict: bool = True, where: Optional[str] = None, params: tuple = ()) -> Any:
		table = self._validate_identifier(table)
		column = self._validate_identifier(column)
		alias = " as count" if as_dict else ""
		sql = f"SELECT COUNT(DISTINCT `{column}`){alias} FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return self._execute(sql, params, 'one')

	def select_all_array(self, table: str, column: str, where: Optional[str] = None, params: tuple = ()) -> List[Any]:
		table = self._validate_identifier(table)
		column = self._validate_identifier(column)
		sql = f"SELECT `{column}` FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return [row[column] for row in self._execute(sql, params, 'all')]

	def select_order_string(self, table: str, columns: List[str], order_by: str, order_dir: str = 'ASC') -> Union[Dict, bool]:
		table = self._validate_identifier(table)
		validated_columns = [self._validate_identifier(col) for col in columns]
		order_column = self._validate_identifier(order_by)
		
		if order_dir.upper() not in ('ASC', 'DESC'):
			raise ValueError("order_dir должен быть 'ASC' или 'DESC'")
		
		columns_sql = ", ".join([f"`{col}`" for col in validated_columns])
		return self._execute(f"SELECT {columns_sql} FROM `{table}` ORDER BY `{order_column}` {order_dir.upper()}", (), 'one')

	def close(self) -> None:
		self._cursor.close()
		self._file.close()

	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.close()