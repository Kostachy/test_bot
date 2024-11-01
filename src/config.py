from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    api_hash: str
    api_id: int


@dataclass
class DatabaseConfig:
    database_url: str


@dataclass
class Config:
    tg_bot: TgBot
    database: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env("TG_BOT_TOKEN"),
            api_hash=env("TG_BOT_API_HASH"),
            api_id=env("TG_BOT_API_ID"),
        ),
        database=DatabaseConfig(database_url=env("DATABASE_URL"))
    )
