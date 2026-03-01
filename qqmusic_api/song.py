"""歌曲相关 API"""

from typing import Any, Optional

from .utils.network import NO_PROCESSOR, api_request


@api_request("music.trackInfo.TrackInfoService", "GetTrackInfo")
async def get_song_info(mid: str):
    """获取歌曲信息

    Args:
        mid: 歌曲 mid
    """
    return {"musicId": mid}, NO_PROCESSOR


@api_request("music.song.SongService", "GetDownloadInfo")
async def get_download_info(mid: str, br: int = 320):
    """获取歌曲下载信息

    Args:
        mid: 歌曲 mid
        br: 比特率，默认 320
    """
    return {
        "musicId": mid,
        "br": br,
        "type": "mp3",
    }, NO_PROCESSOR


@api_request("music.song.SongService", "GetPlayUrl")
async def get_play_url(mid: str, br: int = 320):
    """获取歌曲播放链接

    Args:
        mid: 歌曲 mid
        br: 比特率，默认 320
    """
    return {
        "musicId": mid,
        "br": br,
        "type": "mp3",
    }, NO_PROCESSOR
