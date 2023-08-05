# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import json

from marshmallow import Schema, fields, post_load


class BaseModel:
    id = None  # type: str

    def __init__(self, **kwargs):
        # Inject parsed properties in the model
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    @property
    def json(self):
        dump = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(dump)


class BaseSchema(Schema):
    id = fields.Str()

    @post_load
    def make_object(self, data):
        return BaseModel(**data)
