from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from models.model import *
from sqlalchemy.orm import sessionmaker, Session
from db import engine_s


def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()


users_router = APIRouter()

@users_router.get("/api/courier", response_model=Union[list[Main_User_1], list[Main_User_2]])
def get_user_db(DB: Session = Depends(get_session)):
    '''Получение информации о всех курьерах системе.'''
    users = DB.query(User).all()
    if users == None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    else:
        return users

@users_router.post("/api/courier", response_model=Union[Main_User_1, Main_User_2], status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User_2, Body(embell=True, description="Новый пользователь")], DB: Session = Depends(get_session)):
    '''Регистрация курьера в системе.'''
    try:
        user = User(name=item.name, district=item.district)
        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(user)
        DB.commit()
        DB.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта")

@users_router.get("/api/courier/{id}", response_model=Union[Main_User_3, Main_Order_3])
def get_user_(id: int, DB: Session = Depends(get_session)):
    """Получение подробной информации о курьере."""
    user = DB.query(User).filter(User.id_user == id).first()
    if user == None:
        return JSONResponse(status_code=484, content={"message": "Пользователь не найден"})
    else:
        return user

#-------------------------

@users_router.post("/api/order", response_model=Union[Main_Order_2, Main_User_4], status_code=status.HTTP_201_CREATED)
def create_order(name: str, district: str, DB: Session = Depends(get_session)):
    '''Публикация заказа в системе с полями:'''
    try:
        user_id = DB.query(User.id_user).all()
        count = 0
        order = Order(name=name, district=district)
        for i in DB.query(User.district).all():
            if district in i[0]:
                break
            count += 1
        order.id_user = user_id[count][0]
        order.status = 1
        if order is None:
            raise HTTPException(status_code=404, detail="Объект не определен")

        user = DB.query(User).filter(User.id_user == user_id[count][0]).filter(User.active_order == {}).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Нет свободного курьера")
        DB.add(order)
        DB.commit()
        DB.refresh(order)

        user.active_order = {"order_id": order.id_order, "order_name": order.name}
        user.time_start = datetime.datetime.today().timestamp()
        try:
            user.time_start_work = user.time_start_work + 1 - 1
        except:
            user.time_start_work = datetime.datetime.today().timestamp()
        DB.add(user)
        DB.commit()
        DB.refresh(user)

        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта. Нет подходящего курьера в данном районе")

@users_router.get("/api/order/{id}", response_model=Union[Main_Order_3])
def get_order(id: int, DB: Session = Depends(get_session)):
    """Получение информации о заказе."""
    order = DB.query(Order).filter(Order.id_order == id).first()
    if order == None:
        return JSONResponse(status_code=484, content={"message": "Заказ не найден"})
    else:
        return order


@users_router.post("/api/order{id}", response_model=Union[Main_Order_4, Main_User_4], status_code=status.HTTP_201_CREATED)
def end_order(id: int, DB: Session = Depends(get_session)):
    '''Завершить заказ.'''
    order = DB.query(Order).filter(Order.id_order == id).first()
    if order == None:
        return JSONResponse(status_code=484, content={"message": "Заказ не найден"})
    else:
        if order.status == 2:
            return JSONResponse(status_code=484, content={"message": "Заказ уже завершён"})

        user = DB.query(User).filter(User.active_order == {"order_id": order.id_order, "order_name": order.name}).first()
        user.active_order = {}
        order.status = 2
        DB.add(order)
        DB.commit()
        DB.refresh(order)

        user.time_end = datetime.datetime.today().timestamp()
        try:
            user.counter_ord = user.counter_ord + 1
        except:
            user.counter_ord = 0
            user.counter_ord = user.counter_ord + 1
        if datetime.datetime.today().timestamp() - user.time_start_work > 86400:
            try:
                user.avg_day_orders = (user.avg_day_orders + user.counter_ord) / 2
            except:
                user.avg_day_orders = user.avg_day_orders
            user.counter_ord = 0
        try:
            user.avg_list_time = [round(user.time_end - user.time_start)] + user.avg_list_time
        except:
            user.avg_list_time = [round(user.time_end - user.time_start)]
        user.avg_order_complete_time = str(datetime.timedelta(seconds=sum(map(int, user.avg_list_time))/len(user.avg_list_time)))
        DB.add(user)
        DB.commit()
        DB.refresh(user)
        return order