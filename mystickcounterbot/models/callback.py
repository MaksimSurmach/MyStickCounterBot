from pydantic import BaseModel, Field
import json


def get_callback_type(data: str) -> str:
    data = json.loads(data)
    if data.get("type"):
        return data.get("type")
    else:
        return ""


class AddQuery(BaseModel):
    type: str = "Add number"
    number: int


class ReduceQuery(BaseModel):
    type: str = "Reduce number"
    number: int


class AddMenuQuery(BaseModel):
    type: str = "Add menu"


class ReduceMenuQuery(BaseModel):
    type: str = "Reduce menu"


class GoalQuery(BaseModel):
    type: str = "Goal menu"


class SetGoalQuery(BaseModel):
    type: str = "Set goal"
    number: int


class SetPriceQuery(BaseModel):
    type: str = "Set price"
    number: int


class PriceQuery(BaseModel):
    type: str = "Price menu"


class StatsQuery(BaseModel):
    type: str = "Stats"
