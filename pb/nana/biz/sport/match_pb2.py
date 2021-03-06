# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nana/biz/sport/match.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nana.sports import match_pb2 as nana_dot_sports_dot_match__pb2
from nana.sports import odds_pb2 as nana_dot_sports_dot_odds__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='nana/biz/sport/match.proto',
  package='nana.biz.sports',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1anana/biz/sport/match.proto\x12\x0fnana.biz.sports\x1a\x17nana/sports/match.proto\x1a\x16nana/sports/odds.proto\"\x12\n\x10SportsMatchesReq\"\xb7\x01\n\x10SportsMatchesRes\x12\x10\n\x08sport_id\x18\x01 \x01(\x05\x12\x0c\n\x04site\x18\x02 \x01(\t\x12?\n\x07matches\x18\x03 \x03(\x0b\x32..nana.biz.sports.SportsMatchesRes.MatchesEntry\x1a\x42\n\x0cMatchesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.nana.sports.Match:\x02\x38\x01\"\x0f\n\rSportsOddsReq\"a\n\tMatchOdds\x12\x10\n\x08match_id\x18\x01 \x01(\x05\x12\x0f\n\x07site_id\x18\x02 \x01(\x05\x12\x1f\n\x04odds\x18\x04 \x03(\x0b\x32\x11.nana.sports.Odds\x12\x10\n\x08is_first\x18\x05 \x01(\x08\"[\n\rSportsOddsRes\x12\x10\n\x08sport_id\x18\x01 \x01(\x05\x12\x0e\n\x06uptime\x18\x02 \x01(\x05\x12(\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32\x1a.nana.biz.sports.MatchOdds\"\x10\n\x0eSportsCheckReq\"\x10\n\x0eSportsCheckRes\"\x12\n\x10SportsRestartReq\"\x12\n\x10SportsRestartRes*\x9b\x01\n\x0bSportsSvrID\x12\x15\n\x11SID_SPORTS_UNKNOW\x10\x00\x12\x13\n\x0fSID_SPORTS_LIVE\x10\x01\x12\x17\n\x13SID_SPORTS_SCHEDULE\x10\x02\x12\x13\n\x0fSID_SPORTS_ODDS\x10\x03\x12\x19\n\x14SID_SPORTS_HEARTBEAT\x10\x81\x12\x12\x17\n\x12SID_SPORTS_RESTART\x10\x82\x12\x62\x06proto3')
  ,
  dependencies=[nana_dot_sports_dot_match__pb2.DESCRIPTOR,nana_dot_sports_dot_odds__pb2.DESCRIPTOR,])

_SPORTSSVRID = _descriptor.EnumDescriptor(
  name='SportsSvrID',
  full_name='nana.biz.sports.SportsSvrID',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SID_SPORTS_UNKNOW', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SID_SPORTS_LIVE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SID_SPORTS_SCHEDULE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SID_SPORTS_ODDS', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SID_SPORTS_HEARTBEAT', index=4, number=2305,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SID_SPORTS_RESTART', index=5, number=2306,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=588,
  serialized_end=743,
)
_sym_db.RegisterEnumDescriptor(_SPORTSSVRID)

SportsSvrID = enum_type_wrapper.EnumTypeWrapper(_SPORTSSVRID)
SID_SPORTS_UNKNOW = 0
SID_SPORTS_LIVE = 1
SID_SPORTS_SCHEDULE = 2
SID_SPORTS_ODDS = 3
SID_SPORTS_HEARTBEAT = 2305
SID_SPORTS_RESTART = 2306



_SPORTSMATCHESREQ = _descriptor.Descriptor(
  name='SportsMatchesReq',
  full_name='nana.biz.sports.SportsMatchesReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=96,
  serialized_end=114,
)


_SPORTSMATCHESRES_MATCHESENTRY = _descriptor.Descriptor(
  name='MatchesEntry',
  full_name='nana.biz.sports.SportsMatchesRes.MatchesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='nana.biz.sports.SportsMatchesRes.MatchesEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='nana.biz.sports.SportsMatchesRes.MatchesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=300,
)

_SPORTSMATCHESRES = _descriptor.Descriptor(
  name='SportsMatchesRes',
  full_name='nana.biz.sports.SportsMatchesRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sport_id', full_name='nana.biz.sports.SportsMatchesRes.sport_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='site', full_name='nana.biz.sports.SportsMatchesRes.site', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='matches', full_name='nana.biz.sports.SportsMatchesRes.matches', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SPORTSMATCHESRES_MATCHESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=300,
)


_SPORTSODDSREQ = _descriptor.Descriptor(
  name='SportsOddsReq',
  full_name='nana.biz.sports.SportsOddsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=302,
  serialized_end=317,
)


_MATCHODDS = _descriptor.Descriptor(
  name='MatchOdds',
  full_name='nana.biz.sports.MatchOdds',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='match_id', full_name='nana.biz.sports.MatchOdds.match_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='site_id', full_name='nana.biz.sports.MatchOdds.site_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='odds', full_name='nana.biz.sports.MatchOdds.odds', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_first', full_name='nana.biz.sports.MatchOdds.is_first', index=3,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=319,
  serialized_end=416,
)


_SPORTSODDSRES = _descriptor.Descriptor(
  name='SportsOddsRes',
  full_name='nana.biz.sports.SportsOddsRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sport_id', full_name='nana.biz.sports.SportsOddsRes.sport_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uptime', full_name='nana.biz.sports.SportsOddsRes.uptime', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='nana.biz.sports.SportsOddsRes.data', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=418,
  serialized_end=509,
)


