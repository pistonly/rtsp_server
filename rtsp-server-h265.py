import sys
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(TestRtspMediaFactory, self).__init__(**properties)
        self.hevcfile = None

    def do_create_element(self, url):
        # 使用 qtdemux 解析 MP4 容器，并使用 h265parse 解析视频流
        # pipeline_str = f"filesrc location={self.hevcfile} ! qtdemux ! queue ! h265parse ! rtph265pay name=pay0 pt=96"
        pipeline_str = f"filesrc location={self.hevcfile} ! h265parse ! rtph265pay name=pay0 pt=96"
        pipeline = Gst.parse_launch(pipeline_str)

        # 监听总线消息以处理循环播放
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.on_eos, pipeline)

        return pipeline

    def on_eos(self, bus, msg, pipeline):
        # 重新开始播放
        pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)

class GstServer():
    def __init__(self, hevcfile):
        self.hevcfile = hevcfile
        self.loop = GLib.MainLoop()  # 使用 GLib.MainLoop
        self.server = GstRtspServer.RTSPServer()
        self.factory = TestRtspMediaFactory()
        self.factory.hevcfile = self.hevcfile
        self.factory.set_shared(True)
        m = self.server.get_mount_points()
        m.add_factory("/test", self.factory)
        self.server.attach(None)

    def run(self):
        self.loop.run()

if __name__ == "__main__":
    Gst.init(None)
    hevcfile = sys.argv[1] if len(sys.argv) > 1 else "3840x2160_8bit.h265"
    server = GstServer(hevcfile)
    server.run()

