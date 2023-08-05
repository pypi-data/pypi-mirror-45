# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

from typing import Any, Dict, List, Optional

from connect.logger import logger, function_log
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.fulfillment import Fulfillment, FulfillmentSchema
from connect.models.tier_config import TierConfig, TierConfigRequestSchema
from .automation import AutomationResource


class FulfillmentAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'requests'
    schema = FulfillmentSchema(many=True)

    def filters(self, status='pending', **kwargs):
        # type: (str, Dict[str, Any]) -> Dict[str, Any]
        filters = super(FulfillmentAutomation, self).filters(status=status, **kwargs)
        if self.config.products:
            filters['asset.product.id__in'] = ','.join(self.config.products)
        return filters

    def dispatch(self, request):
        # type: (Fulfillment) -> str
        try:
            if self.config.products \
                    and request.asset.product.id not in self.config.products:
                return 'Invalid product'

            logger.info('Start request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                logger.info('Method `process_request` did not return result')
                return ''

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'activation_tile': result.tile}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template_id': result.template_id}

            return self.approve(request.id, params)

        except FulfillmentInquire as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FulfillmentFail as fail:
            return self.fail(request.id, reason=fail.message)

        except Skip as skip:
            return skip.code

    def get_tier_config(self, tier_id, product_id):
        # type: (str, str) -> Optional[TierConfig]
        url = self._api.urljoin(self.config.api_url, 'tier/config-requests')
        params = {
            'status': 'approved',
            'configuration__product__id': product_id,
            'configuration__account__id': tier_id,
        }
        response, _ = self._api.get(url=url, params=params)
        objects = self._load_schema(response, schema=TierConfigRequestSchema(many=True))

        if isinstance(objects, list) and len(objects) > 0:
            return objects[0].configuration
        else:
            return None

    @function_log
    def update_parameters(self, pk, params):
        # type: (str, List[Param]) -> str
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self._api.put(
            path=pk,
            json={'asset': {'params': list_dict}},
        )[0]
