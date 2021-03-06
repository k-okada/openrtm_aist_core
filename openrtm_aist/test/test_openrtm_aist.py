#!/usr/bin/env python

PKG = 'openrtm_aist'
import roslib; roslib.load_manifest(PKG)  # This line is not needed with Catkin.

import os
import sys
import unittest

code = """
#include <rtm/Manager.h>
int main (int argc, char** argv)
{
  RTC::Manager* manager;
  manager = RTC::Manager::init(argc, argv);
  return 0;
}
"""
from subprocess import call, check_output, Popen, PIPE, STDOUT

## A sample python unit test
class TestCompile(unittest.TestCase):
    PKG_CONFIG_PATH = ''

    def setUp(self):
        # if rosbuild environment
        openrtm_path = check_output(['rospack','find','openrtm_aist']).rstrip()
        if os.path.exists(os.path.join(openrtm_path, "bin")) :
            self.PKG_CONFIG_PATH='PKG_CONFIG_PATH=%s/lib/pkgconfig:$PKG_CONFIG_PATH'%(openrtm_path)

    ## test 1 == 1
    def test_compile_pkg_config(self):
        global PID
        print "`pkg-config openrtm-aist --cflags --libs` =",check_output("%s pkg-config openrtm-aist --cflags --libs"%(self.PKG_CONFIG_PATH), shell=True, stderr=STDOUT)
        print "%s g++ -o openrtm-sample-pkg-config /tmp/%d-openrtm-sample.cpp `pkg-config openrtm-aist --cflags --libs`"%(self.PKG_CONFIG_PATH, PID)
        ret = call("g++ -o openrtm-sample-pkg-config /tmp/%d-openrtm-sample.cpp `%s pkg-config openrtm-aist --cflags --libs`"%(PID, self.PKG_CONFIG_PATH), shell=True)
        self.assertTrue(ret==0)

    def test_compile_rtm_config(self):
        global PID
        print "`rosrun openrtm_aist rtm-config --cflags --libs` =",check_output("rosrun openrtm_aist rtm-config --cflags --libs", shell=True, stderr=STDOUT)
        ret = call("g++ -o openrtm-sample-pkg-config /tmp/%d-openrtm-sample.cpp `rosrun openrtm_aist rtm-config --cflags --libs`"%(PID), shell=True)
        self.assertTrue(ret==0)

    def test_share(self):
        # check if rtshell runs
        print "`rospack find openrtm_aist`/share/openrtm-1.1/example/rtc.conf = ",os.path.join(check_output(['rospack','find','openrtm_aist']).rstrip(), "share/openrtm-1.1/example/rtc.conf")
        self.assertTrue(os.path.exists(os.path.join(check_output(['rospack','find','openrtm_aist']).rstrip(), "share/openrtm-1.1/example/rtc.conf")))

    def test_example(self):
        print "`pkg-config openrtm-aist --variable=rtm_exampledir`/SeqInComp =",os.path.join(check_output("%s pkg-config openrtm-aist --variable=rtm_exampledir"%(self.PKG_CONFIG_PATH), shell=True).rstrip(), "SeqInComp")
        self.assertTrue(os.path.exists(os.path.join(check_output("%s pkg-config openrtm-aist --variable=rtm_exampledir"%(self.PKG_CONFIG_PATH), shell=True).rstrip(), "SeqInComp")))
        print "`pkg-config openrtm_aist rtm-config --rtm-exampledir`/SeqInComp =",os.path.join(check_output(['rosrun','openrtm_aist','rtm-config','--rtm-exampledir']).rstrip(), "SeqInComp")
        self.assertTrue(os.path.exists(os.path.join(check_output(['rosrun','openrtm_aist','rtm-config','--rtm-exampledir']).rstrip(), "SeqInComp")))

if __name__ == '__main__':
    import rostest
    global PID
    PID = os.getpid()
    f = open("/tmp/%d-openrtm-sample.cpp"%(PID),'w')
    f.write(code)
    f.close()
    rostest.rosrun(PKG, 'test_openrtm_aist', TestCompile) 



