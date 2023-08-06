#!/usr/bin/env python3

import baker
import sys
import os
from websocket import create_connection
from json import loads, dumps
from sjcl import SJCL, sjcl
from base64 import b64decode, b64encode

MAGIC = "XXMOJOXX"
CHUNK_SIZE = 2*1000*1000


@baker.command(
    params={
        "filepath": "path to local file to encrypt and upload",
        "url": "URL of the Lufi service, eg: https://framadrop.org/",
        "delay": "delay after which file is deleted on server, in days",
        "del_at_first_view": "delete file after first successful download", })
def upload(filepath, url, delay=None, del_at_first_view=False):
    key = b64encode(sjcl.get_random_bytes(32))
    size = os.path.getsize(filepath)
    (e, r) = divmod(size, CHUNK_SIZE)
    totalparts = e + [0, 1][r > 0]
    meta = {"name": filepath.split("/")[-1],
            "size": size,
            "total": totalparts,
            "i": 0,
            "del_at_first_view": del_at_first_view}
    f = open(filepath, "rb")
    wsurl = url.replace("http", "ws")+"upload/"
    ws = create_connection(wsurl)
    for (i, data) in enumerate(iter(lambda: f.read(CHUNK_SIZE), b"")):
        meta["part"] = i
        data = SJCL().encrypt(b64encode(data), key)  # b64 is unnecessary be kept for compatibility
        for k in data.keys():
            if isinstance(data[k], bytes):  # b64encode produces bytes
                data[k] = data[k].decode("ascii")
        ws.send(payload=dumps(meta)+MAGIC+dumps(dumps(data)))  # second dumps is unnecessary be kept for compatibility
        result = ws.recv()
        print(result, file=sys.stderr)
        result = loads(result)
        meta["id"] = result["short"]
    ws.close()
    print("download_url "+url+"r/"+meta["id"]+"#"+key.decode("ascii"))
    print("delete_url "+url+"d/"+meta["id"]+"/"+result["token"])


@baker.command(
    params={
        "url": "download link given by the upload function", })
def download(url):
    [url, key] = url.split('#')
    url = url.replace("http", "ws").replace("/r/", "/download/")
    ws = create_connection(url)
    p = 0
    t = 1
    while p < t:
        ws.send('{"part":%d}' % p)
        result = ws.recv()
        idx = result.find(MAGIC)
        meta = loads(result[0:idx])
        print(meta, file=sys.stderr)
        data = loads(loads(result[idx+len(MAGIC):]))  # second loads is unnecessary be kept for compatibility
        t = meta["total"]
        f = open(meta["name"].split("/")[-1], "ab")
        f.write(b64decode(SJCL().decrypt(data, key)))  # b64 is unnecessary be kept for compatibility
        p += 1
    ws.close()


def main():
    baker.run()


if __name__ == "__main__":
    main()
