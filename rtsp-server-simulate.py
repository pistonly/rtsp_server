#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

Gst.init(None)

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        pipeline_str = "videotestsrc ! videoconvert ! x264enc tune=zerolatency ! rtph264pay name=pay0 pt=96"
        return Gst.parse_launch(pipeline_str)

class GstServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        self.factory = TestRtspMediaFactory()
        self.factory.set_shared(True)
        mount_points = self.server.get_mount_points()
        mount_points.add_factory("/test", self.factory)
        self.server.attach(None)
        print("RTSP server is running at rtsp://localhost:8554/test")

if __name__ == '__main__':
    s = GstServer()
    loop = GLib.MainLoop()
    loop.run()
    
