# Copyright (C) 2019 SignalFx, Inc. All rights reserved.

import os
import warnings

from .version import name, version

dim_prefix = 'gcf'

def get_fields():
    fields = {}

    env_dims = {
        'FUNCTION_REGION': dim_prefix + '_region',
        'GCP_PROJECT': dim_prefix + '_project_id',
        'FUNCTION_NAME': dim_prefix + '_function_name',
        'X_GOOGLE_FUNCTION_VERSION': dim_prefix + '_function_version'
    }

    for env_name, dim in env_dims.items():
        runtime_env = os.environ.get(env_name)
        if env_name is not None:
            fields[dim] = runtime_env
    
    fields['function_wrapper_version'] = name + '_' + version

    return fields