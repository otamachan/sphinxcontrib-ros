# -*- coding: utf-8 -*-
u"""
    sphinxcontrib.ros
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    The ROS domain.

    :copyright: Copyright 2015 by Tamaki Nishino
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function

from sphinx.domains import Domain, ObjType
from sphinx.locale import l_
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode

from .package import ROSPackage, ROSAutoPackage, add_formatter
from .message import (ROSMessage, ROSAutoMessage, ROSService,
                      ROSAutoService, ROSAction, ROSAutoAction, ROSTypeLexer)
from .api import ROSAPI


class ROSDomain(Domain):
    u"""
    ROS domain
    """
    name = 'ros'
    label = 'ros'
    object_types = {
        'package': ObjType(l_('package'), 'pkg'),
        'message': ObjType(l_('message'), 'msg'),
        'service': ObjType(l_('service'), 'srv'),
        'action': ObjType(l_('action'), 'action'),
        'node': ObjType(l_('node'), 'node'),
    }
    directives = {
        'package': ROSPackage,
        'autopackage': ROSAutoPackage,
        'message':  ROSMessage,
        'automessage':  ROSAutoMessage,
        'service':  ROSService,
        'autoservice':  ROSAutoService,
        'action':  ROSAction,
        'autoaction':  ROSAutoAction,
        'node':  ROSAPI,
    }
    roles = {
        'pkg':  XRefRole(),
        'msg':  XRefRole(),
        'srv':  XRefRole(),
        'action':  XRefRole(),
        'node':  XRefRole(),
    }
    initial_data = {
        'objects': {}  # (objtype, name) -> docname
    }

    def clear_doc(self, docname):
        for fullname, fn in list(self.data['objects'].items()):
            if fn == docname:
                del self.data['objects'][fullname]

    def merge_domaindata(self, docnames, otherdata):
        for fullname, docname in otherdata['objects'].items():
            if docname in docnames:
                self.data['objects'][fullname] = docname

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        objects = self.data['objects']
        objtypes = self.objtypes_for_role(typ)
        for objtype in objtypes:
            if (objtype, target) in objects:
                return make_refnode(builder, fromdocname,
                                    objects[objtype, target],
                                    objtype + '-' + target,
                                    contnode, target)

    def resolve_any_xref(self, env, fromdocname, builder, target, node,
                         contnode):
        objects = self.data['objects']
        results = []
        for objtype in self.object_types:
            if (objtype, target) in self.data['objects']:
                results.append(('ros:' + self.role_for_objtype(objtype),
                                make_refnode(builder, fromdocname,
                                             objects[objtype, target],
                                             objtype + '-' + target,
                                             contnode, target)))
        return results

    def get_objects(self):
        for (typ, name), docname in self.data['objects'].items():
            yield name, name, typ, docname, typ + '-' + name, 1


def setup(app):
    u"""
    setup
    """
    app.add_config_value('ros_package_attrs', [
        'version',
        'description',
        'maintainers',
        'licenses',
        'urls',
        'authors',
        'build_depends',
        'buildtool_depends',
        'build_export_depends',
        'buildtool_export_depends',
        'exec_depends',
        'test_depends',
        'doc_depends',
        'conflicts',
        'replaces',
        'exports',
    ], True)
    app.add_config_value('ros_package_attrs_formatter', {}, True)
    app.add_config_value('ros_base_path', [], True)
    app.add_domain(ROSDomain)
    app.add_lexer("rostype", ROSTypeLexer())
    return {'version': '0.1.0', 'parallel_read_safe': True}

__all__ = [
    'add_formatter'
]
