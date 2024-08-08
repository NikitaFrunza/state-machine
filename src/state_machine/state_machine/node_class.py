import time
import rclpy
from rclpy.node import Node
from yasmin import State
from yasmin import Blackboard
from yasmin import StateMachine
# from yasmin_viewer import YasminViewerPub
from std_msgs.msg import Bool, String, Int16
from .blackboard_class import shared_blackboard
from geometry_msgs.msg import Pose
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

class NodeSM(Node):
    def __init__(self):
        super().__init__('my_subscriber_node')

        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT

        self.subscription = self.create_subscription(String,'/move_arm_response',self.move_arm_callback, qos_profile)
        self.subscription = self.create_subscription(String, 'input_string', self.input_string_callback, qos_profile)
        self.subscribtion = self.create_subscription(String, '/object_pose', self.object_pose_callback, qos_profile)
        self.subscription  # Prevent unused variable warning

        

    def move_arm_callback(self, msg):
        self.get_logger().info(f'I heard on subscribtion arm says: "{msg.data}"')
        shared_blackboard.movearm_response = msg.data

    def input_string_callback(self, msg):
        # self.get_logger().info(f'I heard on subscribtion input string: "{msg.data}"')
        shared_blackboard.input_string = msg.data

    def object_pose_callback(self, msg):
        # self.get_logger().info(f'I heard on subscribtion input string: "{msg.data}"')
        shared_blackboard.target_pose_objects_array = msg.data
        shared_blackboard.obj_pose_received = True
