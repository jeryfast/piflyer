from unittest import TestCase
import commander


class TestCommander(TestCase):
    def test_update(self):
        self.x = commander()
        self.x.update("C,10,-2")
        self.assertEquals(self.x.getParameters(), [10.0, -2.0, 0.0])
        self.x.update("C,10,-2,50")
        self.assertEquals(self.x.getParameters(), [10.0, -2.0, 50.0])
        #absent throttle data must result in no throttle change
        self.x.update("C,10,-2")
        self.assertEquals(self.x.getParameters(), [10.0, -2.0, 50.0])
        self.assertEquals(self.x.status, "OK")
        # self.fail()

    def test_control(self):
        self.x = commander()
        #mode manual
        self.x.update("M,m")
        self.x.update("C,10,-2")
        self.x.control()
        # mode stabilized
        self.x.update("M,s")
        self.x.update("C,10,-2")
        self.x.control()
        #self.fail()
