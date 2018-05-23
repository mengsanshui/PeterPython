#! /usr/bin/env python
'''
This is just a ROS action server example as study
'''
import rospy
import time
import actionlib
from basics.msg import TimerAction, TimerGoal, TimerResult
def do_timer(goal):
    start_time = time.time()
    time.sleep(goal.time_to_wait.to_sec())
    result = TimerResult()
    result.time_elapsed = rospy.Duration.from_sec(time.time() - start_time)
    result.updates_sent = 0
    server.set_succeeded(result)

rospy.init_node('action_server_timer')
server = actionlib.SimpleActionServer('TimerServer', TimerAction, do_timer, False)
server.start()
rospy.spin()


'''
This is a simple ROS action client 
'''
#! /usr/bin/env python
import rospy
import actionlib
from basics.msg import TimerAction, TimerGoal, TimerResult
rospy.init_node('action_client_timer')
client = actionlib.SimpleActionClient('TimerServer', TimerAction)
client.wait_for_server()
goal = TimerGoal()
goal.time_to_wait = rospy.Duration.from_sec(5.0)
client.send_goal(goal)
client.wait_for_result()
print('Time elapsed: %f'%(client.get_result().time_elapsed.to_sec()))