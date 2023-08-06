# Copyright (C) 2019 SignalFx, Inc. All rights reserved.

from . import tracing, utils, metrics


def configure(source, fields):
    utils.set_source(source)
    utils.set_fields(fields)

# backwards compatibility
def wrapper(*args, **kwargs):
    return metrics.wrapper(*args, **kwargs)


def emits_metrics(*args, **kwargs):
    return metrics.wrapper(*args, **kwargs)


def is_traced(*args, **kwargs):
    return tracing.wrapper(*args, **kwargs)


# less convenient method
def send_metric(counters=[], gauges=[]):
    metrics.send_metric(counters, gauges)


# convenience method
# FIXME: can't do {} or [] as default params.
def send_counter(metric_name, metric_value=1, dimensions={}):
    metrics.send_counter(metric_name, metric_value, dimensions)


# convenience method
def send_gauge(metric_name, metric_value, dimensions={}):
    metrics.send_gauge(metric_name, metric_value, dimensions)

