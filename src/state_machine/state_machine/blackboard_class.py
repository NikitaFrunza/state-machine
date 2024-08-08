from yasmin import Blackboard
from rclpy.publisher import Publisher
from rclpy.client import Client
from rclpy.node import Node
from std_msgs.msg import Bool, String, Int16
from geometry_msgs.msg import Pose

class blackboardData(Blackboard):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.next_state = None

        self.places = []

        #info about environment
        self.environment_data_array = []

        #visual analysis
        self.target_pose_objects_array = None #object pose
        self.out_of_reach = False
        self.objects_not_found = False
        self.obj_pose_received = False
        

        # arm
        self.movearm = False
        self.movearm_response = False
        self.movearm_scan = Bool(data = False)
        self.movearm_home = Bool(data = False)
        self.movearm_pick_object = Bool(data = False)
        self.movearm_place_object = Bool(data = False)
        self.arm_moved_home = False
        self.arm_moved_scan = False
        self.arm_moved_pick = False
        self.arm_moved_place = False
        self.needed_object_data = None

        #navigation
        self.navigation_pose = None
        self.needed_location = None
        self.navigation_succeded = False

        #initialization
        self.input_string = ""

    def init_publishers(self, node: Node):
        self.goto_scan_pose_publisher = node.create_publisher(Bool, '/go_scan', 10) #go to pre visual analysis position
        self.goto_homing_pose_publsiher = node.create_publisher(Bool, '/go_drive', 10) #homing position set
        self.pick_object_coordinates_publisher = node.create_publisher(Pose, '/object_coordinates_arm', 10) #coordinates of object to be picked
        self.place_object_coordinates_publisher = node.create_publisher(Pose, '/goal_coordinates_arm', 10) #coordinates of place where object is placed
        self.start_vision_publisher = node.create_publisher(Bool, '/start_camera', 10) #telling vision to start 
        

shared_blackboard = blackboardData()
