#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
An Object Frame represents a single keyframe within an Object Action.

:frame: The integer frame of the object
:transform: The transformation matrix of the object, in a single array.  The first four elements make up the first row of the matrix, and this pattern continues.
:translation_handle: An array of AnimationGraphHandle's which correspond to the [x,y,z] values in the translation array.
:rotation_handle: An array of 4 AnimationGraphHandle's which correspond to the [w,x,y,z] values in the rotation arrays.
:scale_handle: An array of 3 AnimationGraphHandle's which correspond to the [x,y,z] values in the scale array.
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

class AeselObjectFrame(object):
    def __init__(self):
        self.frame = None
        self.transform = []
        self.translation_handle = []
        self.rotation_handle = []
        self.scale_handle = []

    def to_dict(self):
        return_dict = copy.deepcopy(vars(self))
        return_dict['translation_handle'] = [vars(handle) for handle in self.translation_handle]
        return_dict['rotation_handle'] = [vars(handle) for handle in self.rotation_handle]
        return_dict['scale_handle'] = [vars(handle) for handle in self.scale_handle]
        return return_dict
