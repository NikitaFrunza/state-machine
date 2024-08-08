from yasmin import Blackboard
from rclpy.publisher import Publisher
from rclpy.client import Client

class blackboardData(Blackboard):
    def __init__(self):
        super().__init__()
        self.goal = None
        self.pose = None

shared_blackboard_nav = blackboardData()
