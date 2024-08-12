import time
import rclpy
from yasmin import State
from yasmin import Blackboard
from yasmin import StateMachine
# from yasmin_viewer import YasminViewerPub

from .blackboard_class import shared_blackboard
from .bb_test import bb

class TaskManager(State):
    def __init__(self) -> None:
        super().__init__(["taskmanager_go_to_navigation", "taskmanager_go_to_moveArm", "taskmanager_go_to_visualAnalysis"])

        print(bb.init_state)

        self.tasks = ["navigation", "visual_analysis", "move_arm"]
        self.next_task_index = 0
        self.current_state_index = 0

        # self.pick_keys_list = list(shared_blackboard.environment_data_array[0]["arena_start_state"])
        # self.place_keys_list = list(shared_blackboard.environment_data_array[0]["arena_target_state"])

        self.location_pickup_tracker = 0
        self.object_pickup_tracker = 0

        self.goto_pickupws_state = True
        self.goto_placews_state = False

        self.start_pickup_obj = False
        self.start_place_obj = False

        self.array_of_objs_on_robot = []

        self.object_to_place = None

        self.move_arm_to_scan = False

        self.get_object_poses = False

    def choose_object_to_pickup(self) -> bool:
        pickup_location = None
        if (self.location_pickup_tracker < len(shared_blackboard.environment_data_array[0]["arena_start_state"][self.location_pickup_tracker])):
            print("object to pickup chosen")
            print(self.object_pickup_tracker)
            pickup_location = shared_blackboard.environment_data_array[0]["arena_start_state"][self.location_pickup_tracker]
        # probably remove the equal sign to work correctly
        if (len(pickup_location["objects"]) > self.object_pickup_tracker):
            object_to_pickup = pickup_location["objects"][self.object_pickup_tracker]
            self.array_of_objs_on_robot.append(object_to_pickup)
            shared_blackboard.needed_object_data = object_to_pickup
            print(object_to_pickup)
            self.object_pickup_tracker += 1
            return True
        else:
            return False

    def choose_location_pickup(self):
        sizearena = len(shared_blackboard.environment_data_array[0]["arena_start_state"])
        print(f"Inside choose_location_pickup location pickup tracker is {self.location_pickup_tracker} and size of arena state is {sizearena}")
        if (self.location_pickup_tracker <= len(shared_blackboard.environment_data_array[0]["arena_start_state"])):
            print("choose location pickup function condition is true")
            shared_blackboard.needed_location = shared_blackboard.environment_data_array[0]["arena_start_state"][self.location_pickup_tracker]
            return True
        else:
            return False
        
    def choose_object_place(self):
        print("find object to be placed")
        # print(self.array_of_objs_on_robot)
        if (self.array_of_objs_on_robot):
            self.object_to_place = self.array_of_objs_on_robot.pop(0)
            return True
        else:
            return False

    def choose_location_place(self):
        result = self.choose_object_place()
        print("object to be placed is ")
        print(result)
        if result:
            print("find location where object has to be placed")
            locations = shared_blackboard.environment_data_array[0]["arena_target_state"]
            target_location = None
            for location in locations:
                objects = location["objects"]
                for obj in objects:
                    if obj["id"] == self.object_to_place["id"]:
                        target_location = location
                        shared_blackboard.needed_location = target_location
                        break
                if target_location:
                    break
            print("Selected target location is ")
            print(target_location)
            return True
        return False


    def execute(self, blackboard: Blackboard) -> str:
        print("Executing state Task Manager\n")
        # time.sleep(3)

        current_state = self.tasks[self.current_state_index]
        
        # if (current_state == "navigation"):
        #     self.next_task_index = 0

        if (current_state == "navigation"):
            if (shared_blackboard.arm_moved_home is not True):
                self.next_task_index = 2
                shared_blackboard.movearm_home.data = True
                shared_blackboard.movearm_scan.data = False
            else:
                if (shared_blackboard.out_of_reach is True):
                    print("logic for out of reach")
                    shared_blackboard.out_of_reach = False

                elif (self.goto_pickupws_state is True):
                    print("task manager telling navigation to go to pickup location")
                    result = self.choose_location_pickup()
                    print(f"location choose to pickup result is: {result}")
                    if (result):
                        print(self.location_pickup_tracker)
                        self.start_pickup_obj = True
                        self.goto_pickupws_state = False
                        # self.location_pickup_tracker += 1
                    else:
                        self.location_pickup_tracker = 0
                        print("pickup locations finished")
                    self.next_task_index = self.current_state_index
                    self.current_state_index = 1

                elif (self.goto_placews_state is True):
                    print("navigation going to the place station")
                    location_found = self.choose_location_place()
                    if location_found: #if location found then next state to execute is navigate to it but after navigation task manager current satet has to be move arm place
                        self.start_place_obj = True
                        self.next_task_index = self.current_state_index
                        self.current_state_index = 2
                    else:
                        self.current_state_index = 0
                        self.next_task_index = self.current_state_index
                        self.goto_placews_state = False


                self.next_task_index = self.current_state_index
                self.current_state_index = 1

        elif (current_state == "visual_analysis"):
            if (shared_blackboard.arm_moved_scan == False):
                print("task manager moving arm to scan")
                self.move_arm_to_scan = True
                shared_blackboard.movearm_scan.data = True
                shared_blackboard.movearm_home.data = False
                self.next_task_index = 2
                self.get_object_poses = True
            elif (self.get_object_poses):
                print("task manager tell visual analysisto wait for object pose")
                shared_blackboard.obj_pose_received = False
                self.next_task_index = self.current_state_index
                self.get_object_poses = False
                # self.move_arm_to_scan = False
            else:
                self.current_state_index = 2
                self.next_task_index = self.current_state_index
            # time.sleep(0.1)

        elif (current_state == "move_arm"):
            # self.current_state_index = 0
            if (shared_blackboard.out_of_reach is True or shared_blackboard.objects_not_found is True):
                self.next_task_index = 0

            # elif (self.move_arm_to_scan):
            #     shared_blackboard.movearm_scan.data = True
            #     self.next_task_index = 2
            #     self.current_state_index = 1

            else:
                if (self.start_pickup_obj):
                    print("task manager tells arm to picking object")
                    print(self.object_pickup_tracker)
                    result = self.choose_object_to_pickup()
                    print(f"result is {result}")
                    if (result):
                        print("object to pickup selected")
                        shared_blackboard.movearm_pick_object.data = True
                        self.next_task_index = 2
                        # if (len(self.array_of_objs_on_robot) > 3): 
                        #     self.next_task_index = 0
                        #     self.goto_placews_state = True
                        #     self.start_pickup_obj = False
                        #     self.object_pickup_tracker = 0
                        #     # self.location_pickup_tracker = 0
                        #     self.current_state_index = 0
                        #     self.next_task_index = self.current_state_index
                        # else:
                        #     self.next_task_index = 2
                    else:
                        # self.next_task_index = 2
                        self.current_state_index = 0
                        self.next_task_index = self.current_state_index
                        self.goto_placews_state = True
                        self.start_pickup_obj = False
                        self.object_pickup_tracker = 0
                        # self.location_pickup_tracker = 0
                        self.current_state_index = 0

                elif (self.start_place_obj):
                    print("arm placing object")
                    shared_blackboard.movearm_place_object.data = True
                    if (len(self.array_of_objs_on_robot) == 0):
                        self.next_task_index = self.current_state_index #next state is go to move arm to place
                        self.current_state_index = 0
                        self.goto_placews_state = True
                        self.start_place_obj = False
                        self.location_pickup_tracker += 1
                        shared_blackboard.movearm_place_object.data = True
                
                else:
                    self.next_task_index = self.current_state_index
        
            time.sleep(0.1)



        next_task = self.tasks[self.next_task_index]

        if (next_task == "navigation"):
            return "taskmanager_go_to_navigation"
        elif (next_task == "visual_analysis"):
            return "taskmanager_go_to_visualAnalysis"
        elif (next_task == "move_arm"):
            return "taskmanager_go_to_moveArm"




























        # if (shared_blackboard.counter == 1):
        #     shared_blackboard.movearm_home.data = True
        #     return "taskmanager_go_to_navigation"
        
        # elif (shared_blackboard.counter == 2):
        #     shared_blackboard.movearm_scan.data = True
        #     return "taskmanager_go_to_visualAnalysis" 
        
        # elif (shared_blackboard.counter == 3):
        #     if shared_blackboard.environment_data_array and shared_blackboard.environment_data_array[0] is not None:
        #         shared_blackboard.movearm_pick_object.data = True
        #     if shared_blackboard.environment_data_array and shared_blackboard.environment_data_array[1] is not None:
        #         shared_blackboard.movearm_place_object.data = True
        #     return "taskmanager_go_to_moveArm"
    