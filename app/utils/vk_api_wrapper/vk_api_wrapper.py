import aiohttp

from app.schemas.vk_group_schema import VKGroupExternal


class VKAPIWrapper:
    def __init__(
        self,
        usertoken: int,
    ) -> None:
        self.usertoken = usertoken


    async def _get(
        self,
        url: str
    ):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()

        return result


    async def get_groups(
        self
    ):
        response = await self._get(
            f"https://api.vk.com/method/groups.get?access_token={self.usertoken}&filter=admin&extended=1&v=5.131"
        )

        return response["response"]["items"]
    

    async def get_group_by_id(
        self,
        group_id: int
    ) -> VKGroupExternal:
        response = await self._get(
            f"https://api.vk.com/method/groups.getById?access_token={self.usertoken}&group_id={group_id}&v=5.131"
        )

        return VKGroupExternal(**response["response"][0])
    

    async def create_post(
        self,
        usertoken: int,
        owner_id: int, # id группы
        message: str,
        attachments: str,
        source: str,
    ):
        pass