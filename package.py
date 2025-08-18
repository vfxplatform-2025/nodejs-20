# -*- coding: utf-8 -*-
name        = "nodejs"
version     = "20.9.0"
authors     = ["M83"]
description = "Node.js 16 LTS, compatible with Chromium/QtWebEngine builds"

build_requires = [
    "gcc-11.5.0",
    "python-3.13.2",    # VFX 플랫폼 통일 파이썬
]

requires = [
    # 필요 시 OpenSSL, zlib, ICU 등 명시 가능
]

build_command = "python {root}/rezbuild.py install"

def commands():
    env.NodeJS_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.prepend("{root}/lib")

