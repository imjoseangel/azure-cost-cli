#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.subscription import SubscriptionClient


cost_client = CostManagementClient(credential=DefaultAzureCredential())


def subscription_list():
    subscription_client = SubscriptionClient(credential=DefaultAzureCredential())
    sub_list = subscription_client.subscriptions.list()
    column_width = 40

    print("Subscription ID".ljust(column_width) + "Display name")
    print("-" * (column_width * 2))
    for group in list(sub_list):
        print(f'{group.subscription_id:<{column_width}}{group.display_name}')


def main():
    # subscription_list()
    pass

if __name__ == '__main__':
    main()
