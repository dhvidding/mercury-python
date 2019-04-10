# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Accenture Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import uuid
import msgpack


class AppException(Exception):

    def __init__(self, status, message):
        Exception.__init__(self, {'status': status, 'message': message})
        self.status = status if isinstance(status, int) else 500
        self.message = str(message)

    def get_status(self):
        return self.status

    def get_message(self):
        return self.message


class EventEnvelope:

    def __init__(self):
        self.event_id = str(uuid.uuid4())
        self.headers = dict()
        self.body = None
        self.status = None
        self.to = None
        self.reply_to = None
        self.correlation_id = None
        self.broadcast = False
        self.exec_time = -1.0
        self.round_trip = -1.0

    def set_event_id(self, event_id: str):
        if isinstance(event_id, str):
            self.event_id = event_id
        else:
            raise ValueError('id must be str')
        return self

    def get_event_id(self):
        return self.event_id

    def set_to(self, to: str):
        self.to = to
        return self

    def get_to(self):
        return self.to

    def get_status(self):
        return self.status if self.status else 200

    def set_status(self, status: int):
        if isinstance(status, int):
            self.status = status
        else:
            raise ValueError('status must be int')
        return self

    def set_reply_to(self, reply_to: str, me=False):
        if isinstance(reply_to, str):
            self.reply_to = ('->' if me else '') + reply_to
        else:
            raise ValueError('reply_to must be str')
        return self

    def get_reply_to(self):
        return self.reply_to

    def set_correlation_id(self, correlation_id: str):
        self.correlation_id = correlation_id if isinstance(correlation_id, str) else str(correlation_id)
        return self

    def get_correlation_id(self):
        return self.correlation_id

    def set_header(self, key: str, value: any):
        self.headers[key] = value if isinstance(value, str) else str(value)
        return self

    def get_header(self, key: str):
        if key in self.headers:
            return self.headers[key]
        else:
            return None

    def get_headers(self):
        return self.headers

    def set_body(self, body: any):
        self.body = body
        return self

    def get_body(self):
        return self.body

    def set_broadcast(self, broadcast: bool):
        self.broadcast = broadcast
        return self

    def is_broadcast(self):
        return self.broadcast

    def get_exec_time(self):
        return self.exec_time

    def set_exec_time(self, exec_time):
        self.exec_time = exec_time
        return self

    def get_round_trip(self):
        return self.round_trip

    def set_round_trip(self, round_trip):
        self.round_trip = round_trip
        return self

    def to_map(self):
        result = dict()
        if self.to:
            result['to'] = self.to
        result['headers'] = dict() if not self.headers else self.headers
        result['id'] = self.event_id
        if self.body:
            result['body'] = self.body
        if self.reply_to:
            result['reply_to'] = self.reply_to
        if self.correlation_id:
            result['cid'] = self.correlation_id
        if self.broadcast:
            result['broadcast'] = True
        if self.status:
            result['status'] = self.status
        if self.exec_time >= 0:
            result['exec_time'] = self.exec_time
        if self.round_trip >= 0:
            result['round_trip'] = self.round_trip
        return result

    def from_map(self, data: dict):
        if 'id' in data and isinstance(data['id'], str):
            self.event_id = data['id']
        if 'to' in data and isinstance(data['to'], str):
            self.to = data['to']
        if 'headers' in data and isinstance(data['headers'], dict):
            self.headers = data['headers']
        if 'body' in data:
            self.body = data['body']
        if 'reply_to' in data and isinstance(data['reply_to'], str):
            self.body = data['reply_to']
        if 'cid' in data:
            self.correlation_id = data['cid']
        if 'status' in data:
            self.status = data['status']
        if 'broadcast' in data:
            self.broadcast = data['broadcast']
        if 'exec_time' in data:
            self.exec_time = data['exec_time']
        if 'round_trip' in data:
            self.round_trip = data['round_trip']
        return self

    def to_bytes(self):
        return msgpack.packb(self.to_map(), use_bin_type=True)

    def from_bytes(self, data):
        return self.from_map(msgpack.unpackb(data, raw=False))