_SPORTSCHECKREQ = _descriptor.Descriptor(
  name='SportsCheckReq',
  full_name='nana.biz.sports.SportsCheckReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=511,
  serialized_end=527,
)


_SPORTSCHECKRES = _descriptor.Descriptor(
  name='SportsCheckRes',
  full_name='nana.biz.sports.SportsCheckRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=529,
  serialized_end=545,
)


_SPORTSRESTARTREQ = _descriptor.Descriptor(
  name='SportsRestartReq',
  full_name='nana.biz.sports.SportsRestartReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=547,
  serialized_end=565,
)


_SPORTSRESTARTRES = _descriptor.Descriptor(
  name='SportsRestartRes',
  full_name='nana.biz.sports.SportsRestartRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=567,
  serialized_end=585,
)

_SPORTSMATCHESRES_MATCHESENTRY.fields_by_name['value'].message_type = nana_dot_sports_dot_match__pb2._MATCH
_SPORTSMATCHESRES_MATCHESENTRY.containing_type = _SPORTSMATCHESRES
_SPORTSMATCHESRES.fields_by_name['matches'].message_type = _SPORTSMATCHESRES_MATCHESENTRY
_MATCHODDS.fields_by_name['odds'].message_type = nana_dot_sports_dot_odds__pb2._ODDS
_SPORTSODDSRES.fields_by_name['data'].message_type = _MATCHODDS
DESCRIPTOR.message_types_by_name['SportsMatchesReq'] = _SPORTSMATCHESREQ
DESCRIPTOR.message_types_by_name['SportsMatchesRes'] = _SPORTSMATCHESRES
DESCRIPTOR.message_types_by_name['SportsOddsReq'] = _SPORTSODDSREQ
DESCRIPTOR.message_types_by_name['MatchOdds'] = _MATCHODDS
DESCRIPTOR.message_types_by_name['SportsOddsRes'] = _SPORTSODDSRES
DESCRIPTOR.message_types_by_name['SportsCheckReq'] = _SPORTSCHECKREQ
DESCRIPTOR.message_types_by_name['SportsCheckRes'] = _SPORTSCHECKRES
DESCRIPTOR.message_types_by_name['SportsRestartReq'] = _SPORTSRESTARTREQ
DESCRIPTOR.message_types_by_name['SportsRestartRes'] = _SPORTSRESTARTRES
DESCRIPTOR.enum_types_by_name['SportsSvrID'] = _SPORTSSVRID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SportsMatchesReq = _reflection.GeneratedProtocolMessageType('SportsMatchesReq', (_message.Message,), dict(
  DESCRIPTOR = _SPORTSMATCHESREQ,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsMatchesReq)
  ))
_sym_db.RegisterMessage(SportsMatchesReq)

SportsMatchesRes = _reflection.GeneratedProtocolMessageType('SportsMatchesRes', (_message.Message,), dict(

  MatchesEntry = _reflection.GeneratedProtocolMessageType('MatchesEntry', (_message.Message,), dict(
    DESCRIPTOR = _SPORTSMATCHESRES_MATCHESENTRY,
    __module__ = 'nana.biz.sport.match_pb2'
    # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsMatchesRes.MatchesEntry)
    ))
  ,
  DESCRIPTOR = _SPORTSMATCHESRES,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsMatchesRes)
  ))
_sym_db.RegisterMessage(SportsMatchesRes)
_sym_db.RegisterMessage(SportsMatchesRes.MatchesEntry)

SportsOddsReq = _reflection.GeneratedProtocolMessageType('SportsOddsReq', (_message.Message,), dict(
  DESCRIPTOR = _SPORTSODDSREQ,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsOddsReq)
  ))
_sym_db.RegisterMessage(SportsOddsReq)

MatchOdds = _reflection.GeneratedProtocolMessageType('MatchOdds', (_message.Message,), dict(
  DESCRIPTOR = _MATCHODDS,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.MatchOdds)
  ))
_sym_db.RegisterMessage(MatchOdds)

SportsOddsRes = _reflection.GeneratedProtocolMessageType('SportsOddsRes', (_message.Message,), dict(
  DESCRIPTOR = _SPORTSODDSRES,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsOddsRes)
  ))
_sym_db.RegisterMessage(SportsOddsRes)

SportsCheckReq = _reflection.GeneratedProtocolMessageType('SportsCheckReq', (_message.Message,), dict(
  DESCRIPTOR = _SPORTSCHECKREQ,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsCheckReq)
  ))
_sym_db.RegisterMessage(SportsCheckReq)

SportsCheckRes = _reflection.GeneratedProtocolMessageType('SportsCheckRes', (_message.Message,), dict(
  DESCRIPTOR = _SPORTSCHECKRES,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsCheckRes)
  ))
_sym_db.RegisterMessage(SportsCheckRes)

SportsRestartReq = _reflection.GeneratedProtocolMessageType('SportsRestartReq', (_message.Message,), dict(
  DESCRIPTOR = _SPORTSRESTARTREQ,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsRestartReq)
  ))
_sym_db.RegisterMessage(SportsRestartReq)

SportsRestartRes = _reflection.GeneratedProtocolMessageType('SportsRestartRes', (_message.Message,), dict(
  DESCRIPTOR = _SPORTSRESTARTRES,
  __module__ = 'nana.biz.sport.match_pb2'
  # @@protoc_insertion_point(class_scope:nana.biz.sports.SportsRestartRes)
  ))
_sym_db.RegisterMessage(SportsRestartRes)


_SPORTSMATCHESRES_MATCHESENTRY._options = None
# @@protoc_insertion_point(module_scope)
