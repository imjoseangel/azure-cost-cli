#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from datetime import datetime, timezone, timedelta
import json

from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import (QueryDefinition, QueryDataset,
                                              QueryTimePeriod, QueryAggregation,
                                              QueryGrouping)
from azure.mgmt.subscription import SubscriptionClient


cost_client = CostManagementClient(credential=DefaultAzureCredential())
COLUMN_WIDTH = 50

def subscription_list():
    subscription_client = SubscriptionClient(credential=DefaultAzureCredential())
    sub_list = subscription_client.subscriptions.list()

    print("Subscription ID".ljust(COLUMN_WIDTH) + "Display name")
    print("-" * (COLUMN_WIDTH * 2))
    for group in list(sub_list):
        print(f'{group.subscription_id:<{COLUMN_WIDTH}}{group.display_name}')


TIME_PERIOD_IN_PAST = 30
SUBSCRIPTION_ID = "5e91a5fa-3787-4f0f-84ff-d7e9590c724a"
RESOURCE_GROUP_NAME = "rg-crossresources-dev"

scope = f'/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP_NAME}'
maxDateInPast = ((datetime.now(timezone.utc)) - timedelta(days=TIME_PERIOD_IN_PAST))

time_period = QueryTimePeriod(from_property=maxDateInPast,
                              to=datetime.now(timezone.utc))

query_aggregation = {}
# in result, will be column with index = 0

query_aggregation["totalCost"] = QueryAggregation(name="Cost", function="Sum")
# in result, will be column with index = 1

query_aggregation["totalCostUSD"] = QueryAggregation(name="CostUSD", function="Sum")
query_grouping = [QueryGrouping(type="Dimension", name="ResourceId"),
                  QueryGrouping(type="Dimension", name="ChargeType"),
                  QueryGrouping(type="Dimension", name="PublisherType")]

querydataset = QueryDataset(granularity=None, configuration=None,
                            aggregation=query_aggregation, grouping=query_grouping)
query = QueryDefinition(type="ActualCost", timeframe="Custom",
                        time_period=time_period, dataset=querydataset)

result = cost_client.query.usage(scope=scope, parameters=query)

if result:
    print("Resource Name".ljust(COLUMN_WIDTH) + "Cost")
    print("-" * (COLUMN_WIDTH * 2))
    for data in result.as_dict()['rows']:
        print(f'{data[2].split("/")[-1]:<{COLUMN_WIDTH}} {round(data[0])}')


def main():
    # subscription_list()
    pass


if __name__ == '__main__':
    main()
