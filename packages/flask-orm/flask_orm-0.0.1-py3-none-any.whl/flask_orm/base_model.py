from sqlalchemy import Column, Integer
from typing import Optional, ClassVar, TypeVar, Generic, AnyStr
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .base_query import BaseQuery


Q = TypeVar['Q']


class BaseModel(Generic[Q]):
    query: Q = None

    @property
    def session(self) -> Q.session:
        return self.query.session

    @declared_attr
    def __tablename__(cls) -> AnyStr:
        return cls.__name__

    @declared_attr
    def id(self) -> Column:
        return Column(Integer, primary_key=True)

    @classmethod
    def all(cls) -> Q:
        return cls.query.all()

    def save(self, commit: bool=True) -> None:
        self.session.add(self)
        if commit:
            self.session.commit()

    def delete(self) -> None:
        self.session.remove(self)
        self.session.commit()





Model = declarative_base(cls=BaseModel[BaseQuery])
