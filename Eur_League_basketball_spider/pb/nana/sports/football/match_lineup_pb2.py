# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nana/sports/football/match_lineup.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='nana/sports/football/match_lineup.proto',
  package='nana.sports.football',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\'nana/sports/football/match_lineup.proto\x12\x14nana.sports.football\"\x96\x02\n\x0fMatchLineupInfo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08sport_id\x18\x02 \x01(\x05\x12\x10\n\x08match_id\x18\x03 \x01(\x05\x12\x14\n\x0chome_team_id\x18\x04 \x01(\x05\x12\x14\n\x0c\x61way_team_id\x18\x05 \x01(\x05\x12\x17\n\x0fhome_manager_id\x18\x06 \x01(\x05\x12\x17\n\x0f\x61way_manager_id\x18\x07 \x01(\x05\x12\x11\n\tconfirmed\x18\x08 \x01(\x05\x12\x16\n\x0ehome_formation\x18\t \x01(\t\x12\x16\n\x0e\x61way_formation\x18\n \x01(\t\x12\x18\n\x10home_team_rating\x18\x0b \x01(\x05\x12\x18\n\x10\x61way_team_rating\x18\x0c \x01(\x05\"\xd7\x02\n\x11MatchLineupDetail\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08sport_id\x18\x02 \x01(\x05\x12\x10\n\x08match_id\x18\x03 \x01(\x05\x12\x0f\n\x07team_id\x18\x04 \x01(\x05\x12\x11\n\tplayer_id\x18\x05 \x01(\x05\x12\x0e\n\x06status\x18\x06 \x01(\x05\x12\x0e\n\x06season\x18\x07 \x01(\t\x12\x0e\n\x06rating\x18\x08 \x01(\x05\x12\x0f\n\x07\x63\x61ptain\x18\t \x01(\x05\x12\x16\n\x0eplayer_name_zh\x18\n \x01(\t\x12\x17\n\x0fplayer_name_zht\x18\x0b \x01(\t\x12\x16\n\x0eplayer_name_en\x18\x0c \x01(\t\x12\x14\n\x0cshirt_number\x18\r \x01(\x05\x12\x10\n\x08position\x18\x0e \x01(\t\x12\x12\n\nlocation_x\x18\x0f \x01(\x05\x12\x12\n\nlocation_y\x18\x10 \x01(\x05\x12\x14\n\x0cposition_num\x18\x11 \x01(\x05\"{\n\x0bMatchLineup\x12\x33\n\x04info\x18\x01 \x01(\x0b\x32%.nana.sports.football.MatchLineupInfo\x12\x37\n\x06\x64\x65tail\x18\x02 \x03(\x0b\x32\'.nana.sports.football.MatchLineupDetailb\x06proto3')
)




_MATCHLINEUPINFO = _descriptor.Descriptor(
  name='MatchLineupInfo',
  full_name='nana.sports.football.MatchLineupInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='nana.sports.football.MatchLineupInfo.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sport_id', full_name='nana.sports.football.MatchLineupInfo.sport_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='match_id', full_name='nana.sports.football.MatchLineupInfo.match_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='home_team_id', full_name='nana.sports.football.MatchLineupInfo.home_team_id', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='away_team_id', full_name='nana.sports.football.MatchLineupInfo.away_team_id', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='home_manager_id', full_name='nana.sports.football.MatchLineupInfo.home_manager_id', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='away_manager_id', full_name='nana.sports.football.MatchLineupInfo.away_manager_id', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='confirmed', full_name='nana.sports.football.MatchLineupInfo.confirmed', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='home_formation', full_name='nana.sports.football.MatchLineupInfo.home_formation', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='away_formation', full_name='nana.sports.football.MatchLineupInfo.away_formation', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='home_team_rating', full_name='nana.sports.football.MatchLineupInfo.home_team_rating', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='away_team_rating', full_name='nana.sports.football.MatchLineupInfo.away_team_rating', index=11,
      number=12, type=5, cpp_type=1, label=1,
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
  serialized_start=66,
  serialized_end=344,
)


