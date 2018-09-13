TAG_TEMPERATURE = 26
TAG_RELHUMIDITY = 66
TAG_PRECIPITATION = 57
TAG_WIND_DATA = 28

tag_map = {
    TAG_TEMPERATURE: 'Temperatura (%d)' % TAG_TEMPERATURE,
    TAG_RELHUMIDITY: 'Humedad Relativa (%d)' % TAG_RELHUMIDITY,
    TAG_PRECIPITATION: 'Precipitacion, 6h (%d)' % TAG_PRECIPITATION,
    TAG_WIND_DATA: 'Datos del viento (%d)' % TAG_WIND_DATA
}


def _TAG_DATA_IDENTITY(prev, _): return prev


def _TAG_FLOAT(_, f): return float(f)


def _TAG_DICT(key, type_op):
    def __TAG_DICT(prev, data):
        if type(prev) is dict:
            m = prev
        else:
            m = {}
        m[key] = type_op(data)
        return m
    return __TAG_DICT


def _TAG_EXFREE(op):
    def __T(prev, data):
        try:
            return op(prev, data)
        except Exception:
            print('WRN: Could not operate over: ({}, {})'.format(prev, data))
            return None
    return __T


# Each tag can have 1+ columns; each element in an operation
# list, represents the convertion made to a column.
# An operation receives the previously converted data, and the data
# of the current column. It must return converted data. On the first
# iteration, the 'previously converted data' is the timestamp of the data.
tag_data_map = {
    TAG_TEMPERATURE: [_TAG_FLOAT],
    TAG_RELHUMIDITY: [_TAG_FLOAT],
    TAG_PRECIPITATION: [_TAG_FLOAT, _TAG_DATA_IDENTITY],
    TAG_WIND_DATA: [_TAG_DICT('deg', int), _TAG_DICT(
        'spd', float), _TAG_DATA_IDENTITY]
}

# Convert all functions to exception free functions
tag_data_map = {k: [_TAG_EXFREE(op) for op in tag_data_map[k]]
                for k in tag_data_map}
