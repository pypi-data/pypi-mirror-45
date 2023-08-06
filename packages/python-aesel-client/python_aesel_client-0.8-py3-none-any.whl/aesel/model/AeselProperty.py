#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A Property is a set of between 1 and 4 double values, which may or not be
associated to objects. Properties can also support frames and/or timestamps,
just like objects, but cannot be locked and have no transformations.

Properties are meant to be interacted with by individual devices, and these
changes will be streamed to other devices via the Events API. In addition,
Create and Update messages sent to the HTTP API are converted to events and
streamed out to registered devices.

:key: The Unique ID of the Property, assigned by Aesel.
:name: The Name of the Property.
:parent: The ID of the Parent data entity which contains the Property.
:scene: The ID of the Scene which contains the Property.
:asset_sub_id: The ID of the Property within a parent asset.
:frame: The integer frame of the Property.
:actions: An array of AeselPropertyFrame instances.
:values: An array of AeselPropertyValue instances.
"""

"""
Apache2 License Notice
Copyright 2018 Alex Barry
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

import copy
import json

class AeselProperty(object):
    def __init__(self):
        self.key = None
        self.name = None
        self.parent = None
        self.asset_sub_id = None
        self.scene = None
        self.actions = []
        self.values = []

    def to_dict(self):
        return_dict = copy.deepcopy(vars(self))
        return_dict["actions"] = [action.to_dict() for action in self.actions]
        return return_dict

    def to_transform_json(self, mtype=9):
        msg_dict = {
                    "msg_type": mtype,
                    "key":self.key,
                    "name":self.name,
                    "scene":self.scene,
                    "values": self.values
                    }
        msg_dict["actions"] = [action.to_dict() for action in self.actions]
        return json.dumps(msg_dict)
