import aiomysql
import re
from core.configuration import (
	MYSQL_HOST,
	MYSQL_USERNAME,
	MYSQL_PASSWORD,
	MYSQL_DATABASE,
	DEV_MYSQL_DATABASE,
	DEV_MYSQL_PASSWORD,
	DEV_MYSQL_USERNAME,
	DEV_MYSQL_HOST,
	MYSQL_PORT,
	IS_DEV_MODE,
)
from typing import Optional, Union, List, Dict, Any


class MySqliUp:
	def __init__(self):
		self.pool = None

	async def _begin(self, conn) -> None:
		await conn.begin()

	async def _commit(self, conn) -> None:
		await conn.commit()

	async def _rollback(self, conn) -> None:
		await conn.rollback()

	async def _execute(self, conn, cursor, query: str, params: tuple = ()) -> None:
		await cursor.execute(query, params)

	def _validate_identifier(self, identifier: str) -> str:
		if not re.match(r"^[a-zA-Z0-9_]+$", identifier):
			raise ValueError(f"Недопустимое имя идентификатора: {identifier}")
		if len(identifier) > 64:
			raise ValueError("Имя идентификатора слишком длинное (макс. 64 символа)")
		return identifier

	async def connect(self):
		self.pool = await aiomysql.create_pool(
			host=DEV_MYSQL_HOST if IS_DEV_MODE else MYSQL_HOST,
			user=DEV_MYSQL_USERNAME if IS_DEV_MODE else MYSQL_USERNAME,
			password=DEV_MYSQL_PASSWORD if IS_DEV_MODE else MYSQL_PASSWORD,
			db=DEV_MYSQL_DATABASE if IS_DEV_MODE else MYSQL_DATABASE,
			port=MYSQL_PORT,
			autocommit=False,
		)

	async def execute(self, query: str, params: tuple = (), fetch: str = None) -> Any:
		async with self.pool.acquire() as conn:
			async with conn.cursor(aiomysql.DictCursor) as cursor:
				try:
					await self._begin(conn)
					await self._execute(conn, cursor, query, params)
					if fetch == "one":
						res = await cursor.fetchone()
						await self._commit(conn)
						return res if res is not None else False
					if fetch == "all":
						res = await cursor.fetchall()
						await self._commit(conn)
						return res
					await self._commit(conn)
				except Exception as e:
					await self._rollback(conn)
					raise e


	async def create_row(self, table: str, data: Dict[str, Any]) -> None:
		table = self._validate_identifier(table)
		columns = [self._validate_identifier(col) for col in data.keys()]
		values = tuple(data.values())

		columns_sql = ", ".join([f"`{col}`" for col in columns])
		placeholders = ", ".join(["%s"] * len(values))

		await self.execute(
			f"INSERT INTO `{table}` ({columns_sql}) VALUES ({placeholders})", values
		)

	async def delete_row(
		self, table: str, where: Optional[str] = None, params: tuple = ()
	) -> None:
		table = self._validate_identifier(table)
		sql = f"DELETE FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		await self.execute(sql, params)

	async def update_row(
		self, table: str, updates: Dict[str, Any], where: str, where_params: tuple
	) -> None:
		table = self._validate_identifier(table)
		set_parts = []
		values = []

		for col, val in updates.items():
			validated_col = self._validate_identifier(col)
			set_parts.append(f"`{validated_col}` = %s")
			values.append(val)

		set_clause = ", ".join(set_parts)
		params = tuple(values) + where_params

		await self.execute(f"UPDATE `{table}` SET {set_clause} WHERE {where}", params)

	async def select_all_row(
		self, table: str, where: Optional[str] = None, params: tuple = ()
	) -> Union[Dict, bool]:
		table = self._validate_identifier(table)
		sql = f"SELECT * FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return await self.execute(sql, params, "one")

	async def select_row(
		self,
		table: str,
		columns: List[str],
		where: Optional[str] = None,
		params: tuple = (),
	) -> Union[Dict, bool]:
		table = self._validate_identifier(table)
		validated_columns = [self._validate_identifier(col) for col in columns]
		columns_sql = ", ".join([f"`{col}`" for col in validated_columns])

		sql = f"SELECT {columns_sql} FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return await self.execute(sql, params, "one")

	async def select_count_all_row(
		self,
		table: str,
		as_dict: bool = True,
		where: Optional[str] = None,
		params: tuple = (),
	) -> Any:
		table = self._validate_identifier(table)
		alias = " as count" if as_dict else ""
		sql = f"SELECT COUNT(*){alias} FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return await self.execute(sql, params, "one")

	async def select_count_row(
		self,
		table: str,
		column: str,
		as_dict: bool = True,
		where: Optional[str] = None,
		params: tuple = (),
	) -> Any:
		table = self._validate_identifier(table)
		column = self._validate_identifier(column)
		alias = " as count" if as_dict else ""
		sql = f"SELECT COUNT(DISTINCT `{column}`){alias} FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		return await self.execute(sql, params, "one")

	async def select_all_array(
		self, table: str, column: str, where: Optional[str] = None, params: tuple = ()
	) -> List[Any]:
		table = self._validate_identifier(table)
		column = self._validate_identifier(column)
		sql = f"SELECT `{column}` FROM `{table}`"
		if where:
			sql += f" WHERE {where}"
		results = await self.execute(sql, params, "all")
		return [row[column] for row in results]

	async def select_order_row(
		self, table: str, columns: List[str], order_by: str, order_dir: str = "ASC"
	) -> Union[Dict, bool]:
		table = self._validate_identifier(table)
		validated_columns = [self._validate_identifier(col) for col in columns]
		order_column = self._validate_identifier(order_by)

		if order_dir.upper() not in ("ASC", "DESC"):
			raise ValueError("order_dir должен быть 'ASC' или 'DESC'")

		columns_sql = ", ".join([f"`{col}`" for col in validated_columns])
		return await self.execute(
			f"SELECT {columns_sql} FROM `{table}` ORDER BY `{order_column}` {order_dir.upper()}",
			(),
			"one",
		)

	async def close(self) -> None:
		if self.pool:
			self.pool.close()
			await self.pool.wait_closed()

	async def __aenter__(self):
		await self.connect()
		return self

	async def __aexit__(self, *args):
		await self.close()