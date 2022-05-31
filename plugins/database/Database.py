import datetime
import motor.motor_asyncio
from config import Config

class Db:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users


async def set_target(self, id, target):
        await self.col.update_one({'id': id}, {'$set': {'target': target}})


async def get_target(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('target', None)
