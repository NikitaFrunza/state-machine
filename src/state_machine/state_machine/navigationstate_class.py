import time
import rclpy
from yasmin import State
from yasmin import Blackboard
from yasmin import StateMachine
# from yasmin_viewer import YasminViewerPub

from .blackboard_class import shared_blackboard
from .navigation_class import Navigation

class NavigationClass(State):
    def __init__(self) -> None:
        super().__init__(["navigation_go_to_taskManager"])
        self.nav = Navigation()

    def execute(self, blackboard: Blackboard) -> str:
        print("Executing state Navigation\n")
        # time.sleep(3)

        nav = Navigation()
        destination = shared_blackboard.needed_location
        print(destination)
        self.nav.set_params(destination)
        result = self.nav.start_navigation()

    #     nav = Navigation()
    #     destinations = shared_blackboard.places
    #     # print(destinations)
    #     while (destinations):
    #         current_dest = destinations.pop(0)
    #         print("current destination")
    #         print(current_dest)
    #         self.nav.set_params(current_dest)
    #         result = self.nav.start_navigation()
    #         time.sleep(20)

    #     finish = {
    #     'pose': {
    #         'position': {
    #             'x': 2.196580171585083,
    #             'y': -3.1218459606170654,
    #             'z': 0.0
    #         },
    #         'orientation': {
    #             'x': 0.0,
    #             'y': 0.0,
    #             'z': -0.7055570313355489,
    #             'w': 0.7086531419058038
    #         }
    #     }
    # }
        
    #     self.nav.set_params(finish)
    #     result = self.nav.start_navigation()

        # if result == "succeeded":
        #     shared_blackboard.navigation_succeded = True

        shared_blackboard.counter = 2

        return "navigation_go_to_taskManager"