_MATCHLINEUPDETAIL = _descriptor.Descriptor(
  name='MatchLineupDetail',
  full_name='nana.sports.football.MatchLineupDetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='nana.sports.football.MatchLineupDetail.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sport_id', full_name='nana.sports.football.MatchLineupDetail.sport_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='match_id', full_name='nana.sports.football.MatchLineupDetail.match_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='team_id', full_name='nana.sports.football.MatchLineupDetail.team_id', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_id', full_name='nana.sports.football.MatchLineupDetail.player_id', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='nana.sports.football.MatchLineupDetail.status', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='season', full_name='nana.sports.football.MatchLineupDetail.season', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rating', full_name='nana.sports.football.MatchLineupDetail.rating', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='captain', full_name='nana.sports.football.MatchLineupDetail.captain', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_name_zh', full_name='nana.sports.football.MatchLineupDetail.player_name_zh', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_name_zht', full_name='nana.sports.football.MatchLineupDetail.player_name_zht', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_name_en', full_name='nana.sports.football.MatchLineupDetail.player_name_en', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shirt_number', full_name='nana.sports.football.MatchLineupDetail.shirt_number', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='position', full_name='nana.sports.football.MatchLineupDetail.position', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='location_x', full_name='nana.sports.football.MatchLineupDetail.location_x', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='location_y', full_name='nana.sports.football.MatchLineupDetail.location_y', index=15,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='position_num', full_name='nana.sports.football.MatchLineupDetail.position_num', index=16,
      number=17, type=5, cpp_type=1, label=1,
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
  serialized_start=347,
  serialized_end=690,
)


_MATCHLINEUP = _descriptor.Descriptor(
  name='MatchLineup',
  full_name='nana.sports.football.MatchLineup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='nana.sports.football.MatchLineup.info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='detail', full_name='nana.sports.football.MatchLineup.detail', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=692,
  serialized_end=815,
)

_MATCHLINEUP.fields_by_name['info'].message_type = _MATCHLINEUPINFO
_MATCHLINEUP.fields_by_name['detail'].message_type = _MATCHLINEUPDETAIL
DESCRIPTOR.message_types_by_name['MatchLineupInfo'] = _MATCHLINEUPINFO
DESCRIPTOR.message_types_by_name['MatchLineupDetail'] = _MATCHLINEUPDETAIL
DESCRIPTOR.message_types_by_name['MatchLineup'] = _MATCHLINEUP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MatchLineupInfo = _reflection.GeneratedProtocolMessageType('MatchLineupInfo', (_message.Message,), dict(
  DESCRIPTOR = _MATCHLINEUPINFO,
  __module__ = 'nana.sports.football.match_lineup_pb2'
  # @@protoc_insertion_point(class_scope:nana.sports.football.MatchLineupInfo)
  ))
_sym_db.RegisterMessage(MatchLineupInfo)

MatchLineupDetail = _reflection.GeneratedProtocolMessageType('MatchLineupDetail', (_message.Message,), dict(
  DESCRIPTOR = _MATCHLINEUPDETAIL,
  __module__ = 'nana.sports.football.match_lineup_pb2'
  # @@protoc_insertion_point(class_scope:nana.sports.football.MatchLineupDetail)
  ))
_sym_db.RegisterMessage(MatchLineupDetail)

MatchLineup = _reflection.GeneratedProtocolMessageType('MatchLineup', (_message.Message,), dict(
  DESCRIPTOR = _MATCHLINEUP,
  __module__ = 'nana.sports.football.match_lineup_pb2'
  # @@protoc_insertion_point(class_scope:nana.sports.football.MatchLineup)
  ))
_sym_db.RegisterMessage(MatchLineup)


# @@protoc_insertion_point(module_scope)
