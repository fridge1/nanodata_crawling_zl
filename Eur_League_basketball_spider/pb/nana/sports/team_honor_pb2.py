# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nana/sports/team_honor.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nana.sports import season_pb2 as nana_dot_sports_dot_season__pb2
from nana.sports import comp_pb2 as nana_dot_sports_dot_comp__pb2
from nana.sports import honor_pb2 as nana_dot_sports_dot_honor__pb2
from nana.sports import team_pb2 as nana_dot_sports_dot_team__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='nana/sports/team_honor.proto',
  package='nana.sports',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1cnana/sports/team_honor.proto\x12\x0bnana.sports\x1a\x18nana/sports/season.proto\x1a\x16nana/sports/comp.proto\x1a\x17nana/sports/honor.proto\x1a\x16nana/sports/team.proto\"\xfa\x01\n\tTeamHonor\x12\x1f\n\x04team\x18\x01 \x01(\x0b\x32\x11.nana.sports.Team\x12,\n\x06honors\x18\x02 \x03(\x0b\x32\x1c.nana.sports.TeamHonor.Honor\x1a\x9d\x01\n\x05Honor\x12+\n\x05honor\x18\x01 \x01(\x0b\x32\x1c.nana.sports.TeamHonor.Honor\x12\x1f\n\x04\x63omp\x18\x02 \x01(\x0b\x32\x11.nana.sports.Comp\x12#\n\x06season\x18\x03 \x01(\x0b\x32\x13.nana.sports.Season\x12!\n\x05title\x18\x04 \x01(\x0b\x32\x12.nana.sports.Titleb\x06proto3')
  ,
  dependencies=[nana_dot_sports_dot_season__pb2.DESCRIPTOR,nana_dot_sports_dot_comp__pb2.DESCRIPTOR,nana_dot_sports_dot_honor__pb2.DESCRIPTOR,nana_dot_sports_dot_team__pb2.DESCRIPTOR,])




_TEAMHONOR_HONOR = _descriptor.Descriptor(
  name='Honor',
  full_name='nana.sports.TeamHonor.Honor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='honor', full_name='nana.sports.TeamHonor.Honor.honor', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='comp', full_name='nana.sports.TeamHonor.Honor.comp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='season', full_name='nana.sports.TeamHonor.Honor.season', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='title', full_name='nana.sports.TeamHonor.Honor.title', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=238,
  serialized_end=395,
)

_TEAMHONOR = _descriptor.Descriptor(
  name='TeamHonor',
  full_name='nana.sports.TeamHonor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='nana.sports.TeamHonor.team', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='honors', full_name='nana.sports.TeamHonor.honors', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TEAMHONOR_HONOR, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=395,
)

_TEAMHONOR_HONOR.fields_by_name['honor'].message_type = _TEAMHONOR_HONOR
_TEAMHONOR_HONOR.fields_by_name['comp'].message_type = nana_dot_sports_dot_comp__pb2._COMP
_TEAMHONOR_HONOR.fields_by_name['season'].message_type = nana_dot_sports_dot_season__pb2._SEASON
_TEAMHONOR_HONOR.fields_by_name['title'].message_type = nana_dot_sports_dot_honor__pb2._TITLE
_TEAMHONOR_HONOR.containing_type = _TEAMHONOR
_TEAMHONOR.fields_by_name['team'].message_type = nana_dot_sports_dot_team__pb2._TEAM
_TEAMHONOR.fields_by_name['honors'].message_type = _TEAMHONOR_HONOR
DESCRIPTOR.message_types_by_name['TeamHonor'] = _TEAMHONOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TeamHonor = _reflection.GeneratedProtocolMessageType('TeamHonor', (_message.Message,), dict(

  Honor = _reflection.GeneratedProtocolMessageType('Honor', (_message.Message,), dict(
    DESCRIPTOR = _TEAMHONOR_HONOR,
    __module__ = 'nana.sports.team_honor_pb2'
    # @@protoc_insertion_point(class_scope:nana.sports.TeamHonor.Honor)
    ))
  ,
  DESCRIPTOR = _TEAMHONOR,
  __module__ = 'nana.sports.team_honor_pb2'
  # @@protoc_insertion_point(class_scope:nana.sports.TeamHonor)
  ))
_sym_db.RegisterMessage(TeamHonor)
_sym_db.RegisterMessage(TeamHonor.Honor)


# @@protoc_insertion_point(module_scope)
