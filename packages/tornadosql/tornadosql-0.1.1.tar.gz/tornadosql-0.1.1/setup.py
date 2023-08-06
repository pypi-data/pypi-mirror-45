#!/usr/bin/env python
#
# Copyright wangxinxing961129@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core

version = "0.1.1"

distutils.core.setup(
    name="tornadosql",
    version=version,
    license = 'https://www.apache.org/licenses/LICENSE-2.0',
    py_modules=["tornadosql"],
    author="wxx",
    author_email="wangxinxing961129@gmail.com",
    url="https://github.com/oouxx/tornadosql",
    description="A lightweight wrapper around pymysql to support python3",
    download_url = 'https://codeload.github.com/oouxx/tornadosql/tar.gz/v0.1.1',
    install_requires=[
        'pymysql']
    )
