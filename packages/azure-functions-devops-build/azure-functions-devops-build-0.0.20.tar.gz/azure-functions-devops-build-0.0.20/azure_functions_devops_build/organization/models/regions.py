# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.serialization import Model

class Regions(Model):
    _attribute_map = {
        'count': {'key': 'count', 'type': 'int'},
        'value': {'key': 'value', 'type': '[RegionDetails]'},
    }

    def __init__(self, count=None, value=None):
        self.count = count
        self.value = value