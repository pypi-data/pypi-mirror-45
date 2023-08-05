##############################################################################
#
# Copyright (c) 2019 Jens Vagelpohl and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import unittest


class FakeServer(dict):

    def start(self):
        pass


SERVER = FakeServer()


def fake_init(address, app, **kw):
    global SERVER
    SERVER.clear()

    SERVER['app'] = app
    SERVER['address'] = address
    SERVER.update(kw)

    return SERVER


class CherootInitializationTests(unittest.TestCase):

    def test__makeBool(self):
        from dataflake.wsgi.cheroot import _makeBool

        for value in ('On', 'TRUE', '1'):
            self.assertTrue(_makeBool(value))

        for value in ('off', 'False', '0'):
            self.assertFalse(_makeBool(value))

    def test_initialization(self):
        # Install fake server class first
        from dataflake.wsgi import cheroot
        old_impl = cheroot.LoggingWSGIServer
        cheroot.LoggingWSGIServer = fake_init

        from dataflake.wsgi.cheroot import serve_paste

        global SERVER

        # The defaults
        serve_paste(None, None)
        self.assertEqual(SERVER['address'], ('0.0.0.0', 8080))

        # Host and port set
        serve_paste(None, None, host='localhost', port='8888')
        self.assertEqual(SERVER['address'], ('localhost', 8888))

        # Test integer fixup
        serve_paste(None, None, numthreads='2', max='-1',
                    request_queue_size='99', timeout='0',
                    shutdown_timeout='5', accepted_queue_size='-1',
                    accepted_queue_timeout='999')
        self.assertEqual(SERVER['numthreads'], 2)
        self.assertEqual(SERVER['max'], -1)
        self.assertEqual(SERVER['request_queue_size'], 99)
        self.assertEqual(SERVER['timeout'], 0)
        self.assertEqual(SERVER['shutdown_timeout'], 5)
        self.assertEqual(SERVER['accepted_queue_size'], -1)
        self.assertEqual(SERVER['accepted_queue_timeout'], 999)

        # Test boolean fixup
        serve_paste(None, None, peercreds_enabled='OFF',
                    peercreds_resolve_enabled='On')
        self.assertEqual(SERVER['peercreds_enabled'], False)
        self.assertEqual(SERVER['peercreds_resolve_enabled'], True)

        # Clean up fake server class
        cheroot.LoggingWSGIServer = old_impl
