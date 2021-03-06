# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nana/sports/country.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='nana/sports/country.proto',
  package='nana.sports',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x19nana/sports/country.proto\x12\x0bnana.sports\"[\n\x07\x43ountry\x12\n\n\x02id\x18\x01 \x01(\r\x12\x10\n\x08sport_id\x18\x02 \x01(\r\x12\x0f\n\x07name_zh\x18\x03 \x01(\t\x12\x10\n\x08name_zht\x18\x04 \x01(\t\x12\x0f\n\x07name_en\x18\x05 \x01(\tb\x06proto3')
)




_COUNTRY = _descriptor.Descriptor(
  name='Country',
  full_name='nana.sports.Country',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='nana.sports.Country.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sport_id', full_name='nana.sports.Country.sport_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name_zh', full_name='nana.sports.Country.name_zh', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name_zht', full_name='nana.sports.Country.name_zht', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name_en', full_name='nana.sports.Country.name_en', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=133,
)

DESCRIPTOR.message_types_by_name['Country'] = _COUNTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Country = _reflection.GeneratedProtocolMessageType('Country', (_message.Message,), dict(
  DESCRIPTOR = _COUNTRY,
  __module__ = 'nana.sports.country_pb2'
  # @@protoc_insertion_point(class_scope:nana.sports.Country)
  ))
_sym_db.RegisterMessage(Country)


# @@protoc_insertion_point(module_scope)
