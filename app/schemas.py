from pydantic import BaseModel
from typing import Dict

class ConfigurationBase(BaseModel):
    country_code: str
    requirements: Dict[str, str]

class ConfigurationCreate(ConfigurationBase):
    pass

class Configuration(ConfigurationBase):
    class Config:
        orm_mode = True
