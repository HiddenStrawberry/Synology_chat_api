import random
import requests
from requests_toolbelt import MultipartEncoder

from synology_dsm import SynologyDSM

DSM_IP = "192.168.1.1"
DSM_PORT = 5001
DSM_ADMIN_USERNAME = "admin"
DSM_ADMIN_PASSWORD = "test"


def chat_send_files(message="", file_path="", channel_id=0):
    """

    :param message: 要发送的图片附带的消息
    :param file_path: 要发送的文件路径
    :param channel_id: 频道ID,可从频道对应的URL中得到,先进入网页端Chat,如 https://10.10.10.185:8888/#channels/1，那么channel就是1
    :return:
    """

    api = SynologyDSM(
        DSM_IP,
        DSM_PORT,
        DSM_ADMIN_USERNAME,
        DSM_ADMIN_PASSWORD,
        use_https=True,
        verify_ssl=False,
        timeout=None,
        device_token=None,
        debugmode=True)
    api.login()
    sid = api._session_id

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'X-SYNO-TOKEN': '2HJ4b0qsoErPo',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryJak4Kk5l5FU4kznM',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://{DSM_IP}:{DSM_PORT}/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = (
        ('api', 'SYNO.Chat.Post'),
        ('method', 'create'),
        ('version', '5'),
        ('channel_id', channel_id),
        ('ds_file', 'null'),
        ('is_thread', 'null'),
        ('thread_id', 'null'),
        ('_sid', sid)

    )

    multipart_encoder = MultipartEncoder(

        fields={
            "file": (file_path.split('.')[0], open(file_path, "rb"), 'application/octet-stream'),
            "type": "file",
            "message": message,
            "conn_id": ""
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    headers['Content-Type'] = multipart_encoder.content_type

    response = requests.post(f'https://{DSM_IP}:{DSM_PORT}/webapi/entry.cgi', params=params, headers=headers,
                             data=multipart_encoder,
                             verify=False)
    print(response.json())


if __name__ == "__main__":
    chat_send_files(message="", file_path="", channel_id=0)
