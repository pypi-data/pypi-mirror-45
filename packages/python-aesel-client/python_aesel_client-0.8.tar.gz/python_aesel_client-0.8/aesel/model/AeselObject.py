#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
An Object is represented by a transformation matrix representing it’s position
in 3-space, as well as a collection of Assets (Mesh files, Texture files,
Shader scripts, etc.). Objects are meant to be interacted with by individual
devices, and these changes will be streamed to all devices via the
Event API. This API exposes CRUD and Query operations for Objects.

Objects may also have a frame/timestamp, as well as animation graph handles.
Both of these are, however, optional.

:key: The Unique ID of the Object, assigned by Aesel.
:name: The Name of the Object.
:scene: The ID of the Scene which contains the Object.
:type: The type of the object (ie. "mesh", "curve", etc).
:subtype: The subtype of the object (ie. "cube", "sphere", etc).
:frame: The integer frame of the object
:transform: The transformation matrix of the object, in a single array.  The first four elements make up the first row of the matrix, and this pattern continues.
:actions: An array of AeselAction instances.
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

class AeselObject(object):
    def __init__(self):
        self.key = None
        self.name = None
        self.scene = None
        self.type = None
        self.subtype = None
        self.transform = []
        self.actions = []

    def to_dict(self):
        return_dict = copy.deepcopy(vars(self))
        return_dict["actions"] = [action.to_dict() for action in self.actions]
        return return_dict

    def to_transform_json(self, mtype=1):
        msg_dict = {
                    "msg_type": mtype,
                    "key":self.key,
                    "name":self.name,
                    "scene":self.scene,
                    "transform": self.transform
                    }
        msg_dict["actions"] = [action.to_dict() for action in self.actions]
        return json.dumps(msg_dict)
