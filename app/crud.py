import chromadb
from tortoise import Tortoise, run_async
from .models import User

async def main():
    client = await chromadb.AsyncHttpClient()
    return client


async def init():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["hsg_task.models"]}
    )
    await Tortoise.generate_schemas()


run_async(init())
