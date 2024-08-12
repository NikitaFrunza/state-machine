import time
import rclpy
from yasmin import State
from yasmin import Blackboard
from yasmin import StateMachine
# from yasmin_viewer import YasminViewerPub

from .rosbag_parser_class import RosbagParser
from .blackboard_class import shared_blackboard

from .bb_test import bb
#add a function which can use the dictionary to find the needed workstation (ex. WS01) and add to it to it the location on the map
#as a nre, separate array object for that workstation so would be like 
# 'WS03': [{'object': 17, 'target': 0, 'object_type': 'M30', 'location': (1.36, -2.08, 0.0, 1.80)

class Initialization(State):
    def __init__(self) -> None:
        super().__init__(["go_to_taskManager"])
        bb.init_state = "coming from init state"
        print(bb.counter)
        # print(bb.object_placed)
        self.arena_array = []

        self.ws_pose_dict = {
            'WS01': {
                    'position': {'x': 1.9244441986, 'y': 4.92034030, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.69700362, 'w': 0.7170675988}
            },
            'WS02': {
                    'position': {'x': 1.99993574, 'y': 6.32392685, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.7430598982, 'w': 0.6692249156}
            },
            'WS03': {
                    'position': {'x': 6.137911319732666, 'y': 5.4621148109436035, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.39593910413074607, 'w': 0.9182767697269393}
            },
            'WS04': {
                    'position': {'x': 4.3728156089782715, 'y': 4.197620391845703, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.01514480706978665, 'w': 0.9998853108326069}
            },
            'WS05': {
                    'position': {'x': 5.615399360656738, 'y': 3.9833414554595947, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.9996739212208946, 'w': 0.025535293827183628}
            },
            'WS06': {
                    'position': {'x': 3.432215929031372, 'y': 1.4613157510757446, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.020702729865410555, 'w': 0.9997856755205686}
            },
            'WS07': {
                    'position': {'x': 4.652684688568115, 'y': 1.4068031311035156, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.9996821987452877, 'w': 0.025209155316810283}
            },
            'WS08': {
                    'position': {'x': 5.6072163581848145, 'y': 1.177388310432434, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.03696196254651506, 'w': 0.9993166731945935}
            },
            'WS09': {
                    'position': {'x': 5.634782314300537, 'y': -0.12611526250839233, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.037995065333237134, 'w': 0.9992779268103159}
            },
            'WS10': {
                    'position': {'x': 2.5427045822143555, 'y': -0.6764813661575317, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.030121273934482957, 'w': 0.9995462514844242}
            },
            'WS11': {
                    'position': {'x': 3.7749104499816895, 'y': -0.6779744029045105, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.9995174114358681, 'w': 0.031063551576428414}
            },
            'WS12': {
                    'position': {'x': 5.093892574310303, 'y': -2.052351474761963, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.9219364783587585, 'w': 0.3873411027394981}
            },
            'WS13': {
                    'position': {'x': 4.345003604888916, 'y': -2.983733892440796, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.36637720757398007, 'w': 0.930466410876982}
            },
            'WS14': {
                    'position': {'x': 4.096377372741699, 'y': -3.1645636558532715, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.9037166555565109, 'w': 0.4281310622575223}
            },
            'SH01': {
                    'position': {'x': 4.695500373840332, 'y': 5.831582069396973, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.6696278031725259, 'w': 0.7426968461077083}
            },
            'SH02': {
                    'position': {'x': 5.345235347747803, 'y': -1.840674877166748, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.42899354839037657, 'w': 0.9033075530733891}
            },
            'PP01': {
                    'position': {'x': 5.8394317626953125, 'y': 2.8510496616363525, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.024769996753105396, 'w': 0.9996931765601139}
            },
            'RT01': {
                    'position': {'x': 5.26912260055542, 'y': -3.290691614151001, 'z': 0.0},
                    'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.3553576195131485, 'w': 0.9347304222362447}
            }
        }

    def init_queue(self):
        # shared_blackboard.places.append((1.047, -0.01, 0.0, 2.988))
        # shared_blackboard.places.append((-1.776, -0.757, 0.0, -2.334))
        # shared_blackboard.places.append((-0.96, -0.51, 0.0, 1.80))
        # shared_blackboard.places.append((-0.11, -1.83, 0.0, 1.80))
        locations_pickup = self.arena_array[0]["arena_start_state"]
        locations_place = self.arena_array[0]["arena_target_state"]

        for location in locations_pickup:
            shared_blackboard.places.append(location)
        for location in locations_place:
            shared_blackboard.places.append(location)

        shared_blackboard.places

    def update_ws_poses(self):
        all_locations = []

        locations_pickup = self.arena_array[0]["arena_start_state"]
        locations_place = self.arena_array[0]["arena_target_state"]

        all_locations.extend(locations_pickup)
        all_locations.extend(locations_place)

        for location in all_locations:
            if location["name"] in self.ws_pose_dict:
                location["pose"] = self.ws_pose_dict[location["name"]]
        print()

    def execute(self, blackboard: Blackboard) -> str:
        print("Executing state Initialization\n")
        # self.init_queue()

        # while(shared_blackboard.input_string == ""):
        #     print("waiting for string")
        #     time.sleep(0.1)

        # parser = RosbagParser(shared_blackboard.input_string)
        # self.arena_array = parser.parse_tasks()
        # self.update_ws_poses()
        # shared_blackboard.environment_data_array = self.arena_array
        # print(shared_blackboard.environment_data_array)
        # self.init_queue()
        # print(shared_blackboard.environment_data_array)

        # time.sleep(3)
        shared_blackboard.counter = 1

        return "go_to_taskManager"