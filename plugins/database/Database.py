import datetime
import motor.motor_asyncio
import Config

class db:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users


async def set_target(self, id, caption):
        await self.col.update_one({'id': id}, {'$set': {'target': target}})


async def get_target(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('target', None)
