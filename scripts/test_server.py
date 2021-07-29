#! /usr/bin/env python
# test server, real one run on amir

import rospy
from std_srvs.srv import Trigger, TriggerResponse

def trigger_response(request):
    return TriggerResponse(success=True, message='ok amir go stand by')

rospy.init_node('test_server') 
my_service = rospy.Service('/amir_start_service', Trigger, trigger_response)
rospy.spin()