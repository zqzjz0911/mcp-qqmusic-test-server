import asyncio
from qqmusic_api import search, singer
from qqmusic_api.search import SearchType
from mcp.server.fastmcp import FastMCP
import json

# Initialize FastMCP server
mcp = FastMCP("mcp-qqmusic-test-server")

@mcp.tool()
async def search_music(keyword: str, page: int = 1, num: int = 20):
    """
    Search for music tracks
    
    Args:
        keyword: Search keyword or phrase
        page: Page number for pagination (default: 1)
        num: Maximum number of results to return (default: 20)
        
    Returns:
        List of music tracks matching the search criteria
    """
    result = await search.search_by_type(keyword=keyword, page=page, num=num)
    
    # 提取指定字段
    # json.dumps(result, ensure_ascii=False) - 这行代码没有实际作用，因为结果没有被使用
    if isinstance(result, list):
        filtered_list = []
        for item in result:
            # 提取歌曲信息而不是专辑信息
            song_info = {
                "id": item.get("id"),
                "mid": item.get("mid"),
                "name": item.get("name"),
                "pmid": item.get("pmid", ""),
                "subtitle": item.get("subtitle", ""),
                "time_public": item.get("time_public", ""),
                "title": item.get("title", item.get("name", ""))
            }
            filtered_list.append(song_info)
    
    return filtered_list


@mcp.tool()
async def search_songs_by_singer(singer_name: str, page: int = 1, num: int = 20, order: int = 1):
    """
    Search for songs by singer name
    
    Args:
        singer_name: Singer name to search for
        page: Page number for pagination (default: 1)
        num: Maximum number of results to return (default: 20)
        order: Sort order (0: newest, 1: most popular) (default: 1)
        
    Returns:
        List of songs by the specified singer
    """
    singer_result = await search.search_by_type(keyword=singer_name, search_type=SearchType.SINGER, num=1)
    
    if not singer_result or len(singer_result) == 0:
        return []
    
    singer_mid = singer_result[0].get("singerMID") or singer_result[0].get("mid")
    if not singer_mid:
        return []
    
    songs_result = await singer.get_songs(mid=singer_mid, page=page, num=num, order=order)
    
    if not songs_result or not isinstance(songs_result, list):
        return []
    
    filtered_list = []
    for item in songs_result:
        
        singer_names = []
        singer_mids = []
        for _singer in item.get("singer", []):
            singer_names.append(_singer.get("name"))
            singer_mids.append(_singer.get("mid"))
        # 提取歌曲信息
        song_info = {
            "mid": item.get("mid"),
            "name": item.get("name"),
            "title": item.get("title", item.get("name", "")),
            "album_title": item.get("album", {}).get("name", ""),
            "album_mid": item.get("album", {}).get("mid", ""),
            "time_public": item.get("album", {}).get("time_public", ""),
            "singer_name": singer_names,
            "singer_mids": singer_mids
        }
        filtered_list.append(song_info)
    
    return filtered_list


if __name__ == "__main__":
    mcp.run(transport='stdio')
