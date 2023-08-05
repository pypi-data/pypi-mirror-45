from functools import wraps
from .exceptions import RecordIsNull
from .utils import to_py_key, to_py_deep, to_js_key, get_repr, bind


__all__ = 'query', 'query_repr'
empty_tuple = tuple()


def query_repr(interface):
    return get_repr('Record', interface)


def recursive_require(required, fields):
    out = {}

    for field_name, field in required.items():
        if field is None or not len(field):
            # out[field_name] = recursive_require(fields[field_name], fields[field_name].fields)
            if hasattr(fields[field_name], 'fields'):
                out[field_name] = recursive_require(
                    {key: None for key in fields[field_name].fields},
                    fields[field_name].fields
                )
            else:
                out[field_name] = None
        else:
            out[field_name] = recursive_require(required[field_name], fields[field_name].fields)

    return out


def query(**fields):
    query_records = bind(fields)
    empty_requires = {record_name: None for record_name in query_records.keys()}

    def create_query(resolver):
        wrapper = wraps(resolver)

        @wrapper
        def init(query_name):
            @wrapper
            def resolve(required=None, props=None, context=None):
                context = context or {}

                if required is not None and len(required):
                    required = to_py_deep(required)

                required = recursive_require(required or empty_requires, query_records)

                if props is not None and len(props):
                    state = resolver(
                        required,
                        query=query_records,
                        query_name=query_name,
                        **to_py_deep(props),
                        **context
                    )
                else:
                    state = resolver(
                        required,
                        query=query_records,
                        query_name=query_name,
                        **context
                    )

                values = {}

                for record_name, required_fields in required.items():
                    try:
                        result = query_records[record_name](
                            state[record_name],
                            required_fields,
                            query=query_records,
                            query_name=query_name,
                            **context
                        )
                    except RecordIsNull:
                        result = None

                    values[to_js_key(record_name)] = result

                return values

            return resolve

        return init

    return create_query
