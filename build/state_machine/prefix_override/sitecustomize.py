import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/rosbuntu/Desktop/state_machine_ws/install/state_machine'
