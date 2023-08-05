"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import logging

from sleekxmppfs import Iq
from sleekxmppfs.plugins import BasePlugin
from sleekxmppfs.xmlstream.handler import Callback
from sleekxmppfs.xmlstream.matcher import StanzaPath
from sleekxmppfs.xmlstream import register_stanza_plugin
from sleekxmppfs.plugins.xep_0049 import stanza, PrivateXML


log = logging.getLogger(__name__)


class XEP_0049(BasePlugin):

    name = 'xep_0049'
    description = 'XEP-0049: Private XML Storage'
    dependencies = set([])
    stanza = stanza

    def plugin_init(self):
        register_stanza_plugin(Iq, PrivateXML)

    def register(self, stanza):
        register_stanza_plugin(PrivateXML, stanza, iterable=True)

    def store(self, data, ifrom=None, block=True, timeout=None, callback=None):
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq['from'] = ifrom

        if not isinstance(data, list):
            data = [data]

        for elem in data:
            iq['private'].append(elem)

        return iq.send(block=block, timeout=timeout, callback=callback)

    def retrieve(self, name, ifrom=None, block=True, timeout=None, callback=None):
        iq = self.xmpp.Iq()
        iq['type'] = 'get'
        iq['from'] = ifrom
        iq['private'].enable(name)
        return iq.send(block=block, timeout=timeout, callback=callback)
