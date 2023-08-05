# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from google.cloud.tasks_v2beta2 import types
from google.cloud.tasks_v2beta2.gapic import cloud_tasks_client
from google.cloud.tasks_v2beta2.gapic import enums


class CloudTasksClient(cloud_tasks_client.CloudTasksClient):
    __doc__ = cloud_tasks_client.CloudTasksClient.__doc__
    enums = enums


__all__ = ("enums", "types", "CloudTasksClient")
