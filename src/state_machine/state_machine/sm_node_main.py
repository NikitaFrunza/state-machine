#!/usr/bin/env python3

import threading
import rclpy
from rclpy.node import Node
from yasmin import StateMachine, State
from std_msgs.msg import Bool, String, Int16

from .blackboard_class import shared_blackboard
from .navigationstate_class import NavigationClass
from .initialization_class import Initialization
from .taskmanager_class import TaskManager
from .movearm_class import MoveArm
from .visualproccessing_class import VisualAnalysis
from .node_class import NodeSM


def main():
    # init ROS 2
    rclpy.init()
    sm_node = NodeSM()
    shared_blackboard.init_publishers(sm_node)
    
    # create a FSM
    sm = StateMachine(outcomes=["finish"])

    # add states
    sm.add_state(
        "Initialization",
        Initialization(),
        transitions={
            "go_to_taskManager": "Task_Manager"
        }
    )
    sm.add_state(
        "Task_Manager",
        TaskManager(),
        transitions={
            "taskmanager_go_to_navigation": "Navigation",
            "taskmanager_go_to_moveArm": "Move_Arm",
            "taskmanager_go_to_visualAnalysis": "Visual_Analysis"
        }
    )
    sm.add_state(
        "Navigation",
        NavigationClass(),
        transitions={
            "navigation_go_to_taskManager": "Task_Manager"
        }
    )    
    sm.add_state(
        "Visual_Analysis",
        VisualAnalysis(),
        transitions={
            "visualanalysis_go_to_taskManager": "Task_Manager"
        }
    )
    sm.add_state(
        "Move_Arm",
        MoveArm(),
        transitions={
            "movearm_go_to_taskManager": "Task_Manager"
        }
    )

    
    # execute FSM
    def execute_sm():        
        outcome = sm()
        print(outcome)

    sm_thread = threading.Thread(target=execute_sm)
    sm_thread.start()

    rclpy.spin(sm_node)

    # shutdown ROS 2
    sm_thread.join()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

