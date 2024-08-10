import random

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose
from nav2_msgs.action import NavigateToPose

from yasmin import CbState
from yasmin import Blackboard
from yasmin import StateMachine
from yasmin_ros import ActionState
from yasmin_ros.basic_outcomes import SUCCEED, ABORT, CANCEL
from yasmin_viewer import YasminViewerPub

from .navigation_blackboard_class import shared_blackboard_nav

HAS_NEXT = "has_next"
END = "end"

class Navigation:
    def __init__(self):
        self.blackboard = Blackboard()
        self.nav_sm = StateMachine(outcomes=[SUCCEED, ABORT, CANCEL])
        self._create_sm()
        
    def _create_sm(self):
        self.nav_sm.add_state(
            "SET_GOAL",
            CbState([SUCCEED], self.set_goal),
            transitions={SUCCEED: "NAVIGATING"}
        )
        self.nav_sm.add_state(
            "NAVIGATING",
            Nav2State(),
            transitions={
                SUCCEED: SUCCEED,
                CANCEL: CANCEL,
                ABORT: ABORT  
            }
        )
  
    # def set_params(self, goal: tuple):
    #     self.blackboard.goal = goal 

    # def set_goal(self, blackboard: Blackboard) -> str:
    #     goal = blackboard.goal  

    #     pose = Pose()
    #     pose.position.x = goal[0]
    #     pose.position.y = goal[1]
    #     pose.orientation.z = goal[2]
    #     pose.orientation.w = goal[3]
    #     blackboard.pose = pose 
    #     return SUCCEED 
    
    def set_params(self, goal):
        self.blackboard.goal = goal

    def set_goal(self, blackboard: Blackboard) -> str:
        navigation_goal = blackboard.goal

        position = navigation_goal["pose"]["position"]
        orientation = navigation_goal["pose"]["orientation"]

        pose = Pose()

        pose.position.x = position["x"]
        pose.position.y = position["y"]
        pose.position.z = position["z"]
        pose.orientation.x = orientation["x"]
        pose.orientation.y = orientation["y"]
        pose.orientation.z = orientation["z"]
        pose.orientation.w = orientation["w"]

        # navigation_goal = blackboard.goal

        # position = navigation_goal["pose"]["position"]
        # orientation = navigation_goal["pose"]["orientation"]

        # pose = Pose()

        # pose.position.x = position["x"]
        # pose.position.y = position["y"]
        # pose.position.z = position["z"]
        # pose.orientation.x = orientation["x"]
        # pose.orientation.y = orientation["y"]
        # pose.orientation.z = orientation["z"]
        # pose.orientation.w = orientation["w"]

        # print("pose of the destination")
        # print(pose)

        blackboard.pose = pose      

        return SUCCEED

    def start_navigation(self) -> str:
        YasminViewerPub("Navigation FSM", self.nav_sm)
        return self.nav_sm(self.blackboard)  

class Nav2State(ActionState):
    def __init__(self) -> None:
        super().__init__(
            NavigateToPose,  # Action type
            "/navigate_to_pose",  # Action name
            self.create_goal_handler,  # Callback to create the goal
            None,  # Outcomes, includes (SUCCEED, ABORT, CANCEL)
            None  # Callback to process the response
        )

    def create_goal_handler(self, blackboard: Blackboard) -> NavigateToPose.Goal:
        goal = NavigateToPose.Goal()
        goal.pose.pose = blackboard.pose  # Use pose from the shared blackboard
        goal.pose.header.frame_id = "map"
        return goal



