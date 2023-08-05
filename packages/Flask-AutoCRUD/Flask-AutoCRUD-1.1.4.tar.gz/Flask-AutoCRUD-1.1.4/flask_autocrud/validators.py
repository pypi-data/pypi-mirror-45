from flask import abort
from flask import request

from sqlalchemy import asc as ASC
from sqlalchemy import desc as DESC

from .wrapper import resp_json

from .config import GRAMMAR
from .config import ARGUMENT
from .config import HTTP_STATUS


def validate_entity(model, data):
    """

    :param model:
    :param data:
    """
    fields = model.required() + model.optional()
    unknown = [k for k in data if k not in fields]
    missing = set(model.required()) - set(data)

    if len(unknown) or len(missing):
        abort(
            resp_json({
                'unknown': unknown,
                'missing': list(missing)
            }, code=HTTP_STATUS.UNPROCESSABLE_ENTITY)
        )


def parsing_query_string(model):
    """

    :param model:
    :return:
    """
    order = []
    fields = []
    filters = []
    invalid = []

    try:
        page = request.args.get(ARGUMENT.STATIC.page)
        int(page) if page else None
    except ValueError:
        invalid.append(ARGUMENT.STATIC.page)

    try:
        limit = request.args.get(ARGUMENT.STATIC.limit)
        int(limit) if limit else None
    except ValueError:
        invalid.append(ARGUMENT.STATIC.limit)

    for k, v in request.args.items():
        if k in ARGUMENT.STATIC.__dict__.keys():
            continue

        if hasattr(model, k):
            attribute = getattr(model, k)

            if v.startswith(GRAMMAR.NOT_LIKE):
                filters.append(attribute.notilike(v[2:], escape='/'))
            elif v.startswith(GRAMMAR.LIKE):
                filters.append(attribute.ilike(v[1:], escape='/'))
            else:
                items = v.split(GRAMMAR.SEP)
                if len(items) > 1:
                    if items[0].startswith(GRAMMAR.NOT):
                        items[0] = items[0].lstrip(GRAMMAR.NOT)
                        in_statement = ~attribute.in_(items)
                    else:
                        in_statement = attribute.in_(items)
                    filters.append(in_statement)
                else:
                    if v.startswith(GRAMMAR.NOT):
                        filters.append(attribute != (None if v == GRAMMAR.NOT_NULL else v.lstrip(GRAMMAR.NOT)))
                    else:
                        filters.append(attribute == (None if v == GRAMMAR.NULL else v.lstrip('\\')))

        elif k == ARGUMENT.DYNAMIC.sort:
            for item in v.split(GRAMMAR.NOT):
                direction = DESC if item.startswith(GRAMMAR.REVERSE) else ASC
                item = item.lstrip(GRAMMAR.REVERSE)

                if not hasattr(model, item):
                    invalid.append(item)
                else:
                    order.append(direction(getattr(model, item)))

        elif k == ARGUMENT.DYNAMIC.fields:
            fields = v.split(GRAMMAR.SEP)
            for item in fields:
                if not hasattr(model, item):
                    invalid.append(item)
        else:
            invalid.append(k)

    if len(invalid) > 0:
        abort(resp_json({'invalid': invalid}, code=HTTP_STATUS.BAD_REQUEST))

    return fields, model.query.filter(*filters).order_by(*order)
