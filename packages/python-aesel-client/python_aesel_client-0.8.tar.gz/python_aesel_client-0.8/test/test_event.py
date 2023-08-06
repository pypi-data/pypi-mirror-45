# -*- coding: utf-8 -*-

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

import pytest
import time

from aesel.model.AeselGraphHandle import AeselGraphHandle
from aesel.model.AeselObject import AeselObject
from aesel.model.AeselAction import AeselAction
from aesel.model.AeselObjectFrame import AeselObjectFrame
from aesel.model.AeselProperty import AeselProperty
from aesel.model.AeselPropertyFrame import AeselPropertyFrame
from aesel.model.AeselPropertyValue import AeselPropertyValue
from aesel.model.AeselScene import AeselScene
from aesel.model.AeselSceneTransform import AeselSceneTransform
from aesel.model.AeselSceneGroup import AeselSceneGroup
from aesel.model.AeselUserDevice import AeselUserDevice

from aesel.AeselTransactionClient import AeselTransactionClient
from aesel.AeselEventClient import AeselEventClient

# Initial setup of Transaction client
@pytest.fixture
def transaction_client():
    return AeselTransactionClient("http://localhost:8080")

# Initial Setup of Event Client
@pytest.fixture
def event_client():
    return AeselEventClient("localhost", 8762)

# Execute tests on the Property API
def test_property_events(transaction_client, event_client):
    print("Testing Property API")

    # Create a Scene
    print("Creating base scene")
    scn = AeselScene()
    scn.name = "test"
    scn.region = "US-MD"
    scn.latitude = 100.0
    scn.longitude = 100.0
    scn.tags = []
    scn.devices = []
    scn_crt_resp = None
    try:
        scn_crt_resp = transaction_client.create_scene("propEventScene", scn)
    except Exception as e:
        print(e)
        assert(False)
    print(scn_crt_resp)

    # Create a new Property
    print("Create Property")
    prop = AeselProperty()
    prop.name = "testProperty"
    prop.scene = "propEventScene"
    prop.values.append(100.0)
    prop_action = AeselAction()
    prop_action.name = "testPropAction"
    prop_action.description = "this is a Property Action"
    prop_frame_initial = AeselPropertyFrame()
    prop_frame_initial.frame = 1
    pfi_value = AeselPropertyValue()
    pfi_value.value = 100.0
    pfi_value.left_type = "test"
    pfi_value.left_x = 10.0
    pfi_value.left_y = 10.2
    pfi_value.right_type = "test2"
    pfi_value.right_x = 10.1
    pfi_value.right_y = 10.3
    prop_frame_initial.values = [pfi_value]
    prop_action.keyframes = [prop_frame_initial]
    prop.actions = [prop_action]
    prop_crt_resp = None
    try:
        prop_crt_resp = transaction_client.create_property("propTestScene", prop)
    except Exception as e:
        print(e)
        assert(False)
    print(prop_crt_resp)
    assert(len(prop_crt_resp["properties"]) > 0)
    assert(len(prop_crt_resp["properties"][0]["key"]) > 0)
    prop_key = prop_crt_resp["properties"][0]["key"]

    # Send event
    print("Send Property Event")
    evt_prop = AeselProperty()
    evt_prop.key = prop_key
    evt_prop.name = "testPropAction"
    evt_prop.scene = "propEventScene"
    evt_prop.values.append(110.0)
    event_client.send_property_update(evt_prop)

    # Wait for event to process
    time.sleep(1)

    # Check to make sure that the property value is updated
    print("Check Property")
    prop_get_resp = None
    try:
        prop_get_resp = transaction_client.get_property("propEventScene", prop_key)
    except Exception as e:
        print(e)
        assert(False)
    print(prop_get_resp)
    assert(len(prop_get_resp["properties"]) > 0)
    assert(abs(prop_get_resp["properties"][0]["values"][0] - 110.0) < 0.001)

    # Send a Frame update
    print("Send Property Frame Event")
    evt_prop2 = AeselProperty()
    evt_prop2.key = prop_key
    evt_action = AeselAction()
    evt_action.name = "testPropAction"
    evt_frame = AeselPropertyFrame()
    evt_frame.frame = 1
    evt_value = AeselPropertyValue()
    evt_value.value = 103.0
    evt_value.left_type = "test2"
    evt_value.left_x = 15.0
    evt_value.left_y = 16.2
    evt_value.right_type = "test3"
    evt_value.right_x = 17.1
    evt_value.right_y = 18.3
    evt_frame.values = [evt_value]
    evt_action.keyframes = [evt_frame]
    evt_prop2.actions = [evt_action]

    event_client.send_property_frame_update(evt_prop2)

    # Wait for event to process
    time.sleep(1)

    # Check to make sure that the property value is updated
    print("Check Property")
    prop_get_resp2 = None
    try:
        prop_get_resp2 = transaction_client.get_property("propEventScene", prop_key)
    except Exception as e:
        print(e)
        assert(False)
    print(prop_get_resp2)
    assert(len(prop_get_resp2["properties"]) > 0)
    assert(len(prop_get_resp2["properties"][0]["actions"]) > 0)
    assert(len(prop_get_resp2["properties"][0]["actions"][0]["keyframes"]) > 0)
    assert(len(prop_get_resp2["properties"][0]["actions"][0]["keyframes"][0]["values"]) > 0)
    assert(abs(prop_get_resp2["properties"][0]["actions"][0]["keyframes"][0]["values"][0]["value"] - 103.0) < 0.001)

    # Delete a Property
    print("Delete Property")
    try:
        transaction_client.delete_property("propTestScene", prop_key)
    except Exception as e:
        print(e)
        assert(False)

