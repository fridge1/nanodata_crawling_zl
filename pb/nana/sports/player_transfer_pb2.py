# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nana/sports/player_transfer.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nana.sports import player_pb2 as nana_dot_sports_dot_player__pb2
from nana.sports import team_pb2 as nana_dot_sports_dot_team__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='nana/sports/player_transfer.proto',
  package='nana.sports',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n!nana/sports/player_transfer.proto\x12\x0bnana.sports\x1a\x18nana/sports/player.proto\x1a\x16nana/sports/team.proto\"\xf0\x01\n\x0ePlayerTransfer\x12#\n\x06player\x18\x01 \x01(\x0b\x32\x13.nana.sports.Player\x12$\n\tfrom_team\x18\x02 \x01(\x0b\x32\x11.nana.sports.Team\x12\"\n\x07to_team\x18\x03 \x01(\x0b\x32\x11.nana.sports.Team\x12\x15\n\rtransfer_time\x18\x04 \x01(\x05\x12\x14\n\x0ctransfer_fee\x18\x05 \x01(\x05\x12\x15\n\rtransfer_desc\x18\x06 \x01(\x05\x12\x15\n\rtransfer_type\x18\x07 \x01(\x05\x12\x14\n\x0cmarket_value\x18\x08 \x01(\x05\x62\x06proto3')
  ,
  dependencies=[nana_dot_sports_dot_player__pb2.DESCRIPTOR,nana_dot_sports_dot_team__pb2.DESCRIPTOR,])




_PLAYERTRANSFER = _descriptor.Descriptor(
  name='PlayerTransfer',
  full_name='nana.sports.PlayerTransfer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player', full_name='nana.sports.PlayerTransfer.player', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='from_team', full_name='nana.sports.PlayerTransfer.from_team', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='to_team', full_name='nana.sports.PlayerTransfer.to_team', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transfer_time', full_name='nana.sports.PlayerTransfer.transfer_time', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transfer_fee', full_name='nana.sports.PlayerTransfer.transfer_fee', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transfer_desc', full_name='nana.sports.PlayerTransfer.transfer_desc', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transfer_type', full_name='nana.sports.PlayerTransfer.transfer_type', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='market_value', full_name='nana.sports.PlayerTransfer.market_value', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=101,
  serialized_end=341,
)

_PLAYERTRANSFER.fields_by_name['player'].message_type = nana_dot_sports_dot_player__pb2._PLAYER
_PLAYERTRANSFER.fields_by_name['from_team'].message_type = nana_dot_sports_dot_team__pb2._TEAM
_PLAYERTRANSFER.fields_by_name['to_team'].message_type = nana_dot_sports_dot_team__pb2._TEAM
DESCRIPTOR.message_types_by_name['PlayerTransfer'] = _PLAYERTRANSFER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PlayerTransfer = _reflection.GeneratedProtocolMessageType('PlayerTransfer', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERTRANSFER,
  __module__ = 'nana.sports.player_transfer_pb2'
  # @@protoc_insertion_point(class_scope:nana.sports.PlayerTransfer)
  ))
_sym_db.RegisterMessage(PlayerTransfer)


# @@protoc_insertion_point(module_scope)
