from pydantic import BaseModel, Field
from pathlib import Path
import yaml

class PROJECT_CONFIG(BaseModel):
    name: str
    version: str

class VECTOR_STORE_CONFIG(BaseModel):
    type: str
    persist_directory: str
    collection_name: str


class AppConfig(BaseModel):
    project_config: PROJECT_CONFIG = Field(validation_alias="project_name")
    vector_store: VECTOR_STORE_CONFIG = Field(validation_alias="vector_db")

config_path = Path(__file__).resolve().parents[2] / "project_config.yml"
with open(config_path, "r") as file:
    data = yaml.safe_load(file)

config = AppConfig.model_validate(data)
persist_directory = Path(config.vector_store.persist_directory)
if not persist_directory.is_absolute():
    config.vector_store.persist_directory = str((config_path.parent / persist_directory).resolve())
    