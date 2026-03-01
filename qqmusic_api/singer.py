"""歌手相关 API"""

from enum import Enum
from typing import Any, Literal, cast

from .utils.network import NO_PROCESSOR, RequestGroup, api_request


class AreaType(Enum):
    """地区类型枚举"""

    ALL = -100
    CHINA = 200
    TAIWAN = 2
    AMERICA = 5
    JAPAN = 4
    KOREA = 3


class GenreType(Enum):
    """风格类型枚举"""

    ALL = -100
    POP = 7
    RAP = 3
    CHINESE_STYLE = 19
    ROCK = 4
    ELECTRONIC = 2
    FOLK = 8
    R_AND_B = 11
    ETHNIC = 37
    LIGHT_MUSIC = 93
    JAZZ = 14
    CLASSICAL = 33
    COUNTRY = 13
    BLUES = 10


class SexType(Enum):
    """性别类型枚举"""

    ALL = -100
    MALE = 0
    FEMALE = 1
    GROUP = 2


class TabType(Enum):
    """Tab 类型枚举"""

    WIKI = ("wiki", "IntroductionTab")
    ALBUM = ("album", "AlbumTab")
    COMPOSER = ("song_composing", "SongTab")
    LYRICIST = ("song_lyric", "SongTab")
    PRODUCER = ("producer", "SongTab")
    ARRANGER = ("arranger", "SongTab")
    MUSICIAN = ("musician", "SongTab")
    SONG = ("song_sing", "SongTab")
    VIDEO = ("video", "VideoTab")

    def __init__(self, tab_id: str, tab_name: str):
        self.tab_id = tab_id
        self.tab_name = tab_name


class IndexType(Enum):
    """首字母索引枚举"""

    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8
    I = 9
    J = 10
    K = 11
    L = 12
    M = 13
    N = 14
    O = 15
    P = 16
    Q = 17
    R = 18
    S = 19
    T = 20
    U = 21
    V = 22
    W = 23
    X = 24
    Y = 25
    Z = 26
    ALL = -100
    HASH = 27


def validate_int_enum(value: int | Enum, enum_type: type[Enum]) -> int:
    """确保传入的值符合指定的枚举类型"""
    if isinstance(value, enum_type):
        return value.value
    if value in {item.value for item in enum_type}:
        return cast(int, value)
    raise ValueError(f"Invalid value: {value} for {enum_type.__name__}")


@api_request("music.musichallSinger.SingerList", "GetSingerList")
async def get_singer_list(
    area: int | AreaType = AreaType.ALL,
    sex: int | SexType = SexType.ALL,
    genre: int | GenreType = GenreType.ALL,
):
    """获取歌手列表

    Args:
        area: 地区
        sex: 性别
        genre: 风格
    """
    area = validate_int_enum(area, AreaType)
    sex = validate_int_enum(sex, SexType)
    genre = validate_int_enum(genre, GenreType)
    return {
        "hastag": 0,
        "area": area,
        "sex": sex,
        "genre": genre,
    }, lambda data: cast(
        list[dict[str, Any]],
        data["hotlist"],
    )


@api_request("music.UnifiedHomepage.UnifiedHomepageSrv", "GetHomepageTabDetail")
async def get_tab_detail(mid: str, tab_type: TabType, page: int = 1, num: int = 10, order: int = 0):
    """获取歌手 Tab 详细信息

    Args:
        mid: 歌手 mid
        tab_type: Tab 类型
        page: 页码
        num: 返回数量
        order: 排序方式，0-默认，1-最新
    """
    params = {
        "SingerMid": mid,
        "IsQueryTabDetail": 1,
        "TabID": tab_type.tab_id,
        "PageNum": page - 1,
        "PageSize": num,
        "Order": order,
    }

    def _processor(data: dict[str, Any]) -> list[dict[str, Any]]:
        data = data[tab_type.tab_name]
        return data.get("List", data.get("VideoList", data.get("AlbumList", data)))

    return params, _processor


async def get_songs(
    mid: str,
    tab_type: Literal[
        TabType.SONG,
        TabType.ALBUM,
        TabType.COMPOSER,
        TabType.LYRICIST,
        TabType.PRODUCER,
        TabType.ARRANGER,
        TabType.MUSICIAN,
    ] = TabType.SONG,
    page: int = 1,
    num: int = 10,
    order: int = 0,
) -> list[dict[str, Any]]:
    """获取歌手歌曲

    Args:
        mid: 歌手 mid
        tab_type: Tab 类型
        page: 页码
        num:  返回数量
        order: 排序方式，0-默认，1-最新
    """
    return await get_tab_detail(mid, tab_type, page, num, order)
