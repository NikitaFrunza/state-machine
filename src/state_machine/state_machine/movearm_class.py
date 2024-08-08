import time
import rclpy
from yasmin import State
from yasmin import Blackboard
from yasmin import StateMachine
# from yasmin_viewer import YasminViewerPub
from geometry_msgs.msg import Pose

from std_msgs.msg import Bool, String, Int16

from .blackboard_class import shared_blackboard

class MoveArm(State):
    def __init__(self) -> None:
        super().__init__(["movearm_go_to_taskManager"])

    def execute(self, blackboard: Blackboard) -> str:
        print("Executing state Move Arm\n")
        time.sleep(3)
        # movearm_msg = Bool()
        # shared_blackboard.movearm = True
        # movearm_msg.data = shared_blackboard.movearm
        # shared_blackboard.go_to_scan_pose_publisher.publish(movearm_msg)
        # shared_blackboard.counter = 1
        # #create another topic for response from arm moved for pose
        # #modify the while loops for waiting so depending on the action to be perfomrmed go to the proper while loop
        # #create a var in shared blcakboard move_arm_scan, move_arm_pose. so if one is true i go to the appropriate while loop to wait for it 
        # while(shared_blackboard.movearm_response != "arm moved"): #arm moved for scan
        #     #while shared_blackboard.movearm_response != "arm moved for pose"
        #     print("waiting for update from scan")
        #     print(f"in the blackboard we have {shared_blackboard.movearm_response} ")
        #     time.sleep(0.1)
        # while(shared_blackboard.movearm_response != "arm moved"):
        #     print("waiting for update from target pose")
        #     print(f"in the blackboard we have {shared_blackboard.movearm_response} ")
        #     time.sleep(0.1)

        if (shared_blackboard.movearm_home.data == True):
            shared_blackboard.goto_homing_pose_publsiher.publish(shared_blackboard.movearm_home)
            while(shared_blackboard.movearm_response != "arm moved"):
                print("waiting for update from homing")
                time.sleep(0.1)
            shared_blackboard.movearm_home.data = False
            shared_blackboard.arm_moved_home = True # here can add if later, so if recived from arm good response then i say arm is moved home, othewise do other logic
            shared_blackboard.arm_moved_scan = False
            shared_blackboard.arm_moved_pick = False
            shared_blackboard.arm_moved_place = False

        if (shared_blackboard.movearm_scan.data == True):
            shared_blackboard.goto_scan_pose_publisher.publish(shared_blackboard.movearm_scan)
            while(shared_blackboard.movearm_response != "arm moved"):
                print("waiting for update from scan")
                time.sleep(0.1)
            shared_blackboard.movearm_scan.data = False
            shared_blackboard.arm_moved_scan = True
            shared_blackboard.arm_moved_home = False
            shared_blackboard.arm_moved_pick = False
            shared_blackboard.arm_moved_place = False

        if (shared_blackboard.movearm_pick_object.data == True):
            curr_obj_pose = shared_blackboard.needed_object_data["pose"]
            
            obj_pose = Pose()
            obj_pose.position.x = curr_obj_pose["position"]["x"]
            obj_pose.position.y = curr_obj_pose["position"]["y"]
            obj_pose.position.z = curr_obj_pose["position"]["z"]
            obj_pose.orientation.x = curr_obj_pose["orientation"]["x"]
            obj_pose.orientation.y = curr_obj_pose["orientation"]["y"]
            obj_pose.orientation.z = curr_obj_pose["orientation"]["z"]
            obj_pose.orientation.w = curr_obj_pose["orientation"]["w"]

            obj_name = shared_blackboard.needed_object_data["type"]

            # pose_string = f"pose: (position: (x: {obj_pose.position.x}, y: {obj_pose.position.y}, z: {obj_pose.position.z}), " \
            #   f"orientation: (x: {obj_pose.orientation.x}, y: {obj_pose.orientation.y}, z: {obj_pose.orientation.z}, w: {obj_pose.orientation.w}))"

            # # Combine pose string with object name
            # string_tosend = f"{pose_string}, '{obj_name}'"

            # shared_blackboard.pick_object_coordinates_publisher.publish(string_tosend)
            
            shared_blackboard.pick_object_coordinates_publisher.publish(obj_pose)
            while(shared_blackboard.movearm_response != "arm moved"):
                print("waiting for update from pick")
                time.sleep(0.1)
            shared_blackboard.movearm_pick_object.data = False
            shared_blackboard.arm_moved_pick = True
            shared_blackboard.arm_moved_scan = False
            shared_blackboard.arm_moved_home = False
            shared_blackboard.arm_moved_place = False

        if (shared_blackboard.movearm_place_object.data == True):
            shared_blackboard.place_object_coordinates_publisher.publish(shared_blackboard.needed_object_data)
            while(shared_blackboard.movearm_response != "arm moved"):
                print("waiting for update from place")
                time.sleep(0.1)
            shared_blackboard.movearm_place_object.data = False
            shared_blackboard.arm_moved_place = True
            shared_blackboard.arm_moved_scan = False
            shared_blackboard.arm_moved_home = False
            shared_blackboard.arm_moved_pick = False

        shared_blackboard.movearm_response = ""
        shared_blackboard.counter = 1
        

        return "movearm_go_to_taskManager"