# -*- coding: utf-8 -*-
# Copyright 2014 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Stéphane Albert
#
import datetime
import decimal

import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from cloudkitty.api.v1.datamodels import storage as storage_models
from cloudkitty.common import policy
from cloudkitty import storage as ck_storage
from cloudkitty import utils as ck_utils


class DataFramesController(rest.RestController):
    """REST Controller to access stored data frames."""

    @wsme_pecan.wsexpose(storage_models.DataFrameCollection,
                         datetime.datetime,
                         datetime.datetime,
                         wtypes.text,
                         wtypes.text)
    def get_all(self, begin=None, end=None, tenant_id=None,
                resource_type=None):
        """Return a list of rated resources for a time period and a tenant.

        :param begin: Start of the period
        :param end: End of the period
        :param tenant_id: UUID of the tenant to filter on.
        :param resource_type: Type of the resource to filter on.
        :return: Collection of DataFrame objects.
        """

        policy.enforce(pecan.request.context, 'storage:list_data_frames', {})

        if not begin:
            begin = ck_utils.get_month_start()
        if not end:
            end = ck_utils.get_next_month()

        begin_ts = ck_utils.dt2ts(begin)
        end_ts = ck_utils.dt2ts(end)
        backend = pecan.request.storage_backend
        dataframes = []
        try:
            frames = backend.get_time_frame(begin_ts,
                                            end_ts,
                                            tenant_id=tenant_id,
                                            res_type=resource_type)
            for frame in frames:
                for service, data_list in frame['usage'].items():
                    frame_tenant = None
                    resources = []
                    for data in data_list:
                        desc = data['desc'] if data['desc'] else {}
                        price = decimal.Decimal(str(data['rating']['price']))
                        resource = storage_models.RatedResource(
                            service=service,
                            desc=desc,
                            volume=data['vol']['qty'],
                            rating=price)
                        frame_tenant = data['tenant_id']
                        resources.append(resource)
                    dataframe = storage_models.DataFrame(
                        begin=ck_utils.iso2dt(frame['period']['begin']),
                        end=ck_utils.iso2dt(frame['period']['end']),
                        tenant_id=frame_tenant,
                        resources=resources)
                    dataframes.append(dataframe)
        except ck_storage.NoTimeFrame:
            pass
        return storage_models.DataFrameCollection(dataframes=dataframes)


class StorageController(rest.RestController):
    """REST Controller to access stored data."""

    dataframes = DataFramesController()
