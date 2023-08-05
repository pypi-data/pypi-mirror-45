# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from typing import List, Any, Dict

from connect.models import ActivationTemplateResponse, ActivationTileResponse
from .base import BaseResource


class TemplateResource(BaseResource):
    """ Specific resource.
    One method `render`
    He returns json string with activation tile
    """
    resource = 'templates'

    def list(self, filters=None):
        # type: (Dict[str, Any]) -> List[Any]
        raise AttributeError('This resource do not have method `list`')

    def render(self, pk, request_id):
        # type: (str, str) -> ActivationTileResponse
        if not all([pk, request_id]):
            raise ValueError('Invalid ids for render template')
        response, _ = self._api.get(path=pk + '/render', params={'request_id': request_id})
        return ActivationTileResponse(response)

    def get(self, pk):
        # type: (str) -> ActivationTemplateResponse
        return ActivationTemplateResponse(template_id=pk)