# Execute tests on the Object API
def test_object_events(transaction_client, event_client):
    print("Testing Object API")

    # Create a Scene
    print("Creating base scene")
    scn = AeselScene()
    scn.name = "test"
    scn.region = "US-MD"
    scn.latitude = 100.0
    scn.longitude = 100.0
    scn.tags = []
    scn.devices = []
    scn_crt_resp = None
    try:
        scn_crt_resp = transaction_client.create_scene("objEventScene", scn)
    except Exception as e:
        print(e)
        assert(False)
    print(scn_crt_resp)

    # Create a new Object
    print("Create Object")
    obj = AeselObject()
    obj.name = "testObject"
    obj.scene = "objEventScene"
    obj.type = "mesh"
    obj.subtype = "cube"
    obj_action = AeselAction()
    obj_action.name = "testObjAction"
    obj_action.description = "this is an Object Action"
    obj_frame_initial = AeselObjectFrame()
    obj_frame_initial.frame = 1
    obj_frame_initial.transform = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                                   1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    for i in range(0, 3):
        handle = AeselGraphHandle()
        handle.left_type = "test"
        handle.left_x = 10.0 + i
        handle.left_y = 10.2 + i
        handle.right_type = "test2"
        handle.right_x = 10.1 + i
        handle.right_y = 10.3 + i
        obj_frame_initial.translation_handle.append(handle)
    for i in range(0, 4):
        handle = AeselGraphHandle()
        handle.left_type = "test"
        handle.left_x = 10.0 + i
        handle.left_y = 10.2 + i
        handle.right_type = "test2"
        handle.right_x = 10.1 + i
        handle.right_y = 10.3 + i
        obj_frame_initial.rotation_handle.append(handle)
    for i in range(0, 3):
        handle = AeselGraphHandle()
        handle.left_type = "test"
        handle.left_x = 10.0 + i
        handle.left_y = 10.2 + i
        handle.right_type = "test2"
        handle.right_x = 10.1 + i
        handle.right_y = 10.3 + i
        obj_frame_initial.scale_handle.append(handle)
    obj_action.keyframes = [obj_frame_initial]
    obj.actions = [obj_action]

    obj_crt_resp = None
    try:
        obj_crt_resp = transaction_client.create_object("objEventScene", obj)
    except Exception as e:
        print(e)
        assert(False)
    print(obj_crt_resp)
    assert(len(obj_crt_resp["objects"]) > 0)
    assert(len(obj_crt_resp["objects"][0]["key"]) > 0)
    obj_key = obj_crt_resp["objects"][0]["key"]

    # Send Event
    print("Send Object Event")
    evt_obj = AeselObject()
    evt_obj.key = obj_key
    evt_obj.scene = "objEventScene"
    evt_obj.transform = [2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0]
    event_client.send_object_update(evt_obj)

    # Wait for event to process
    time.sleep(1)

    # Check the current object transform to make sure it updated correctly
    print("Check object event")
    obj_get_resp = None
    try:
        obj_get_resp = transaction_client.get_object("objEventScene", obj_key)
    except Exception as e:
        print(e)
        assert(False)
    print(obj_get_resp)
    assert(len(obj_get_resp["objects"]) > 0)
    assert(abs(obj_get_resp["objects"][0]["transform"][0] - 2.0 < 0.001))

    # Send a Frame Update
    print("Send Object Frame Event")
    evt_obj = AeselObject()
    evt_obj.key = obj_key
    evt_obj_action = AeselAction()
    evt_obj_action.name = "testObjAction"
    evt_obj_frame = AeselObjectFrame()
    evt_obj_frame.frame = 1
    evt_obj_frame.transform = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
                               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    for i in range(0, 3):
        handle = AeselGraphHandle()
        handle.left_type = "test"
        handle.left_x = 10.0 + i
        handle.left_y = 10.2 + i
        handle.right_type = "test2"
        handle.right_x = 10.1 + i
        handle.right_y = 10.3 + i
        evt_obj_frame.translation_handle.append(handle)
    for i in range(0, 4):
        handle = AeselGraphHandle()
        handle.left_type = "test"
        handle.left_x = 10.0 + i
        handle.left_y = 10.2 + i
        handle.right_type = "test2"
        handle.right_x = 10.1 + i
        handle.right_y = 10.3 + i
        evt_obj_frame.rotation_handle.append(handle)
    for i in range(0, 3):
        handle = AeselGraphHandle()
        handle.left_type = "test"
        handle.left_x = 10.0 + i
        handle.left_y = 10.2 + i
        handle.right_type = "test2"
        handle.right_x = 10.1 + i
        handle.right_y = 10.3 + i
        evt_obj_frame.scale_handle.append(handle)
    evt_obj_action.keyframes = [evt_obj_frame]
    evt_obj.actions = [evt_obj_action]
    event_client.send_object_frame_update(evt_obj)

    # Wait for event to process
    time.sleep(1)

    # Check the current object transform to make sure it updated correctly
    print("Check object frame event")
    obj_get_resp2 = None
    try:
        obj_get_resp2 = transaction_client.get_object("objEventScene", obj_key)
    except Exception as e:
        print(e)
        assert(False)
    print(obj_get_resp2)
    assert(len(obj_get_resp2["objects"]) > 0)
    assert(len(obj_get_resp2["objects"][0]["actions"]) > 0)
    assert(len(obj_get_resp2["objects"][0]["actions"][0]["keyframes"]) > 0)
    assert(abs(obj_get_resp2["objects"][0]["actions"][0]["keyframes"][0]["transform"][0] - 2.0 < 0.001))

    # Delete an Object
    print("Delete Object")
    try:
        transaction_client.delete_object("objTestScene", obj_key)
    except Exception as e:
        print(e)
        assert(False)
