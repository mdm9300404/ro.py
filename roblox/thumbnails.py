from enum import Enum
from typing import Optional
from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject


class ThumbnailState(Enum):
    completed = "Completed"
    in_review = "InReview"
    pending = "Pending"
    error = "Error"
    moderated = "Moderated"


class ThumbnailReturnPolicy(Enum):
    place_holder = "PlaceHolder"
    auto_generated = "AutoGenerated"
    force_auto_generated = "ForceAutoGenerated"


class ThumbnailFormat(Enum):
    png = "Png"
    jpeg = "Jpeg"


class AvatarThumbnailType(Enum):
    full_body = 1
    headshot = 2
    bust = 3


class Thumbnail:
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.target_id: int = data["targetId"]
        self.state: ThumbnailState = ThumbnailState(data["state"])
        self.image_url: Optional[str] = data["imageUrl"]


class UniverseThumbnail:
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.universe_id: int = data["universeId"]
        self.error: Optional[str] = data["error"]
        self.thumbnails: list[Thumbnail] = [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in data["thumbnails"]
        ]


class ThumbnailProvider:
    def __init__(self, shared: ClientSharedObject):
        self._shared: ClientSharedObject = shared

    async def get_asset_thumbnails(
        self,
        asset_ids: list[int],
        return_policy: ThumbnailReturnPolicy = ThumbnailReturnPolicy.place_holder,
        size: str = "30x30",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/assets"),
            params={
                "assetIds": asset_ids,
                "returnPolicy": return_policy.value,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_asset_thumbnail_3d(self, asset_id: int) -> Thumbnail:
        thumbnail_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "thumbnails", "v1/assets-thumbnail-3d"
            ),
            params={"assetId": asset_id},
        )
        thumbnail_data = thumbnail_response.json()
        return Thumbnail(shared=self._shared, data=thumbnail_data)

    async def get_badge_icons(
        self,
        badge_ids: list[int],
        size: str = "150x150",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/badges/icons"),
            params={
                "badgeIds": badge_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_bundle_thumbnails(
        self,
        bundle_ids: list[int],
        size: str = "150x150",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "thumbnails", "v1/bundles/thumbnails"
            ),
            params={
                "bundleIds": bundle_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_gamepass_icons(
        self,
        gamepass_ids: list[int],
        size: str = "150x150",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/game-passes"),
            params={
                "gamePassIds": gamepass_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_universe_icons(
        self,
        universe_ids: list[int],
        return_policy: ThumbnailReturnPolicy = ThumbnailReturnPolicy.place_holder,
        size: str = "50x50",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/games/icons"),
            params={
                "universeIds": universe_ids,
                "returnPolicy": return_policy.value,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_universe_thumbnails(
        self,
        universe_ids: list[int],
        size: str = "768x432",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
        count_per_universe: int = None,
        defaults: bool = None,
    ) -> list[UniverseThumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "thumbnails", "v1/games/multiget/thumbnails"
            ),
            params={
                "universeIds": universe_ids,
                "countPerUniverse": count_per_universe,
                "defaults": defaults,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            UniverseThumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_group_icons(
        self,
        group_ids: list[int],
        size: str = "150x150",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/groups/icons"),
            params={
                "groupIds": group_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_place_icons(
        self,
        place_ids: list[int],
        return_policy: ThumbnailReturnPolicy = ThumbnailReturnPolicy.place_holder,
        size: str = "50x50",
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/places/gameicons"),
            params={
                "placeIds": place_ids,
                "returnPolicy": return_policy.value,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )
        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_user_avatars(
        self,
        user_ids: list[int],
        type: AvatarThumbnailType = AvatarThumbnailType.full_body,
        size: str = None,
        format: ThumbnailFormat = ThumbnailFormat.png,
        is_circular: bool = False,
    ) -> list[Thumbnail]:
        uri: str
        if type == AvatarThumbnailType.full_body:
            uri = "avatar"
            size = size or "30x30"
        elif type == AvatarThumbnailType.bust:
            uri = "avatar-bust"
            size = size or "48x48"
        elif type == AvatarThumbnailType.headshot:
            uri = "avatar-headshot"
            size = size or "48x48"
        else:
            raise ValueError("Avatar type is invalid.")

        thumbnails_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", f"v1/users/{uri}"),
            params={
                "userIds": user_ids,
                "size": size,
                "format": format.value,
                "isCircular": is_circular,
            },
        )

        thumbnails_data = thumbnails_response.json()["data"]
        return [
            Thumbnail(shared=self._shared, data=thumbnail_data)
            for thumbnail_data in thumbnails_data
        ]

    async def get_user_avatar_3d(self, user_id: int) -> Thumbnail:
        thumbnail_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("thumbnails", "v1/users/avatar-3d"),
            params={"userId": user_id},
        )
        thumbnail_data = thumbnail_response.json()
        return Thumbnail(shared=self._shared, data=thumbnail_data)
