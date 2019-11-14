import json

from pb import add_pb_to_path

json.JSONEncoder.item_separator = ','
json.JSONEncoder.key_separator = ':'
add_pb_to_path()


def patch_all(): pass
