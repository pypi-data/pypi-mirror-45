# Copyright (C) 2019 SignalFx, Inc. All rights reserved.

import functools
import os
import opentracing
import warnings
from jaeger_client import Config

from . import utils


def wrapper(func):
    @functools.wraps(func)
    def call(*args, **kwargs):
        source = utils.get_source()
        function_name = os.environ.get('FUNCTION_NAME')
        if function_name is None:
            warnings.warn('FUNCTION_NAME cannot be found. Abort sending tracing')
            return call

        tracer = init_jaeger_tracer(function_name)

        span_tags = utils.get_fields()
        span_tags['component'] = 'python-' + source + '-wrapper'

        span_prefix = os.getenv('SIGNALFX_SPAN_PREFIX', source + '_python_')

        try:
            with tracer.start_active_span(span_prefix + function_name, tags=span_tags) as scope:
                # call the original handler
                return func(*args, **kwargs)
        except BaseException as e:
            scope.span.set_tag('error', True)
            scope.span.log_kv({'message': e})

            raise
        finally:
            tracer.close()

    return call


def init_jaeger_tracer(function_name):
    endpoint = utils.get_tracing_url()
    service_name = os.getenv('SIGNALFX_SERVICE_NAME', function_name)
    access_token = utils.get_access_token()

    tracer_config = {
            'sampler': {
                'type': 'const',
                'param': 1
                },
            'propagation': 'b3',
            'jaeger_endpoint': endpoint,
            'logging': True,
            }

    if access_token:
        tracer_config['jaeger_user'] = 'auth'
        tracer_config['jaeger_password'] = access_token

    config = Config(config=tracer_config, service_name=service_name)

    tracer = config.new_tracer()
    opentracing.tracer = tracer

    return tracer
