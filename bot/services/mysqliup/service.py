import aiomysql
import re
from ...core.configuration import (
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
    def __init__(self, name: str):
        self._pool = None
        self._database = self._validate_identifier(name)

    def _validate_identifier(self, identifier: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", identifier):
            raise ValueError(f"Недопустимое имя идентификатора: {identifier}")
        if len(identifier) > 64:
            raise ValueError("Имя идентификатора слишком длинное (макс. 64 символа)")
        return identifier

    async def connect(self):
        self._pool = await aiomysql.create_pool(
            host=DEV_MYSQL_HOST if IS_DEV_MODE else MYSQL_HOST,
            user=DEV_MYSQL_USERNAME if IS_DEV_MODE else MYSQL_USERNAME,
            password=DEV_MYSQL_PASSWORD if IS_DEV_MODE else MYSQL_PASSWORD,
            db=DEV_MYSQL_DATABASE if IS_DEV_MODE else MYSQL_DATABASE,
            port=MYSQL_PORT,
            autocommit=False,
        )

    async def _execute(self, query: str, params: tuple = (), fetch: str = None) -> Any:
        async with self._pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute(query, params)
                    if fetch == "one":
                        res = await cursor.fetchone()
                        return res if res is not None else False
                    if fetch == "all":
                        return await cursor.fetchall()
                    await conn.commit()
                except Exception as e:
                    await conn.rollback()
                    raise

    async def create_data_base(self, database: str) -> None:
        database = self._validate_identifier(database)
        await self._execute(f"CREATE DATABASE IF NOT EXISTS `{database}`")

    async def delete_data_base(self, database: str) -> None:
        database = self._validate_identifier(database)
        await self._execute(f"DROP DATABASE IF EXISTS `{database}`")

    async def create_table(self, table: str, columns: Dict[str, str]) -> None:
        table = self._validate_identifier(table)
        column_defs = []
        for col_name, col_type in columns.items():
            validated_name = self._validate_identifier(col_name)
            if not re.match(
                r"^[A-Z]+(([0-9,]+))?(s+(NOTs+NULL|NULL|AUTO_INCREMENT|PRIMARYs+KEY|UNIQUE))*$",
                col_type,
                re.IGNORECASE,
            ):
                raise ValueError(f"Недопустимый тип колонки: {col_type}")
            column_defs.append(f"`{validated_name}` {col_type}")

        columns_sql = ", ".join(column_defs)
        await self._execute(f"CREATE TABLE IF NOT EXISTS `{table}` ({columns_sql})")

    async def delete_table(self, table: str) -> None:
        table = self._validate_identifier(table)
        await self._execute(f"DROP TABLE IF EXISTS `{table}`")

    async def create_column(self, table: str, column: str, column_type: str) -> None:
        table = self._validate_identifier(table)
        column = self._validate_identifier(column)
        if not re.match(
            r"^[A-Z]+(([0-9,]+))?(s+(NOTs+NULL|NULL|AUTO_INCREMENT|UNIQUE))*$",
            column_type,
            re.IGNORECASE,
        ):
            raise ValueError(f"Недопустимый тип колонки: {column_type}")
        await self._execute(
            f"ALTER TABLE `{table}` ADD COLUMN `{column}` {column_type}"
        )

    async def delete_column(self, table: str, column: str) -> None:
        table = self._validate_identifier(table)
        column = self._validate_identifier(column)
        await self._execute(f"ALTER TABLE `{table}` DROP COLUMN `{column}`")

    async def create_row(self, table: str, data: Dict[str, Any]) -> None:
        table = self._validate_identifier(table)
        columns = [self._validate_identifier(col) for col in data.keys()]
        values = tuple(data.values())

        columns_sql = ", ".join([f"`{col}`" for col in columns])
        placeholders = ", ".join(["%s"] * len(values))

        await self._execute(
            f"INSERT INTO `{table}` ({columns_sql}) VALUES ({placeholders})", values
        )

    async def delete_row(
        self, table: str, where: Optional[str] = None, params: tuple = ()
    ) -> None:
        table = self._validate_identifier(table)
        sql = f"DELETE FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        await self._execute(sql, params)

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

        await self._execute(f"UPDATE `{table}` SET {set_clause} WHERE {where}", params)

    async def select_all_row(
        self, table: str, where: Optional[str] = None, params: tuple = ()
    ) -> Union[Dict, bool]:
        table = self._validate_identifier(table)
        sql = f"SELECT * FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        return await self._execute(sql, params, "one")

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
        return await self._execute(sql, params, "one")

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
        return await self._execute(sql, params, "one")

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
        return await self._execute(sql, params, "one")

    async def select_all_array(
        self, table: str, column: str, where: Optional[str] = None, params: tuple = ()
    ) -> List[Any]:
        table = self._validate_identifier(table)
        column = self._validate_identifier(column)
        sql = f"SELECT `{column}` FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        results = await self._execute(sql, params, "all")
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
        return await self._execute(
            f"SELECT {columns_sql} FROM `{table}` ORDER BY `{order_column}` {order_dir.upper()}",
            (),
            "one",
        )

    async def close(self) -> None:
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()
