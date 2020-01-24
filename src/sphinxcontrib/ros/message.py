# -*- coding: utf-8 -*-
u"""
    sphinxcontrib.ros.mssage
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :ros:message: directive.

    :copyright: Copyright 2015 by Tamaki Nishino.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function

import os
import codecs
import re
from sphinx.locale import _
from docutils import nodes
from docutils.statemachine import StringList
from docutils.parsers.rst import directives
from sphinx.util.docfields import TypedField, GroupedField

from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import (Punctuation, Literal,
                            Text, Comment, Operator, Name, Number, Keyword)

from .base import ROSObjectDescription

BUILTIN_TYPES = ('bool', 'byte',
                 'int8', 'uint8', 'int16', 'uint16',
                 'int32', 'uint32', 'int64', 'uint64',
                 'float32', 'float64', 'string', 'time', 'duration', 'Header')
TYPE_SUFFIX = 'type'
VALUE_SUFFIX = 'value'


def split_blocks(strings):
    u"""Split StringList into list of StringList
    """
    blocks = [StringList()]
    for item in strings.xitems():  # (source, offset, value)
        if item[2].strip():
            blocks[-1].append(item[2], source=item[0], offset=item[1])
        elif len(blocks[-1]):
            blocks.append(StringList())
    # remove the last block if empty
    if len(blocks[-1]) == 0:
        del blocks[-1]
    return blocks


def join_blocks(blocks):
    u"""Join list of StringList to single StringList
    """
    strings = StringList()
    for block in blocks:
        strings.extend(block)
        strings.extend(StringList([u'']))  # insert a blank line
    # remove the last blank line
    if strings and not strings[-1]:
        del strings[-1]
    return strings


def align_strings(strings, header=''):
    u"""Align StringList

    if header is not empty, add header
    """
    spaces = [len(l)-len(l.lstrip()) for l in strings.data if l]
    min_spaces = min(spaces) if spaces else 0
    if min_spaces > 0 or header:
        for index in range(len(strings.data)):
            strings.data[index] = header + strings.data[index][min_spaces:]


class ROSField(object):
    u"""A field or constant in a message file with comments
    """
    matcher = re.compile(r'([\w/]+)(\s*\[\s*\d*\s*\])?'
                         '\s+(\w+)(\s*=\s*[^#]+)?(\s*)(#.*)?$')

    def __init__(self, line, source=None, offset=0,
                 pre_comments='', package_name=''):
        self.source = source
        self.offset = offset
        result = self.matcher.match(line)
        if result is None:
            self.name = None
            return
        self.name = result.group(3)
        self.type = result.group(1)
        self.size = result.group(2).replace(' ', '') if result.group(2) else ''
        self.value = result.group(4).lstrip()[1:] if result.group(4) else ''
        comment = result.group(6) if result.group(6) else ''
        if self.type == 'string' and self.value:
            self.value += result.group(5) + comment
            comment = ''
        else:
            self.value = self.value.strip()
            comment = comment[1:]
        if self.type not in BUILTIN_TYPES:
            if '/' not in self.type:
                # if the type is not builtin type and misses the package name
                self.type = package_name + '/' + self.type
        elif self.type == 'Header':
            self.type = 'std_msgs/Header'
        self.comment = StringList([comment], items=[(source, offset)])
        self.pre_comments = pre_comments
        self.post_comments = StringList()

    def get_description(self, field_comment_option):
        u"""Get the description of the field
        """
        desc = StringList()
        pre_blocks = split_blocks(self.pre_comments)
        post_blocks = split_blocks(self.comment + self.post_comments)
        if 'up-all' in field_comment_option:
            desc = join_blocks(pre_blocks)
        elif 'up' in field_comment_option:
            if pre_blocks:
                desc = pre_blocks[-1]
        elif 'right1' in field_comment_option:
            desc = self.comment
        elif 'right-down' in field_comment_option:
            if post_blocks:
                desc = post_blocks[0]
        elif 'right-down-all' in field_comment_option:
            if post_blocks:
                desc = join_blocks(post_blocks)
        return desc


class ROSFieldGroup(object):
    u"""A group of fields and constants.
    """
    def __init__(self, package_name):
        self.package_name = package_name
        self.description = StringList()
        self.fields = []

    def append(self, line, source, offset):
        if line == '' or line[0] == '#':
            if line:
                line = line[1:]
            if self.fields:
                self.fields[-1].post_comments.append(line,
                                                     source=source,
                                                     offset=offset)
            else:
                self.description.append(line, source=source, offset=offset)
        else:
            if self.fields:
                pre_comments = self.fields[-1].post_comments
            else:
                pre_comments = self.description
            new_field = ROSField(line, source=source, offset=offset,
                                 pre_comments=pre_comments,
                                 package_name=self.package_name)
            # if sucessfully parsed
            if new_field.name:
                self.fields.append(new_field)
                self.pre_comments = StringList()
            else:
                # todo
                print("?? <%s>" % line)


class ROSFieldGroupType(object):
    u"""A specification for ROSFieldGroup.
    """
    def __init__(self, field_name=None, field_label=None,
                 constant_name=None, constant_label=None):
        self.field_name = field_name
        self.field_label = field_label
        self.constant_name = constant_name
        self.constant_label = constant_label

    def make_docfields(self, field_group, field_comment_option):
        docfields = StringList([u''])
        for field in field_group.fields:
            field_type = self.constant_name if field.value else self.field_name
            name = field.name + field.size
            desc = field.get_description(field_comment_option)
            if len(desc) == 0:
                docfields.append(u':{0} {1}:'.format(field_type, name),
                                 source=field.source, offset=field.offset)
            elif len(desc) == 1:
                docfields.append(u':{0} {1}: {2}'.format(field_type,
                                                         name,
                                                         desc[0].strip()),
                                 source=desc.source(0), offset=desc.offset(0))
            elif len(desc) > 1:
                if 'quote' in field_comment_option:
                    align_strings(desc, '  | ')
                else:
                    align_strings(desc, '  ')
                docfields.append(u':{0} {1}: {2}'.format(field_type,
                                                         name, desc[0]),
                                 source=desc.source(0), offset=desc.offset(0))
                docfields.extend(desc[1:])
            docfields.append(u':{0}-{1} {2}: {3}'.format(field_type,
                                                         TYPE_SUFFIX,
                                                         name,
                                                         field.type),
                             source=field.source, offset=field.offset)
            if field.value:
                docfields.append(u':{0}-{1} {2}: {3}'.format(field_type,
                                                             VALUE_SUFFIX,
                                                             name,
                                                             field.value),
                                 source=field.source, offset=field.offset)
        return docfields

    def get_doc_field_types(self):
        return [
            TypedField(self.field_name,
                       label=_(self.field_label),
                       names=(self.field_name,),
                       typerolename='msg',
                       typenames=('{0}-{1}'.format(self.field_name,
                                                   TYPE_SUFFIX),)),
            TypedField(self.constant_name,
                       label=_(self.constant_label),
                       names=(self.constant_name,),
                       typerolename='msg',
                       typenames=('{0}-{1}'.format(self.constant_name,
                                                   TYPE_SUFFIX),)),
            GroupedField('{0}-{1}'.format(self.constant_name,
                                          VALUE_SUFFIX),
                         label=_('{0} (Value)'.format(self.constant_label)),
                         names=('{0}-{1}'.format(self.constant_name,
                                                 VALUE_SUFFIX),)),
            ]

    def get_doc_merge_fields(self):
        return {'{0}-{1}'.format(self.constant_name, VALUE_SUFFIX):
                self.constant_name}


class ROSTypeFile(object):
    def __init__(self, ext=None, field_group_types=None):
        if field_group_types is None:
            field_group_types = []
        self.ext = ext
        self.field_group_types = field_group_types

    def get_doc_field_types(self):
        return [doc_field_type
                for field_group_type in self.field_group_types
                for doc_field_type in field_group_type.get_doc_field_types()]

    def get_doc_merge_fields(self):
        doc_merge_fields = {}
        for field_group_type in self.field_group_types:
            doc_merge_fields.update(field_group_type.get_doc_merge_fields())
        return doc_merge_fields

    def read(self, package_path, ros_type):
        type_file = os.path.join(package_path,
                                 self.ext,
                                 ros_type+'.'+self.ext)
        if not os.path.exists(type_file):
            file_content = None
        else:
            raw_content = codecs.open(type_file, 'r', 'utf-8').read()
            file_content = StringList(raw_content.splitlines(),
                                      source=type_file)
        return type_file, file_content

    def parse(self, file_content, package_name):
        u"""
        """
        field_groups = []
        field_group = ROSFieldGroup(package_name)
        for item in file_content.xitems():  # (source, offset, value)
            line = item[2].strip()
            if line and not [c for c in line if not c == '-']:
                field_groups.append(field_group)
                field_group = ROSFieldGroup(package_name)
            else:
                field_group.append(line, item[0], item[1])
        field_groups.append(field_group)
        return field_groups

    def make_docfields(self, field_groups, field_comment_option):
        docfields = StringList()
        for field_group_type, field_group in zip(self.field_group_types,
                                                 field_groups):
            docfields.extend(
                field_group_type.make_docfields(field_group,
                                                field_comment_option))
        return docfields


class ROSType(ROSObjectDescription):
    has_arguments = True

    option_spec = {
        'noindex': directives.flag,
    }

    def merge_field(self, src_node, dest_node):
        dest_node.insert(4, nodes.Text(':'))
        dest_node.insert(5, nodes.literal('', src_node[2].astext()))


class ROSAutoType(ROSType):
    option_spec = {
        'noindex': directives.flag,
        'base': directives.path,
        'description': directives.unchanged,
        'raw': lambda x: directives.choice(x, ('head', 'tail')),
        'field-comment': directives.unchanged,
    }

    def update_content(self):
        package_name, type_name = self.arguments[0].split('/', 1)
        package = self.find_package(package_name)
        if not package:
            return
        file_path, file_content \
            = self.type_file.read(os.path.dirname(package.filename),
                                  type_name)
        if file_content is None:
            self.state_machine.reporter.warning(
                'cannot find file {0}'.format(file_path),
                line=self.lineno)
            return
        type_relfile = os.path.relpath(file_path, self.env.srcdir)
        self.env.note_dependency(type_relfile)

        field_groups = self.type_file.parse(file_content, package_name)

        # fields
        options = self.options.get('field-comment', '')
        field_comment_option = options.lower().split()
        content = self.type_file.make_docfields(field_groups,
                                                field_comment_option)

        # description
        if field_groups:
            desc = field_groups[0].description
            desc_blocks = split_blocks(desc)
            if desc_blocks:
                description_option = [x.strip() for x in
                                      self.options.get('description', '').
                                      lower().split(',')]
                first = second = None
                for option in description_option:
                    if not option:  # ignore empty option
                        pass
                    elif ':' in option:
                        first, second = option.split(':', 1)
                    elif option == 'quote':
                        pass
                    else:
                        raise ValueError(
                            "unknown option {0} in "
                            "the description option".format(option))
                blocks = desc_blocks[(int(first) if first else None):
                                     (int(second) if second else None)]
                if blocks:
                    description = join_blocks(blocks)
                    if 'quote' in description_option:
                        align_strings(description, '| ')
                    else:
                        align_strings(description)
                    content = content + StringList([u'']) + description

        content = content + self.content
        # raw file content
        raw_option = self.options.get('raw', None)
        #
        if raw_option is not None:
            code_block = StringList([u'', u'.. code-block:: rostype', u''])
            code_block.extend(StringList(['    '+l for l in file_content.data],
                                         items=file_content.items))
            if raw_option == 'head':
                content = code_block + StringList([u'']) + content
            elif raw_option == 'tail':
                content = content + code_block
        return content

    def run(self):
        self.name = self.name.replace('auto', '')
        return ROSType.run(self)


class ROSMessageBase(object):
    type_file = ROSTypeFile(
        ext='msg',
        field_group_types=[
            ROSFieldGroupType(field_name='field',
                              field_label='Field',
                              constant_name='constant',
                              constant_label='Constant'),
        ])

    doc_field_types = type_file.get_doc_field_types()
    doc_merge_fields = type_file.get_doc_merge_fields()


class ROSMessage(ROSMessageBase, ROSType):
    pass


class ROSAutoMessage(ROSMessageBase, ROSAutoType):
    pass


class ROSServiceBase(object):
    type_file = ROSTypeFile(
        ext='srv',
        field_group_types=[
            ROSFieldGroupType(field_name='req-field',
                              field_label='Field (Request)',
                              constant_name='req-constant',
                              constant_label='Constant (Request)'),
            ROSFieldGroupType(field_name='res-field',
                              field_label='Field (Response)',
                              constant_name='res-constant',
                              constant_label='Constant (Response)')
        ])

    doc_field_types = type_file.get_doc_field_types()
    doc_merge_fields = type_file.get_doc_merge_fields()


class ROSService(ROSServiceBase, ROSType):
    pass


class ROSAutoService(ROSServiceBase, ROSAutoType):
    pass


class ROSActionBase(object):
    type_file = ROSTypeFile(
        ext='action',
        field_group_types=[
            ROSFieldGroupType(field_name='goal-field',
                              field_label='Field (Goal)',
                              constant_name='goal-constant',
                              constant_label='Constant (Goal)'),
            ROSFieldGroupType(field_name='result-field',
                              field_label='Field (Result)',
                              constant_name='result-constant',
                              constant_label='Constant (Result)'),
            ROSFieldGroupType(field_name='feedback-field',
                              field_label='Field (Feedback)',
                              constant_name='feedback-constant',
                              constant_label='Constant (Feedback)')
        ])

    doc_field_types = type_file.get_doc_field_types()
    doc_merge_fields = type_file.get_doc_merge_fields()


class ROSAction(ROSActionBase, ROSType):
    pass


class ROSAutoAction(ROSActionBase, ROSAutoType):
    pass


class ROSTypeLexer(RegexLexer):
    name = 'ROSTYPE'
    aliases = ['rostype']
    filenames = ['*.msg', '*.srv', '*.action']

    tokens = {
        'common': [
            (r'[ \t]+', Text),
            (r'#.*$', Comment.Single),
            (r'[\[\]]', Punctuation),
            (r'=', Operator),
            (r'\-?(\d+\.\d*|\.\d+)', Number.Float),
            (r'\-?\d+', Number.Integer),
            ],
        'field': [
            include('common'),
            (r'\n', Text, '#pop'),
            (r'\w+', Name.Property, '#pop'),
        ],
        'root': [
            include('common'),
            (r'\n', Text),
            (r'---\n', Keyword),
            (r'(string)(\s+)([a-zA-Z_]\w*)(\s*)(=)(\s*)(.*)(\s*\n)',
             bygroups(Name.Builtin, Text,
                      Name.Property, Text,
                      Operator, Text,
                      Literal.String, Text)),
            ('(' + '|'.join(BUILTIN_TYPES) + ')', Name.Builtin, 'field'),
            (r'[\w/]+', Name.Class, 'field'),
        ],
    }
