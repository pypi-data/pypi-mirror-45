"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2011 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs import Message
from sleekxmppfs.xmlstream import register_stanza_plugin
from sleekxmppfs.xmlstream.handler import Callback
from sleekxmppfs.xmlstream.matcher import StanzaPath
from sleekxmppfs.plugins import BasePlugin
from sleekxmppfs.plugins.xep_0004 import stanza
from sleekxmppfs.plugins.xep_0004.stanza import Form, FormField, FieldOption


class XEP_0004(BasePlugin):

    """
    XEP-0004: Data Forms
    """

    name = 'xep_0004'
    description = 'XEP-0004: Data Forms'
    dependencies = set(['xep_0030'])
    stanza = stanza

    def plugin_init(self):
        self.xmpp.register_handler(
            Callback('Data Form',
                 StanzaPath('message/form'),
                 self.handle_form))

        register_stanza_plugin(FormField, FieldOption, iterable=True)
        register_stanza_plugin(Form, FormField, iterable=True)
        register_stanza_plugin(Message, Form)

    def plugin_end(self):
        self.xmpp.remove_handler('Data Form')
        self.xmpp['xep_0030'].del_feature(feature='jabber:x:data')

    def session_bind(self, jid):
        self.xmpp['xep_0030'].add_feature('jabber:x:data')

    def make_form(self, ftype='form', title='', instructions=''):
        f = Form()
        f['type'] = ftype
        f['title'] = title
        f['instructions'] = instructions
        return f

    def handle_form(self, message):
        self.xmpp.event("message_xform", message)

    def build_form(self, xml):
        return Form(xml=xml)
