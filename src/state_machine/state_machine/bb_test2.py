from .bb_test import bb
from .bb_test3 import main as main_bb_test3
def main():
    bb.arm_moved = True
    print(bb.counter)
    # main_bb_test3()
    # print(bb.object_placed)
    # print(bb.init_state)
if __name__ == "__main__":
    main()