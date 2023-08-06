# Copyright (C) 2019 SignalFx, Inc. All rights reserved.

from . import serverless
from .version import name, version

from . import utils

fields = utils.get_fields()
serverless.configure('gcf', fields)
    

# backwards compatibility
def wrapper(*args, **kwargs):
    return serverless.wrapper(*args, **kwargs)


def emits_metrics(*args, **kwargs):
    return serverless.emits_metrics(*args, **kwargs)


def is_traced(*args, **kwargs):
    return serverless.is_traced(*args, **kwargs)


# less convenient method
def send_metric(counters=[], gauges=[]):
    serverless.send_metric(counters, gauges)


# convenience method
def send_counter(metric_name, metric_value=1, dimensions={}):
    serverless.send_counter(metric_name, metric_value, dimensions)


# convenience method
def send_gauge(metric_name, metric_value, dimensions={}):
    serverless.send_gauge(metric_name, metric_value, dimensions)

