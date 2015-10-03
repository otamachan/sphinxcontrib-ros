# -*- coding: utf-8 -*-
u"""
    sphinxcontrib.ros.package
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :ros:package: directive.

    :copyright: Copyright 2015 by Tamaki Nishino
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.locale import l_
from sphinx.util.docfields import Field

from .base import ROSObjectDescription, GroupedFieldNoArg


def default_formatter(value):
    return [unicode(value)]


def description_formatter(value):
    if '</a>' in value or '</p>' in value:
        content = [u".. raw:: html", "", "   " + value]
    else:
        content = default_formatter(value)
    return content


def url_formatter(url):
    return [url.type + '<' + url.url + '>']


def person_formatter(person):
    replaces = {'@': ' AT ', '.': ' DOT '}
    email = person.email
    if email:
        for old, new in replaces.items():
            email = email.replace(old, new)
        content = person.name + ' <' + email + '>'
    else:
        content = person.name
    return [content]


def depend_formatter(depend):
    return [':ros:pkg:`{0}`'.format(depend.name)]

FORMATTERS = {
    'default_formatter': default_formatter,
    'description_formatter': description_formatter,
    'url_formatter': url_formatter,
    'person_formatter': person_formatter,
    'depend_formatter': depend_formatter
}


def add_formatter(formatter_name, formatter):
    global FORMATTERS
    FORMATTERS[formatter_name] = formatter


def format_attr(package, attr, formatter_name='default_formatter'):
    value = getattr(package, attr, None)
    field_name = attr if not attr.endswith('s') else attr[:-1]
    field_header = u':' + field_name + ':'
    formatter = FORMATTERS[formatter_name]
    field_content = []
    if value:
        if attr.endswith('s'):
            for v in value:
                field_content.append(field_header)
                field_content.extend(['   '+line for line in formatter(v)])
        else:
            field_content.append(field_header)
            field_content.extend(['   '+line for line in formatter(value)])
        return StringList(field_content)


# http://www.ros.org/reps/rep-0127.html
class ROSPackage(ROSObjectDescription):
    option_spec = {
        'noindex': directives.flag,
    }
    package_attrs = (
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
    )
    doc_field_types = [
        GroupedFieldNoArg(attr[:-1],
                          label=l_(''.join(w.title()
                                           for w in attr.split('_'))),
                          names=(attr[:-1],))
        if attr.endswith('s') else
        Field(attr, label=l_(attr.title()), names=(attr,), has_arg=False)
        for attr in package_attrs
    ]


class ROSAutoPackage(ROSPackage):
    option_spec = {
        'noindex': directives.flag,
        'base': directives.path,
    }
    attr_formatters = {
        'description': 'description_formatter',
        'maintainers': 'person_formatter',
        'urls': 'url_formatter',
        'authors': 'person_formatter',
        'conflicts': 'depend_formatter',
        'replaces': 'depend_formatter',
    }

    def update_content(self):
        package_name = self.arguments[0]
        package = self.find_package(package_name)
        if not package:
            return None
        self.env.note_dependency(self.env.relfn2path(package.filename)[0])
        content = StringList()
        for attr in self.env.config.ros_package_attrs:
            if attr in self.env.config.ros_package_attrs_formatter:
                formatter = self.env.config.ros_package_attrs_formatter[attr]
            elif attr.endswith('_depends'):
                formatter = 'depend_formatter'
            else:
                formatter = self.attr_formatters.get(attr, 'default_formatter')
            field = format_attr(package, attr, formatter)
            if field:
                content.extend(field)
        content.items = [(source, 0) for source, line in content.items]
        if len(content) > 0:
            content.append(StringList([u'']))
        return content + self.content

    def run(self):
        self.name = self.name.replace('auto', '')
        return ROSPackage.run(self)
