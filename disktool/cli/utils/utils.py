import decimal

def explode_array(list_str, separator=","):
    """
    Explode list string into array
    """
    if not list_str:
        return []
    return [item.strip() for item in list_str.split(separator) if item.strip() != '']


def metric_key(metric, prefix=''):
    return '{prefix}{metric.name}'.format(prefix=prefix, metric=metric)


def metric_format(metric, prefix=''):
    key = metric_key(metric, prefix)
    labels = ','.join(
        '{k}="{v}"'.format(k=k, v=v) for k, v in metric.labels.items())
    value = decimal.Decimal(metric.value)

    return '{key}{{{labels}}} {value}\n'.format(
        key=key, labels=labels, value=value)


def metric_print(metric, prefix=''):
    return metric_format(metric, prefix)


def metric_print_smart_meta(metric, prefix=''):
    key = metric_key(metric, prefix)
    return '# HELP {key} disktool metric {metric.name}\n'.format(
        key=key, metric=metric) + '# TYPE {key} gauge\n'.format(key=key, metric=metric)
