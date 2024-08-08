#!/usr/bin/env python3

import threading
import rclpy
from rclpy.node import Node
from yasmin import StateMachine, State
from std_msgs.msg import Bool, String, Int16


class MyNode(Node):
    def __init__(self):
        super().__init__("py_node")
        self.get_logger().info("Hello")

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

