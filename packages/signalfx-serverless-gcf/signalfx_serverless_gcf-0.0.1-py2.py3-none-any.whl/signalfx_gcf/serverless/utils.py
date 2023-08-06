# Copyright (C) 2019 SignalFx, Inc. All rights reserved.

import os
import warnings

source = None
fields = {}

def get_source():
    global source
    return source

def get_fields():
    global fields
    return fields.copy()

def get_metrics_url():
    url = os.environ.get('SIGNALFX_INGEST_ENDPOINT')
    if url:
        warnings.warn('SIGNALFX_INGEST_ENDPOINT is deprecated, use SIGNALFX_METRICS_URL instead.', DeprecationWarning)
    else:
        url = os.environ.get('SIGNALFX_METRICS_URL')

    if not url:
        url = os.environ.get('SIGNALFX_ENDPOINT_URL', 'https://pops.signalfx.com')

    return url


def get_tracing_url():
    url = os.environ.get('SIGNALFX_TRACING_URL')

    if not url:
        url = os.environ.get('SIGNALFX_ENDPOINT_URL')

        if url:
            # if the common endpoint url is used, we need to append the trace path
            url = url + '/v1/trace'
        else:
            url = 'https://ingest.signalfx.com/v1/trace'

    return url


def get_access_token():
    token = os.environ.get('SIGNALFX_ACCESS_TOKEN')
    if not token:
        warnings.warn('SIGNALFX_AUTH_TOKEN is deprecated, use SIGNALFX_ACCESS_TOKEN instead.', DeprecationWarning)
        token = os.environ.get('SIGNALFX_AUTH_TOKEN')

    return token

def set_source(s):
    global source
    source = s

def set_fields(fs):
    global fields
    for key, value in fs.items():
        fields[key] = value
