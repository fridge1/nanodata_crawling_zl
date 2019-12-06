# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nana/sports/player.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='nana/sports/player.proto',
  package='nana.sports',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x18nana/sports/player.proto\x12\x0bnana.sports\"\xfd\x03\n\x06Player\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08sport_id\x18\x02 \x01(\r\x12\x0f\n\x07team_id\x18\x03 \x01(\r\x12\x12\n\nmanager_id\x18\x04 \x01(\r\x12\x0f\n\x07name_en\x18\x06 \x01(\t\x12\x0f\n\x07name_zh\x18\x07 \x01(\t\x12\x10\n\x08name_zht\x18\x08 \x01(\t\x12\x15\n\rshort_name_en\x18\t \x01(\t\x12\x15\n\rshort_name_zh\x18\n \x01(\t\x12\x16\n\x0eshort_name_zht\x18\x0b \x01(\t\x12\x0c\n\x04logo\x18\x0c \x01(\t\x12\x0b\n\x03\x61ge\x18\r \x01(\x05\x12\x10\n\x08\x62irthday\x18\x0e \x01(\x05\x12\x0e\n\x06weight\x18\x10 \x01(\x05\x12\x0e\n\x06height\x18\x11 \x01(\x05\x12\x16\n\x0epreferred_foot\x18\x12 \x01(\x05\x12\x13\n\x0bnationality\x18\x13 \x01(\t\x12\x10\n\x08position\x18\x14 \x01(\t\x12\x1d\n\x15market_value_currency\x18\x15 \x01(\t\x12\x14\n\x0cmarket_value\x18\x16 \x01(\x04\x12\x16\n\x0e\x63ontract_until\x18\x17 \x01(\x05\x12\x14\n\x0c\x61\x62ility_data\x18\x18 \x01(\t\x12\x1c\n\x14\x63haracteristics_data\x18\x19 \x01(\t\x12\x1a\n\x12\x64\x65tailed_positions\x18\x1a \x01(\t\x12\r\n\x05\x65xtra\x18\x0f \x01(\x0c\x62\x06proto3')
)




_PLAYER = _descriptor.Descriptor(
  name='Player',
  full_name='nana.sports.Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='nana.sports.Player.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sport_id', full_name='nana.sports.Player.sport_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='team_id', full_name='nana.sports.Player.team_id', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='manager_id', full_name='nana.sports.Player.manager_id', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name_en', full_name='nana.sports.Player.name_en', index=4,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name_zh', full_name='nana.sports.Player.name_zh', index=5,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name_zht', full_name='nana.sports.Player.name_zht', index=6,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='short_name_en', full_name='nana.sports.Player.short_name_en', index=7,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='short_name_zh', full_name='nana.sports.Player.short_name_zh', index=8,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='short_name_zht', full_name='nana.sports.Player.short_name_zht', index=9,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='logo', full_name='nana.sports.Player.logo', index=10,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='age', full_name='nana.sports.Player.age', index=11,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='birthday', full_name='nana.sports.Player.birthday', index=12,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='weight', full_name='nana.sports.Player.weight', index=13,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='nana.sports.Player.height', index=14,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='preferred_foot', full_name='nana.sports.Player.preferred_foot', index=15,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nationality', full_name='nana.sports.Player.nationality', index=16,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='position', full_name='nana.sports.Player.position', index=17,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='market_value_currency', full_name='nana.sports.Player.market_value_currency', index=18,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='market_value', full_name='nana.sports.Player.market_value', index=19,
      number=22, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='contract_until', full_name='nana.sports.Player.contract_until', index=20,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ability_data', full_name='nana.sports.Player.ability_data', index=21,
      number=24, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='characteristics_data', full_name='nana.sports.Player.characteristics_data', index=22,
      number=25, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='detailed_positions', full_name='nana.sports.Player.detailed_positions', index=23,
      number=26, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extra', full_name='nana.sports.Player.extra', index=24,
      number=15, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_end=551,
)

DESCRIPTOR.message_types_by_name['Player'] = _PLAYER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Player = _reflection.GeneratedProtocolMessageType('Player', (_message.Message,), dict(
  DESCRIPTOR = _PLAYER,
  __module__ = 'nana.sports.player_pb2'
  # @@protoc_insertion_point(class_scope:nana.sports.Player)
  ))
_sym_db.RegisterMessage(Player)


# @@protoc_insertion_point(module_scope)
