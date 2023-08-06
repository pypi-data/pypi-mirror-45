# mautrix-facebook - A Matrix-Facebook Messenger puppeting bridge
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Any, Iterator, Optional
from abc import abstractmethod

from sqlalchemy import Table
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.result import RowProxy, ResultProxy
from sqlalchemy.sql.base import ImmutableColumnCollection
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    db: Engine
    t: Table
    __table__: Table
    c: ImmutableColumnCollection

    @classmethod
    def _one_or_none(cls, rows: ResultProxy) -> Optional[Any]:
        try:
            return cls.scan(next(rows))
        except StopIteration:
            return None

    @classmethod
    def _all(cls, rows: ResultProxy) -> Iterator[Any]:
        for row in rows:
            yield cls.scan(row)

    @classmethod
    @abstractmethod
    def scan(cls, row: RowProxy) -> Any:
        pass

    @classmethod
    def _select_all(cls, *args) -> Iterator[Any]:
        query = cls.t.select()
        if args:
            query = query.where(*args)
        yield from cls._all(cls.db.execute(query))

    @classmethod
    def _select_one_or_none(cls, *args) -> Any:
        query = cls.t.select()
        if args:
            query = query.where(*args)
        return cls._one_or_none(cls.db.execute(query))

    @property
    @abstractmethod
    def _edit_identity(self) -> Any:
        pass

    def edit(self, *, _update_values: bool = True, **values) -> None:
        with self.db.begin() as conn:
            conn.execute(self.t.update()
                         .where(self._edit_identity)
                         .values(**values))
        if _update_values:
            for key, value in values.items():
                setattr(self, key, value)

    def delete(self) -> None:
        with self.db.begin() as conn:
            conn.execute(self.t.delete().where(self._edit_identity))
