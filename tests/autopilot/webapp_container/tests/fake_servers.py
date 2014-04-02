# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2014 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License version 3, as
# published by the Free Software Foundation.

""" Autopilot tests for the webapp_container package """

import os
import BaseHTTPServer
import threading
import subprocess

from autopilot.testcase import AutopilotTestCase

from ubuntuuitoolkit import emulators as toolkit_emulators


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def serve_content(self, content, mime_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()
        self.wfile.write(content)

    def basic_html_content(self):
        return """
<html>
<head>
<title>Some content</title>
</head>
<body>
This is some content
</body>
</html>
        """

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.serve_content(self.basic_html_content())
        else:
            self.send_error(404)

class WebappContainerContentHttpServer(threading.Thread):
    def __init__(self):
        super(WebappContainerContentHttpServer, self).__init__()
        self.server = BaseHTTPServer.HTTPServer(("", 0), RequestHandler)
        self.server.allow_reuse_address = True

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

