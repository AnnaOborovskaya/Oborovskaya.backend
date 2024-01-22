from typing import Union, Annotated
import datetime
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, String, Integer, Identity, Sequence, Float, Boolean, ForeignKey, MetaData, DATETIME, ARRAY, JSON
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id_user = Column(Integer, primary_key=True)
    name = Column(String)
    avg_order_complete_time = Column(DATETIME)
    avg_day_orders = Column(Integer)
    district = Column(ARRAY(String))
    active_order = Column(JSON)
    avg_list_time = Column(ARRAY(Integer))
    time_start = Column(Integer)
    time_end = Column(Integer)
    counter_ord = Column(Integer)
    time_start_work = Column(Integer)

class Order(Base):
    __tablename__ = "orders"
    id_order = Column(Integer, primary_key=True)
    name = Column(String)
    district = Column(String)
    status = Column(Integer)
    id_user = Column(Integer, ForeignKey("users.id_user"))


class Main_User_1(BaseModel):
    id_user: Union[int, None] = None
    name: Union[str, None] = None

class Main_User_2(BaseModel):
    name: Union[str, None] = None
    district: Union[list, None] = None

class Main_User_3(Main_User_1):
    active_order: Union[dict, None] = None
    avg_order_complete_time: Union[datetime.time, None] = None
    avg_day_orders: Union[int, None] = None

class Main_User_4(BaseModel):
    id_user: Union[int, None] = None
    district: Union[list, None] = None
    active_order: Union[dict, None] = None
    avg_order_complete_time: Union[datetime.time, None] = None
    avg_day_orders: Union[int, None] = None
    avg_list_time: Union[list, None] = None
    time_start: Union[int, None] = None
    time_end: Union[int, None] = None
    counter_ord: Union[int, None] = None
    time_start_work: Union[int, None] = None

class Main_Order_1(BaseModel):
    id_order: Union[int, None] = None

class Main_Order_2(Main_Order_1):
    name: Union[str, None] = None
    district: Union[str, None] = None
    id_user: Union[int, None] = None

class Main_Order_3(Main_Order_1):
    id_user: Union[int, None] = None
    status: Union[int, None] = None


class Main_Order_4(Main_Order_1):
    status: Union[int, None] = None

class Main_Order_5(Main_Order_1):
    name: Union[str, None] = None
    district: Union[str, None] = None
    status: Union[int, None] = None
    id_user: Union[int, None] = None
