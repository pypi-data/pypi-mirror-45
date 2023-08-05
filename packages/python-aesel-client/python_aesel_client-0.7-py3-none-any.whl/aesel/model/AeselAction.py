#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
An Action represents a unique set of keyframes on an object or property.  In
either case, it is expected that there can be multiple actions associated to
a parent object.

Some examples of actions are 'walk', 'run', 'jump', etc.  These are commonly
used by animators to build out core movements, and then the actions are woven
together to create the final effects.

:name: The Name of the action.
:description: A description of the action.
:keyframes: An array of AeselFrame instances.
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

class AeselAction(object):
    def __init__(self):
        self.name = None
        self.description = None
        self.keyframes = []

    def to_dict(self):
        return_dict = copy.deepcopy(vars(self))
        return_dict['keyframes'] = [frame.to_dict() for frame in self.keyframes]
        return return_dict
