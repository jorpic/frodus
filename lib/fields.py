#!/usr/bin/env python3

import yaml

with open("fields-spec.yaml") as f:
    known_fields = yaml.safe_load(f)


def name_value(fld):
    name = fld['name']
    val = fld[known_fields[name].get('value', 'value')]
    if isinstance(val, str):
        val = val.strip()
    return (name, val)
