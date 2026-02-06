import aiomysql
import re
from core.configuration import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
    MYSQL_PORT,
)
from typing import Optional, List, Dict, Any


class MySqliUp:
    def __init__(self):
        self.pool = None
        self._conn = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DATABASE,
            port=MYSQL_PORT,
            autocommit=False,
        )

    async def begin(self) -> None:
        self._conn = await self.pool.acquire()
        await self._conn.begin()

    async def commit(self) -> None:
        if self._conn:
            try:
                await self._conn.commit()
            finally:
                self.pool.release(self._conn)
                self._conn = None

    async def rollback(self) -> None:
        if self._conn:
            try:
                await self._conn.rollback()
            finally:
                self.pool.release(self._conn)
                self._conn = None

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def _execute(self, query: str, params: tuple = (), conn=None, cursor=None):
        if conn is None or cursor is None:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, params)
                    await conn.commit()
        else:
            await cursor.execute(query, params)

    async def _query_fetch_one(self, query: str, params: tuple = ()):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchone()
                await conn.commit()
                return result

    async def _query_fetch_all(self, query: str, params: tuple = ()):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchall()
                await conn.commit()
                return result

    def _validate_identifier(self, identifier: str) -> str:
        if re.match(r"^[a-zA-Z0-9_]+$", identifier):
            return identifier

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
            column_defs.append(f"`{validated_name}` {col_type}")

        columns_sql = ", ".join(column_defs)
        await self._execute(f"CREATE TABLE IF NOT EXISTS `{table}` ({columns_sql})")

    async def delete_table(self, table: str) -> None:
        table = self._validate_identifier(table)
        await self._execute(f"DROP TABLE IF EXISTS `{table}`")

    async def create_column(self, table: str, column: str, column_type: str) -> None:
        table = self._validate_identifier(table)
        column = self._validate_identifier(column)
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
    ) -> Optional[Dict[str, Any]]:
        table = self._validate_identifier(table)
        sql = f"SELECT * FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        return await self._query_fetch_one(sql, params)

    async def select_row(
        self,
        table: str,
        columns: List[str],
        where: Optional[str] = None,
        params: tuple = (),
    ) -> Optional[Dict[str, Any]]:
        table = self._validate_identifier(table)
        validated_columns = [self._validate_identifier(col) for col in columns]
        columns_sql = ", ".join([f"`{col}`" for col in validated_columns])
        sql = f"SELECT {columns_sql} FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        return await self._query_fetch_one(sql, params)

    async def select_rows(
        self,
        table: str,
        columns: List[str],
        where: Optional[str] = None,
        params: tuple = (),
    ) -> List[Dict[str, Any]]:
        table = self._validate_identifier(table)
        validated_columns = [self._validate_identifier(col) for col in columns]
        columns_sql = ", ".join([f"`{col}`" for col in validated_columns])
        sql = f"SELECT {columns_sql} FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        return await self._query_fetch_all(sql, params)

    async def select_count_all_row(
        self,
        table: str,
        where: Optional[str] = None,
        params: tuple = (),
    ) -> int:
        table = self._validate_identifier(table)
        sql = f"SELECT COUNT(*) as count FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        result = await self._query_fetch_one(sql, params)
        return result["count"]

    async def select_count_row(
        self,
        table: str,
        column: str,
        where: Optional[str] = None,
        params: tuple = (),
    ) -> int:
        table = self._validate_identifier(table)
        column = self._validate_identifier(column)
        sql = f"SELECT COUNT(DISTINCT `{column}`) as count FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        result = await self._query_fetch_one(sql, params)
        return result["count"]

    async def select_all_array(
        self, table: str, column: str, where: Optional[str] = None, params: tuple = ()
    ) -> List[Any]:
        table = self._validate_identifier(table)
        column = self._validate_identifier(column)
        sql = f"SELECT `{column}` FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        results = await self._query_fetch_all(sql, params)
        return [list(row.values())[0] for row in results] if results else []

    async def select_order_row(
        self, table: str, columns: List[str], order_by: str, order_dir: str = "ASC"
    ) -> Optional[Dict[str, Any]]:
        table = self._validate_identifier(table)
        validated_columns = [self._validate_identifier(col) for col in columns]
        order_column = self._validate_identifier(order_by)

        if order_dir.upper() in ("ASC", "DESC"):
            columns_sql = ", ".join([f"`{col}`" for col in validated_columns])
            return await self._query_fetch_one(
                f"SELECT {columns_sql} FROM `{table}` ORDER BY `{order_column}` {order_dir.upper()}"
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
