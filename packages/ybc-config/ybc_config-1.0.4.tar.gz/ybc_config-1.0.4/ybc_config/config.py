import os
from PIL import Image

profiles_config = {
    "online": {
        "prefix": "https://www.yuanfudao.com",
        "prefix-oss": "https://ybc-online.oss-cn-beijing.aliyuncs.com",
        "websocket": "wss://www.yuanfudao.com/tutor-ybc-sandbox-agent-server/api/ws"
    },
    "test": {
        "prefix": "https://ke.yuanfudao.ws",
        "prefix-oss": "https://ybc-test.oss-cn-beijing.aliyuncs.com",
        "websocket": "ws://ke.yuanfudao.ws/tutor-ybc-sandbox-agent-server/api/ws"
    },
    "local": {
        "prefix": "http://local.yuanfudao.ws:8080",
        "prefix-oss": "https://ybc-test.oss-cn-beijing.aliyuncs.com",
        "websocket": "ws://local.yuanfudao.ws:8080/tutor-ybc-sandbox-agent-server/api/ws"
    }
}
config = {}

uri = '/tutor-ybc-course-api-v2/api'

__DEFAULT_PIC_MAX_LENGTH = 500


def resize_if_too_large(filename):

    file = os.path.abspath(filename)
    im = Image.open(file)
    original_width, original_height = im.size
    max_len = max(original_width, original_height)

    if max_len <= __DEFAULT_PIC_MAX_LENGTH:
        return
    ratio = __DEFAULT_PIC_MAX_LENGTH / max_len
    new_size = (original_width * ratio, original_height * ratio)
    im.thumbnail(new_size)
    im.save(filename, 'PNG')


def _read_config(key):
    return os.environ[key] if key in os.environ else None


ybc_profile = _read_config("YBC_PROFILE")
if ybc_profile is not None and ybc_profile in profiles_config:
    config = profiles_config[ybc_profile]
else:
    config = profiles_config["online"]


