from app.models.config import ConfigWetterCom

app_config = {
    "DEVELOPMENT": ConfigWetterCom(
            host="https://forecast9.p.rapidapi.com"
        )
}

PROD_URL = ""
TEST_URL = ""
HOST_MAPPING = {
    PROD_URL: "PROD",
    TEST_URL: "TEST"
}


def get_config_by_stage(stage):
    return app_config[stage] if stage else app_config["DEVELOPMENT"]


def get_config_by_context(data_context):
    return app_config[data_context] if data_context else app_config["DEVELOPMENT"]
