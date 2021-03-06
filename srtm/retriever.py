# -*- coding: utf-8 -*-

# Copyright 2013 Tomo Krajina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging        as mod_logging
import urllib.request as mod_urllib
import re             as mod_re
from typing import *

def retrieve_all_files_urls(url: str) -> Dict[str, str]:
    mod_logging.info('Retrieving {0}'.format(url))
    url_stream = mod_urllib.urlopen(url)
    contents = url_stream.read()
    url_stream.close()

    url_candidates = mod_re.findall('href="(.*?)"', contents)
    urls: Dict[str, str] = {}

    for url_candidate in url_candidates:
        if url_candidate.endswith('/') and not url_candidate in url:
            files_url = '{0}/{1}'.format(url, url_candidate)

            urls.update(get_files(files_url))

    return urls

def get_files(url: str) -> Dict[str, str]:
    mod_logging.info('Retrieving {0}'.format(url))
    url_stream = mod_urllib.urlopen(url)
    contents = url_stream.read()
    url_stream.close()

    result: Dict[str, str] = {}

    url_candidates = mod_re.findall('href="(.*?)"', contents)
    for url_candidate in url_candidates:
        if url_candidate.endswith('.hgt.zip'):
            file_url = '{0}/{1}'.format(url, url_candidate)
            result[url_candidate.replace('.zip', '')] = file_url

    mod_logging.info('Found {0} files'.format(len(result)))

    return result
