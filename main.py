import argparse

from aiohttp import web
from pollapp.app import init_app
from settings import Settings, get_config


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config file")
    args: argparse.Namespace = parser.parse_args()

    default_config_path: str = args.config or './config.yaml'
    config_object: Settings = get_config(default_config_path)
    web.run_app(init_app(config_object),
                host=config_object.api_host, port=config_object.api_port)
