from typing import Any, List
import urllib.request
import json

latest_feed_url = "https://v2ex.com/api/topics/latest.json"
node_feed_url_template = "https://www.v2ex.com/feed/%s.json"


def get(url: str) -> Any:
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36")
    return json.load(urllib.request.urlopen(request))


def get_latest_feed(url: str) -> List:
    resp = get(latest_feed_url)
    items = []
    for item in resp:
        try:
            items.append({
                'uid'           : item["id"],
                'title'         : item["title"],
                'subtitle'      : item["content"],
                'arg'           : item['url'], 
                'description'   : "test",
                'icon'          : 'icon.png',
            })
        except:
            pass
    return items


def get_node_feed(url):
    resp = get(url)
    items = []
    for item in resp["items"]:
        try:
            items.append({
                'uid'           : item["id"],
                'title'         : item["title"],
                'subtitle'      : item["content_html"],
                'arg'           : item['url'], 
                'description'   : "test",
                'icon'          : 'icon.png',
            })
        except:
            pass
    return items


def get_items(argv: str = None):
    if argv:
        url = node_feed_url_template % argv
        items = get_node_feed(url)
    else:
        items = get_latest_feed(latest_feed_url)

    return json.dumps({"items": items})

