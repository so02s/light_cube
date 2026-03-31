from dependency_injector import containers, providers

from src.output_interfaces import MQTTClient
from src.domain import CubeControl

class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])
    # TODO in another place
    # config.db.url.from_value(f"postgresql+asyncpg://{config.db.user}:{config.db.pasw}@{config.db.host}/{config.db.name}")

    mqtt_adapter = providers.Singleton(
        MQTTClient,
        hostname=config.mqtt.hostname,
        cube_topic=config.mqtt.cube_topic
    )

    cube_control = providers.Factory(
        CubeControl,
        light_output=mqtt_adapter
    )


    # user_service = providers.Singleton(UserServiceImpl, repository=user_repository)
    # game_service = providers.Singleton(
    #     GameServiceImpl,
    #     repository=game_repository,
    #     user_repository=user_repository,
    # )
    # auth_service = providers.Singleton(
    #     AuthServiceImpl,
    #     user_service=user_service,
    #     jwt_provider=jwt_provider,
    # )
    # authentication = providers.Singleton(
    #     Authentication, auth_service=auth_service, jwt_provider=jwt_provider
    # )
