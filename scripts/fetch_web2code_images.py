#!/usr/bin/env python3
"""Web2Code 样例截图：HF 上的图片全在一个 29.6 GB 的 Web2Code_image.zip 里，
这里用 HTTP Range 只读 zip 目录和要用的几张图，不下整包。

用法：python3 scripts/fetch_web2code_images.py   -> middle_processing/samples_src/web2code/<原文件名>
"""
import json
import os
import time
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, 'middle_processing', 'samples_src', 'web2code')
URL = 'https://huggingface.co/datasets/MBZUAI/Web2Code/resolve/main/Web2Code_image.zip'
PICK = (0, 3, 7)   # 与 build_samples.web2code() 选的三条一致


def get(url, start, end):
    req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}'})
    for i in range(5):
        try:
            return urllib.request.urlopen(req, timeout=300)
        except OSError:
            time.sleep(2 ** i)
    raise RuntimeError(f'Range {start}-{end} 连续失败')


class HttpFile:
    """只读、可 seek 的远程文件，每次 read 发一个 Range 请求；zipfile 只需要这几个方法"""

    def __init__(self, url):
        with get(url, 0, 0) as r:
            self.url = r.geturl()                      # 跟一次跳转，之后直连 CDN
            self.size = int(r.headers['Content-Range'].rsplit('/', 1)[1])
        self.pos = 0

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = (off, self.pos + off, self.size + off)[whence]
        return self.pos

    def read(self, n=-1):
        end = self.size if n is None or n < 0 else min(self.size, self.pos + n)
        if end <= self.pos:
            return b''
        with get(self.url, self.pos, end - 1) as r:
            data = r.read()
        self.pos += len(data)
        return data


def main():
    recs = json.load(open(os.path.join(DST, 'samples.json'), encoding='utf-8'))
    want = {recs[i]['image'] for i in PICK}
    zf = zipfile.ZipFile(HttpFile(URL))
    print(f'zip 目录 {len(zf.infolist())} 条')
    for info in zf.infolist():
        hit = next((w for w in want if info.filename.endswith(w)), None)
        if hit:
            out = os.path.join(DST, os.path.basename(hit))
            open(out, 'wb').write(zf.read(info))
            print(f'  {info.filename} -> {out}  {info.file_size} B')
            want.discard(hit)
    if want:
        print('没找到：', *sorted(want))


if __name__ == '__main__':
    main()

