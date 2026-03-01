"""专辑相关 API"""

from typing import Any

from .utils.network import NO_PROCESSOR, api_request


@api_request("music.album.AlbumService", "GetAlbumDetail")
async def get_album_detail(mid: str):
    """获取专辑详情

    Args:
        mid: 专辑 mid
    """
    return {"albumMid": mid}, NO_PROCESSOR


@api_request("music.album.AlbumService", "GetAlbumSongList")
async def get_album_songs(mid: str, page: int = 1, num: int = 50):
    """获取专辑歌曲列表

    Args:
        mid: 专辑 mid
        page: 页码
        num: 返回数量
    """
    return {
        "albumMid": mid,
        "pageNum": page - 1,
        "pageSize": num,
    }, NO_PROCESSOR
