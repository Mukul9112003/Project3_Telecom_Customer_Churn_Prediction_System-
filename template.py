import os
from pathlib import Path
program_name="src"
list_of_files=[
    f"{program_name}/components/__init__.py",
    f"{program_name}/components/data_ingestion.py",
    f"{program_name}/pipeline/__init__.py",
    f"{program_name}pipeline/training_pipeline.py",
    f"{program_name}/constants/__init__.py",
    f"{program_name}/logger/__init__.py",
    f"{program_name}/entity/__init__.py",
    f"{program_name}/entity/config_entity.py",
    f"{program_name}/entity/artifact_entity.py",
    f"{program_name}/configuration/__init__.py",
    f"{program_name}/configuration/mongo_db_connection.py",
    f"{program_name}/data_access/__init__.py",
    f"{program_name}/data_access/telecom.py",
    f"{program_name}/exception/__init__.py",
    "app.py",
    "demo.py",
    "setup.py",
    f"test/__init__.py",
    f"test/testing_excception.py",
    f"test/testing_database_connection.py"
]
for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
    if (not os.path.exists(filepath)) or os.path.getsize(filepath):
        with open(filepath,"a")as file:
            pass
    else:
        print(f"File exist by the name {filepath}")
#git pull origin main --allow-unrelated-histories