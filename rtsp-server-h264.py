import sys
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(TestRtspMediaFactory, self).__init__(**properties)
        self.loop = None
        self.h264file = None

    def do_create_element(self, url):
        # 使用 filesrc 和 h264parse 替代 qtdemux
        src = f"filesrc location={self.h264file} ! qtdemux ! queue"
        h264_depay = "h264parse ! rtph264pay name=pay0 pt=96"
        pipeline_str = f"{src} ! {h264_depay}"
        return Gst.parse_launch(pipeline_str)

class GstServer():
    def __init__(self, h264file):
        self.h264file = h264file
        self.loop = GLib.MainLoop()  # 使用 GLib.MainLoop 替代 GObject.MainLoop
        self.server = GstRtspServer.RTSPServer()
        self.factory = TestRtspMediaFactory()
        self.factory.h264file = self.h264file
        self.factory.set_shared(True)
        m = self.server.get_mount_points()
        m.add_factory("/test", self.factory)
        self.server.attach(None)

    def run(self):
        self.loop.run()

if __name__ == "__main__":
    Gst.init(None)
    h264file = sys.argv[1] if len(sys.argv) > 1 else "test.h264"
    server = GstServer(h264file)
    server.run()

