import simplejson
from google.protobuf.descriptor import FieldDescriptor as FieldDesc


class ConvertException(Exception):
    pass


def dict2pb(cls, adict, strict=False):
    """
    Takes a class representing the ProtoBuf Message and fills it with data from
    the dict.
    """
    obj = cls()
    if not adict:
        return obj

    for field in obj.DESCRIPTOR.fields:
        if field.label != field.LABEL_REQUIRED:
            continue
        if not field.has_default_value:
            continue
        if field.name not in adict:
            raise ConvertException(
                'Field "%s" missing from descriptor dictionary.' % field.name
            )
    field_names = set([field.name for field in obj.DESCRIPTOR.fields])
    if strict:
        for key in adict.keys():
            if key not in field_names:
                raise ConvertException(
                    'Key "%s" can not be mapped to field in %s class.'
                    % (key, type(obj))
                )
    for field in obj.DESCRIPTOR.fields:
        msg_type = field.message_type
        sub_obj = getattr(obj, field.name)

        if adict.get(field.name) is None or sub_obj is None:
            continue
        if field.label == FieldDesc.LABEL_REPEATED:
            if field.type == FieldDesc.TYPE_MESSAGE:
                if hasattr(sub_obj, 'items'):
                    for k, sub_dict in adict[field.name].items():
                        item = getattr(obj, field.name)
                        sub_cls = msg_type.fields_by_name['value'].message_type._concrete_class
                        pb = dict2pb(
                            sub_cls
                            , sub_dict
                        )
                        item[k].CopyFrom(pb)
                else:
                    for sub_dict in adict[field.name]:
                        item = getattr(obj, field.name).add()
                        item.CopyFrom(dict2pb(msg_type._concrete_class, sub_dict))
            else:
                value = adict[field.name]
                if value:
                    getattr(obj, field.name).extend(value)
        else:
            if field.type == FieldDesc.TYPE_MESSAGE:
                value = dict2pb(msg_type._concrete_class, adict[field.name])
                getattr(obj, field.name).CopyFrom(value)
            else:
                value = adict[field.name]
                if value:
                    setattr(obj, field.name, value)
    return obj


def pb2dict(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a dict.
    """
    adict = {}
    if not obj.IsInitialized():
        return None
    for field in obj.DESCRIPTOR.fields:
        if not getattr(obj, field.name):
            continue
        if not field.label == FieldDesc.LABEL_REPEATED:
            if not field.type == FieldDesc.TYPE_MESSAGE:
                adict[field.name] = getattr(obj, field.name)
            else:
                value = pb2dict(getattr(obj, field.name))
                if value:
                    adict[field.name] = value
        else:
            if field.type == FieldDesc.TYPE_MESSAGE:
                adict[field.name] = \
                    [pb2dict(v) for v in getattr(obj, field.name)]
            else:
                adict[field.name] = [v for v in getattr(obj, field.name)]
    return adict


def json2pb(cls, json, strict=False):
    """
    Takes a class representing the Protobuf Message and fills it with data from
    the json string.
    """
    return dict2pb(cls, simplejson.loads(json), strict)


def pb2json(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a json string.
    """
    return simplejson.dumps(pb2dict(obj), sort_keys=True, indent=4)
