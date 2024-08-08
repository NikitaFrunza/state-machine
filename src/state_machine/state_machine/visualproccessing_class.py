import time
import rclpy
from yasmin import State
from yasmin import Blackboard
from yasmin import StateMachine
# from yasmin_viewer import YasminViewerPub
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool, String, Int16
import ast

from .blackboard_class import shared_blackboard

class VisualAnalysis(State):
    def __init__(self) -> None:
        super().__init__(["visualanalysis_go_to_taskManager"])

    def execute(self, blackboard: Blackboard) -> str:
        print("Executing state Visual Analysis\n")

        visual_target_pose = Pose()
        visual_target_pose.position.x = 0.395
        visual_target_pose.position.y = -0.16
        visual_target_pose.position.z = 0.445
        visual_target_pose.orientation.x = 0.884
        visual_target_pose.orientation.y = 0.467
        visual_target_pose.orientation.z = -0.0003
        visual_target_pose.orientation.w = 0.00014

        # if (shared_blackboard.movearm_home.data == True):
        #     shared_blackboard.goto_homing_pose_publsiher.publish(shared_blackboard.movearm_home)
        #     while(shared_blackboard.movearm_response != "arm moved"):
        #         print("waiting for update from homing")
        #         time.sleep(0.1)

        start_cam = Bool()
        start_cam.data = True
        shared_blackboard.start_vision_publisher.publish(start_cam)

        while (shared_blackboard.obj_pose_received is not True):
            print("waiting for objects poses")
            time.sleep(0.1)
            
        start_cam.data = False

        # Split the string by '/'
        split_strings = shared_blackboard.target_pose_objects_array .split('/')

        # Strip leading and trailing whitespace from each segment
        split_strings = [s.strip() for s in split_strings]

        # Convert each segment to a dictionary
        object_poses = [ast.literal_eval(obj_str) for obj_str in split_strings]

        # maybe obj["pose"] does not update shared_blackboard.environment_data_array
        locations = shared_blackboard.environment_data_array[0]["arena_start_state"]

        for location in locations:
            objects = location["objects"]
            for obj in objects:
                for obj_pose in object_poses:
                    if (obj["type"] == obj_pose["type"]):
                        obj["pose"] = obj_pose["pose"]


        time.sleep(3)
        shared_blackboard.counter = 3

        return "visualanalysis_go_to_taskManager"