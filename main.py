import task.models as models
import uvicorn
import os
import shutil

for f in os.listdir("files/"):
    os.remove(f"files/{f}")
shutil.rmtree("vectordb/")
models.create_db_and_tables()

if not os.path.exists("files"):
    os.makedirs("files")
if not os.path.exists("vectordb"):
    os.makedirs("vectordb")

uvicorn.run("task.api:app", host="127.0.0.1", port=8000,
            reload=False, log_level="debug", workers=1)

