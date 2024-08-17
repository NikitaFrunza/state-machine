import time
import rclpy
from yasmin import State
from yasmin import Blackboard
from yasmin import StateMachine
# from yasmin_viewer import YasminViewerPub

from .blackboard_class import shared_blackboard

# from .a_blackboard import my_blackboard
class TaskManager(State):
    def __init__(self) -> None:
        super().__init__(["taskmanager_go_to_navigation", "taskmanager_go_to_moveArm", "taskmanager_go_to_visualAnalysis"])



    def execute(self, blackboard: Blackboard) -> str:
        print("Executing TaskManager")