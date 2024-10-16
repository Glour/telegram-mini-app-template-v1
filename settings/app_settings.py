from functools import lru_cache

from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

from settings.bot_settings import BotSettings
from settings.db_settings import DatabaseSettings
from settings.logging_settings import LoggingSettings
from settings.miscellaneous_settings import MiscellaneousSettings


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str('.env'),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    is_development: bool = Field(default=False)
    postgres: DatabaseSettings
    logging: LoggingSettings
    bot: BotSettings
    misc: MiscellaneousSettings = Field(default_factory=MiscellaneousSettings)


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings()
