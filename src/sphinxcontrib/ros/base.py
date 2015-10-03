# -*- coding: utf-8 -*-
u"""
    sphinxcontrib.ros.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    ROS base object and utilities.

    :copyright: Copyright 2015 by Tamaki Nishino.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function

from docutils import nodes
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.locale import _
from sphinx.util.docfields import Field

from catkin_pkg.packages import find_packages


class GroupedFieldNoArg(Field):
    u"""
    """
    is_grouped = True
    list_type = nodes.bullet_list

    def __init__(self, name, names=(), label=None, rolename=None):
        Field.__init__(self, name, names, label, False, rolename)

    def make_field(self, types, domain, items):
        fieldname = nodes.field_name('', self.label)
        listnode = self.list_type()
        for fieldarg, content in items:
            listnode += nodes.list_item('', nodes.paragraph('', '', *content))
        fieldbody = nodes.field_body('', listnode)
        return nodes.field('', fieldname, fieldbody)


class ROSObjectDescription(ObjectDescription):
    u"""ROS Object"""
    _ros_packages = {}
    doc_merge_fields = {}

    def find_package(self, name):
        if 'base' in self.options and self.options['base'] is not None:
            base_abspath = self.env.relfn2path(self.options['base'])[1]
            packages = find_packages(base_abspath)
            package = next((package for package in packages.values()
                            if package.name == name), None)
        else:
            if not ROSObjectDescription._ros_packages:
                packages = {}
                base_paths = self.env.config.ros_base_path
                if not base_paths:
                    base_paths = ['.']
                for base_path in base_paths:
                    if base_path.startswith('/'):
                        base_abspath = base_path
                    else:
                        base_abspath = self.env.relfn2path(base_path)[1]
                    found_packages = find_packages(base_abspath)
                    for package in found_packages.values():
                        packages[package.name] = package
                ROSObjectDescription._ros_packages = packages
            package = ROSObjectDescription._ros_packages.get(name, None)
        if not package:
            self.state_machine.reporter.warning(
                'cannot find package %s' % name,
                line=self.lineno)
        return package

    def handle_signature(self, sig, signode):
        sig = sig.strip()
        signode += addnodes.desc_name(sig, sig)
        return sig

    def add_target_and_index(self, name, sig, signode):
        targetname = self.objtype + '-' + name
        fullname = (self.objtype, name)
        if targetname not in self.state.document.ids:
            signode['names'].append(targetname)
            signode['ids'].append(targetname)
            signode['first'] = not self.names
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['ros']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % name +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname]),
                    line=self.lineno)
            objects[fullname] = self.env.docname
        indextext = _('%s (ROS %s)') % (name, self.objtype)
        self.indexnode['entries'].append(('single', indextext,
                                          targetname,
                                          ''))

    def before_content(self):
        content = self.update_content()
        if content:
            self.content = content
            # save
            self.tmp_backup = {'content_offset':
                               self.content_offset,
                               'input_lines':
                               self.state.state_machine.input_lines,
                               'get_source_and_line':
                               self.state.reporter.get_source_and_line}
            # overwrite variables to deal with source lines properly
            self.content_offset = 0
            self.state.state_machine.input_lines = self.content
            self.state.reporter.get_source_and_line = self.get_source_and_line

    def after_content(self):
        if hasattr(self, 'tmp_backup'):
            # restore
            self.content_offset = self.tmp_backup['content_offset']
            self.state.state_machine.input_lines \
                = self.tmp_backup['input_lines']
            self.state.reporter.get_source_and_line \
                = self.tmp_backup['get_source_and_line']

    def update_content(self):
        return self.content

    def get_source_and_line(self, lineno=None):
        if lineno is None:
            srcline = None
            src = None
        else:
            src, srcline = self.content.info(lineno)
        return (src, srcline)

    def merge_field(self, src_node, dest_node):
        pass

    def run(self):
        node = ObjectDescription.run(self)
        contentnode = node[1][-1]
        # label is the key to find the field-value
        labelmap = {field_type.name: unicode(field_type.label)  # name -> label
                    for field_type in self.doc_field_types}
        field_nodes = {}
        for child in contentnode:
            if isinstance(child, nodes.field_list):
                for field in child:
                    if isinstance(field, nodes.field):
                        # label -> field_node
                        field_nodes[field[0].astext()] = field
        # merge
        for field_src, field_dest in self.doc_merge_fields.items():
            # name -> label -> field_node
            label_src = labelmap[field_src]
            if label_src in field_nodes:
                field_node_src = field_nodes[label_src]
                label_dest = labelmap[field_dest]
                if label_dest in field_nodes:
                    field_node_dest = field_nodes[label_dest]
                    for item_src in field_node_src[1][0]:
                        name = item_src[0][0].astext()
                        for item_dest in field_node_dest[1][0]:
                            if name == item_dest[0][0].astext():
                                # merge first paragraph
                                self.merge_field(item_src[0],
                                                 item_dest[0])
                for child in contentnode:
                    if isinstance(child, nodes.field_list):
                        child.remove(field_node_src)
        return node
