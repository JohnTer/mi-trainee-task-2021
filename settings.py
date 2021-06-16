from dataclasses import dataclass

import yaml


@dataclass
class Settings(object):
    db_driver: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    api_host: str
    api_port: int

    def get_db_url(self) -> str:
        return f'{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'


def get_config(filepath: str) -> Settings:
    with open(filepath, 'r') as f:
        yaml_config: dict = yaml.load(f)
        settings_object: Settings = Settings(
            **(yaml_config['api'] | yaml_config['database']))
    return settings_object
