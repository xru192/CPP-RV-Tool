#!/usr/bin/env python
#!/usr/bin/env python

import json
from collections import namedtuple


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())


def project_from_json(json_file_name):
    p = Project()
    with open(json_file_name, "r") as f:
        o = json.load(f, object_hook=_json_object_hook)
        for att in dir(p):
            if att.startswith('project_') and hasattr(o, att):
                setattr(p, att, getattr(o, att))
    return p


class Project(object):
    project_name = None
    project_compile_commands_file = None
    project_linked_libs = None
    project_bitcode_file = None
    project_function_type_json_file = None
    project_dse_bitcode_file = None
    project_dse_function_json_file = None
    project_dse_executable_file = None
    project_coverage_bitcode_file = None
    project_coverage_binary_file = None
    project_coverage_executable_file = None
    project_coverage_json_file = None

    project_config_file = None
    project_build_dir = None

    def __init__(self):
        return


if __name__ == '__main__':
    p = project_from_json('/home/zbchen/FDSE/symcc/test/real-world/raylib/build/raylib/libraylib.so.4.0.0_config.json')
