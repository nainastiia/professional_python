import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    low_stock_threshold: int
    environment: str

def get_config() -> AppConfig:
    threshold = int(os.getenv("LOW_STOCK_THRESHOLD", "5"))
    env = os.getenv("APP_ENV", "development")
    return AppConfig(low_stock_threshold=threshold, environment=env)