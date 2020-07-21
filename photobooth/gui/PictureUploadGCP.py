#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Photobooth - a flexible photo booth software
# Copyright (C) 2018  Balthasar Reuter <photobooth at re - web dot eu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
import requests

from pathlib import Path

from photobooth.worker.WorkerTask import WorkerTask
from google.cloud.storage import Client


class PictureUploadGCP(WorkerTask):

    def __init__(self, config):

        super().__init__()

        if config.getBool('UploadWebdav', 'enable_gcp'):
            self._project = config.get('UploadWebdav', 'project')
            service_account_location = str(config.get('UploadWebdav', 'service_account'))
            if (len(service_account_location) != 0):
                self._client = Client.from_service_account_json(service_account_location)
            self._bucket = config.get('UploadWebdav', 'bucket')


    def do(self, picture, filename):

        print("Uploading the picture now!")
        storage_client = self._client
        bucket = storage_client.bucket(self._bucket)
        blob = bucket.blob(filename)
        blob.upload_from_string(picture.getvalue())
        print(blob.public_url)
        return blob.public_url