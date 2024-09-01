from pydantic import BaseModel, SecretStr, Field

from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    uri: str = Field(validation_alias="DB_URL")
    db_name: str = Field(validation_alias="DB_NAME")
    password: SecretStr = Field(validation_alias="DB_PASSWORD")
    username: str = Field(validation_alias="DB_USER")


class TelegramSettings(BaseSettings):
    token: SecretStr = Field(validation_alias="BOT_TOKEN")


class Config(BaseModel):
    db: DBSettings = DBSettings()
    telegram: TelegramSettings = TelegramSettings()
