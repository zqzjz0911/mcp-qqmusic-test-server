"""歌单相关 API"""

from typing import Any

from .utils.network import NO_PROCESSOR, api_request


@api_request("music.playlist.PlayListService", "GetPlaylistDetail")
async def get_playlist_detail(id: str):
    """获取歌单详情

    Args:
        id: 歌单 id
    """
    return {"id": id}, NO_PROCESSOR


@api_request("music.playlist.PlayListService", "GetPlaylistSongList")
async def get_playlist_songs(id: str, page: int = 1, num: int = 50):
    """获取歌单歌曲列表

    Args:
        id: 歌单 id
        page: 页码
        num: 返回数量
    """
    return {
        "id": id,
        "pageNum": page - 1,
        "pageSize": num,
    }, NO_PROCESSOR


@api_request("music.playlist.PlayListService", "GetHotPlayList")
async def get_hot_playlists(page: int = 1, num: int = 20):
    """获取热门歌单

    Args:
        page: 页码
        num: 返回数量
    """
    return {
        "pageNum": page - 1,
        "pageSize": num,
    }, NO_PROCESSOR
