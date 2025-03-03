from typing import Any

from telicent_lib import Record
from telicent_lib.sinks import DataSink

__license__ = """
Copyright (c) Telicent Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class DictionarySink(DataSink):
    """
    A Data Sink backed by a Dictionary intended for test and development purposes only
    """

    def __init__(self):
        super().__init__("Dictionary")
        self.data: dict[Any, Any] = {}

    def send(self, record: Record):
        if record is None:
            return
        self.data[record.key] = record.value

    def get(self) -> dict[Any, Any]:
        """Gets the underlying dictionary"""
        return self.data

    def __str__(self):
        return "In-Memory Dictionary"
