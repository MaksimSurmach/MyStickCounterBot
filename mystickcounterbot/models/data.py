from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class GoalMetadata(BaseModel):
    daily_goal: int = Field(alias="number", default=0)
    last_set: dt = Field(alias="last_set", default_factory=lambda: dt.now())
    user_id: int = Field(alias="user_id", default=None)


class PriceMetadata(BaseModel):
    price: int = Field(alias="price", default=0)
    last_set: dt = Field(alias="last_set", default_factory=lambda: dt.now())


class UserSettings(BaseModel):
    motivation: bool = Field(alias="motivation", default=False)


class UserMetaData(BaseModel):
    user_id: int = Field(alias="user_id")
    username: str = Field(alias="username", default=None)
    goals: GoalMetadata = Field(alias="goals", default_factory=GoalMetadata)
    prices: PriceMetadata = Field(alias="prices", default_factory=PriceMetadata)
    settings: UserSettings = Field(alias="settings", default_factory=UserSettings)
    last_updated: dt = Field(alias="last_updated", default_factory=lambda: dt.now())


class StickActivityMetadata(BaseModel):
    count: int = Field(alias="number")
    user_id: int = Field(alias="user_id")
    timestamp: dt = Field(alias="timestamp", default_factory=lambda: dt.now())


class StickAddedMessageData(BaseModel):
    today_smoked: int = Field(alias="today_smoked")
    added_stick: int = Field(alias="added_stick")
    goal: GoalMetadata = Field(alias="goals", default_factory=GoalMetadata)
    last_smoked: dt | None = Field(alias="timestamp", default=None)

