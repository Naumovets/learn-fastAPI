from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

fake_users = [
    {'id': 1, 'name': 'Даниил', 'role': 'investor'},
    {'id': 2, 'name': 'Кирилл', 'role': 'trader'},
    {'id': 3, 'name': 'Антон', 'role': 'trader'},
    {'id': 4, 'name': 'Александр', 'role': 'investor', 'degree': [{'id': 1, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'}]},
]

fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 223, 'amount': 1.12}
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


class TypeDegree(Enum):
    noob = 'noob'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: TypeDegree


class User(BaseModel):
    id: int
    name: str
    role: str
    degree: Optional[List[Degree]] = []


@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


@app.put('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get('id') == user_id, fake_users))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}


@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:offset + limit]


@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}
