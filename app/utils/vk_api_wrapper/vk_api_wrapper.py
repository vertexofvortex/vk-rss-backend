from io import BytesIO
import aiohttp
import requests

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
        group_id: int,
        message: str,
        image: BytesIO,
        image_filename: str,
        copyright: str,
    ):
        # Step 1: getting the upload server

        upload_server = await self._get(
            f"https://api.vk.com/method/photos.getWallUploadServer?access_token={self.usertoken}&group_id={group_id}&v=5.131"
        )

        # Step 2: sending image to the upload server
        # TODO: make request asynchronously via aiohttp

        send_image = requests.post(
            upload_server["response"]["upload_url"],
            files={ "photo": (image_filename, image) }
        )

        # Step 3: saving the image we've sent to the group album

        photo: str = send_image.json()["photo"]
        hash: str = send_image.json()["hash"]
        server: str = send_image.json()["server"]

        save_image = await self._get(
            f"https://api.vk.com/method/photos.saveWallPhoto?access_token={self.usertoken}&group_id={group_id}&photo={photo}&server={server}&hash={hash}&v=5.131"
        )

        # Step 4: publish a new post

        photo_id = save_image["response"][0]["id"]
        owner_id = save_image["response"][0]["owner_id"]
        print(f"photo_{owner_id}_{photo_id}")

        publish_post = await self._get(
            f"https://api.vk.com/method/wall.post?access_token={self.usertoken}&owner_id=-{group_id}&from_group=1&attachments=photo{owner_id}_{photo_id}&message={message}&copyright={copyright}&v=5.131"
        )

        return True

        #print(upload_server["response"]["upload_url"])

        # async with aiohttp.ClientSession() as session:
        #     with aiohttp.MultipartWriter() as mp_writer:
        #         mp_writer.append_form({
        #             "photo": image,
        #         }, { "Content-Type": "multipart/form-data" })

        #         async with session.post(
        #             upload_server["response"]["upload_url"],
        #             data=mp_writer
        #         ) as response:
        #             # Ignoring MIME type because VK API thinks
        #             # that it's sending me plain HTML
        #             result = await response.json(content_type=None)

        #             print(result)

        # await self._get(
        #     f"https://api.vk.com/method/wall.post?access_token={self.usertoken}&owner_id={group_id}&message={message}&"
        # )