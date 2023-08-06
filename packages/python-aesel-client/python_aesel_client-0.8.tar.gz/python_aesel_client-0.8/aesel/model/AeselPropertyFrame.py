#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A Property Frame represents a single keyframe within a Property Action.

:frame: The integer frame of the object
:values: An array of PropertyValue instances.
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

class AeselPropertyFrame(object):
    def __init__(self):
        self.frame = None
        self.values = []

    def to_dict(self):
        return_dict = copy.deepcopy(vars(self))
        return_dict['values'] = [vars(val) for val in self.values]
        return return_dict
