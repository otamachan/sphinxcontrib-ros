# -*- coding: utf-8 -*-
u"""
    sphinxcontrib.ros.api
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :ros:node: directive.

    :copyright: Copyright 2015 by Tamaki Nishino.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function

from docutils.parsers.rst import directives
from docutils import nodes
from sphinx.locale import _
from sphinx.util.docfields import GroupedField, TypedField

from .base import ROSObjectDescription


class ROSAPI(ROSObjectDescription):
    option_spec = {
        'noindex': directives.flag,
        'base': directives.path,
    }
    doc_field_types = [
        TypedField('pub',
                   label=_('Published Topics'),
                   names=('pub',),
                   typerolename='msg', typenames=('pub-type',)),
        TypedField('sub',
                   label=_('Subscribed Topics'),
                   names=('sub',),
                   typerolename='msg', typenames=('sub-type',)),
        TypedField('srv', label=_('Services'),
                   names=('srv',),
                   typerolename='srv', typenames=('srv-type',)),
        TypedField('srv_called',
                   label=_('Services Called'),
                   names=('srv_called',),
                   typerolename='srv', typenames=('srv_called-type',)),
        TypedField('action',
                   label=_('Actions'),
                   names=('action',),
                   typerolename='action', typenames=('action-type',)),
        TypedField('action_called',
                   label=_('Actions Called'),
                   names=('action_called',),
                   typerolename='action', typenames=('action_called-type',)),
        TypedField('param',
                   label=_('Parameters'),
                   names=('param',),
                   typenames=('param-type',)),
        TypedField('param_set',
                   label=_('Parameters Set'),
                   names=('param_set',),
                   typenames=('param_set-type',)),
        GroupedField('param-default',
                     label=_('Parameters Default Value'),
                     names=('param-default',)),
        GroupedField('param_set-default',
                     label=_('Parameters Set Default Value'),
                     names=('param_set-default',)),
    ]
    doc_merge_fields = {
        'param-default': 'param',
        'param_set-default': 'param_set'
    }

    def merge_field(self, src_node, dest_node):
        dest_node.insert(4, nodes.Text(' (default: '))
        dest_node.insert(5, nodes.literal('', src_node[2].astext()))
        dest_node.insert(6, nodes.Text(')'))
