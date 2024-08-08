import re

class RosbagParser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.task_data_list = []
        # self.task_regex_pattern = re.compile(r'atwork_commander_msgs_msgTask\(header=std_msgsmsgHeader\(seq=(\d+), stamp=builtin_interfacesmsgTime\(sec=(\d+), nanosec=(\d+), __msgtype=\'builtin_interfaces/msg/Time\'\), frame_id=\'(.*?)\', __msgtype=\'std_msgs/msg/Header\'\), execute_on=\[(.*?)\], arena_start_state=\[(.*?)\], arena_target_state=\[(.*?)\], prep_time=builtin_interfacesmsgDuration\(sec=(\d+), nanosec=(\d+), __msgtype=\'builtin_interfaces/msg/Duration\'\), exec_time=builtin_interfacesmsgDuration\(sec=(\d+), nanosec=(\d+), __msgtype=\'builtin_interfaces/msg/Duration\'\), type=\'(\w+)\', id=(\d+), config=\'(.*?)\', commit=\d+, __msgtype_=\'atwork_commander_msgs/msg/Task\'\)')
        # self.workstation_regex_pattern = re.compile(r"atwork_commander_msgsmsgWorkstation\(objects=\[(.*?)\], name='(\w+)', type='(\d+)', pose=geometry_msgsmsgPose\(position=geometry_msgsmsgPoint\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+).*?orientation=geometry_msgsmsgQuaternion\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+), w=(-?\d+\.\d+)")
        # self.object_regex_pattern = re.compile(r"atwork_commander_msgsmsgObject\(object=(\d+), target=(\d+), decoy=(True|False), pose=geometry_msgsmsgPoseStamped\(header=std_msgsmsgHeader\(.*?pose=geometry_msgsmsgPose\(position=geometry_msgsmsgPoint\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+).*?orientation=geometry_msgsmsgQuaternion\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+), w=(-?\d+\.\d+)")

        self.task_regex_pattern = re.compile(r'atwork_commander_msgs__msg__Task\(header=std_msgs__msg__Header\(seq=(\d+), stamp=builtin_interfaces__msg__Time\(sec=(\d+), nanosec=(\d+), __msgtype__=\'builtin_interfaces/msg/Time\'\), frame_id=\'(.*?)\', __msgtype__=\'std_msgs/msg/Header\'\), execute_on=\[(.*?)\], arena_start_state=\[(.*?)\], arena_target_state=\[(.*?)\], prep_time=builtin_interfaces__msg__Duration\(sec=(\d+), nanosec=(\d+), __msgtype__=\'builtin_interfaces/msg/Duration\'\), exec_time=builtin_interfaces__msg__Duration\(sec=(\d+), nanosec=(\d+), __msgtype__=\'builtin_interfaces/msg/Duration\'\), type=\'(\w+)\', id=(\d+), config=\'(.*?)\', commit=\d+, __msgtype__=\'atwork_commander_msgs/msg/Task\'\)')
        self.workstation_regex_pattern = re.compile(r"atwork_commander_msgs__msg__Workstation\(objects=\[(.*?)\], name='(\w+)', type='(\d+)', pose=geometry_msgs__msg__Pose\(position=geometry_msgs__msg__Point\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+).*?orientation=geometry_msgs__msg__Quaternion\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+), w=(-?\d+\.\d+)")
        self.object_regex_pattern = re.compile(r"atwork_commander_msgs__msg__Object\(object=(\d+), target=(\d+), decoy=(True|False), pose=geometry_msgs__msg__PoseStamped\(header=std_msgs__msg__Header\(.*?pose=geometry_msgs__msg__Pose\(position=geometry_msgs__msg__Point\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+).*?orientation=geometry_msgs__msg__Quaternion\(x=(-?\d+\.\d+), y=(-?\d+\.\d+), z=(-?\d+\.\d+), w=(-?\d+\.\d+)")


        self.object_type_dict = {
            11: 'F20_20_B', 12: 'F20_20_G', 13: 'S40_40_B', 14: 'S40_40_G', 15: 'M20_100', 
            16: 'M20', 17: 'M30', 18: 'R20', 20: 'Axis2', 21: 'Bearing2', 22: 'Housing', 
            23: 'Motor2', 24: 'Spacer', 25: 'Screwdriver', 26: 'Wrench', 27: 'Drill', 
            28: 'AllenKey', 30: 'ROCKIN_START', 31: 'BEARING_BOX', 32: 'BEARING', 
            33: 'AXIS', 34: 'DISTANCE_TUBE', 35: 'MOTOR', 40: 'CONTAINER_START', 
            41: 'CONTAINER_END', 50: 'CAVITY_START', 51: 'F20_20_V', 52: 'F20_20_F', 
            53: 'S40_40_H', 54: 'S40_40_V', 55: 'S40_40_F', 56: 'M20_H', 57: 'M20_V', 
            58: 'M20_F', 59: 'M20_100_H', 60: 'M20_100_V', 61: 'M20_100_F', 62: 'M30_H', 
            63: 'M30_V', 64: 'M30_F', 65: 'R20_H', 66: 'R20_V', 67: 'R20_F'
        }

    def parse_tasks(self):
        tasks = re.findall(self.task_regex_pattern, self.input_string)
        
        for task_match in tasks:
            header_seq, header_stamp_sec, header_stamp_nanosec, frame_id, execute_on, arena_start_state_str, arena_target_state_str, prep_time_sec, prep_time_nanosec, exec_time_sec, exec_time_nanosec, task_type, task_id, config = task_match

            arena_start_state = self._process_arena_state(arena_start_state_str)
            arena_target_state = self._process_arena_state(arena_target_state_str)
            
            task_data = {
                'header': {
                    'seq': int(header_seq),
                    'stamp': {
                        'sec': int(header_stamp_sec),
                        'nanosec': int(header_stamp_nanosec)
                    },
                    'frame_id': frame_id
                },
                'execute_on': execute_on.split(', ') if execute_on else [],
                'arena_start_state': arena_start_state,
                'arena_target_state': arena_target_state,
                'prep_time': {'sec': int(prep_time_sec), 'nanosec': int(prep_time_nanosec)},
                'exec_time': {'sec': int(exec_time_sec), 'nanosec': int(exec_time_nanosec)},
                'type': task_type,
                'id': int(task_id),
                'config': config
            }

            self.task_data_list.append(task_data)
        
        return self.task_data_list

    def _process_arena_state(self, arena_state_str):
        if not arena_state_str:
            return []
        
        workstations_data = []
        for work_match in re.finditer(self.workstation_regex_pattern, arena_state_str):
            objects_str, name, type_, px, py, pz, ox, oy, oz, ow = work_match.groups()
            objects_data = self._process_objects(objects_str)

            workstation_data = {
                'name': name,
                'type': type_,
                'pose': {
                    'position': {'x': float(px), 'y': float(py), 'z': float(pz)},
                    'orientation': {'x': float(ox), 'y': float(oy), 'z': float(oz), 'w': float(ow)}
                },
                'objects': objects_data
            }
            workstations_data.append(workstation_data)
        
        return workstations_data

    def _process_objects(self, objects_str):
        objects_data = []
        for obj_match in re.finditer(self.object_regex_pattern, objects_str):
            id, target, decoy_str, px, py, pz, ox, oy, oz, ow = obj_match.groups()
            decoy = True if decoy_str == 'True' else False
            object_type_id = int(id)
            object_type = self.object_type_dict.get(object_type_id, 'Unknown')

            obj_data = {
                'id': int(id),
                'target': int(target),
                'decoy': decoy,
                'type': object_type,
                'pose': {
                    'position': {'x': float(px), 'y': float(py), 'z': float(pz)},
                    'orientation': {'x': float(ox), 'y': float(oy), 'z': float(oz), 'w': float(ow)}
                }
            }
            objects_data.append(obj_data)
        
        return objects_data

# Example usage:

# input_string = "atwork_commander_msgs_msgTask(header=std_msgsmsgHeader(seq=14, stamp=builtin_interfacesmsgTime(sec=0, nanosec=0, __msgtype='builtin_interfaces/msg/Time'), frame_id='', __msgtype='std_msgs/msg/Header'), execute_on=[], arena_start_state=[atwork_commander_msgsmsgWorkstation(objects=[atwork_commander_msgsmsgObject(object=12, target=0, decoy=False, pose=geometry_msgsmsgPoseStamped(header=std_msgsmsgHeader(seq=0, stamp=builtin_interfacesmsgTime(sec=0, nanosec=0, __msgtype='builtin_interfaces/msg/Time'), frame_id='', __msgtype='std_msgs/msg/Header'), pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype='atwork_commander_msgs/msg/Object'), atwork_commander_msgsmsgObject(object=15, target=0, decoy=False, pose=geometry_msgsmsgPoseStamped(header=std_msgsmsgHeader(seq=0, stamp=builtin_interfacesmsgTime(sec=0, nanosec=0, __msgtype='builtin_interfaces/msg/Time'), frame_id='', __msgtype='std_msgs/msg/Header'), pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype='atwork_commander_msgs/msg/Object'), atwork_commander_msgsmsgObject(object=16, target=0, decoy=False, pose=geometry_msgsmsgPoseStamped(header=std_msgsmsgHeader(seq=0, stamp=builtin_interfacesmsgTime(sec=0, nanosec=0, __msgtype='builtin_interfaces/msg/Time'), frame_id='', __msgtype='std_msgs/msg/Header'), pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype='atwork_commander_msgs/msg/Object')], name='WS01', type='10', pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='atwork_commander_msgs/msg/Workstation'), atwork_commander_msgsmsgWorkstation(objects=[], name='WS03', type='10', pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='atwork_commander_msgs/msg/Workstation')], arena_target_state=[atwork_commander_msgsmsgWorkstation(objects=[], name='WS01', type='10', pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='atwork_commander_msgs/msg/Workstation'), atwork_commander_msgsmsgWorkstation(objects=[atwork_commander_msgsmsgObject(object=12, target=0, decoy=False, pose=geometry_msgsmsgPoseStamped(header=std_msgsmsgHeader(seq=0, stamp=builtin_interfacesmsgTime(sec=0, nanosec=0, __msgtype='builtin_interfaces/msg/Time'), frame_id='', __msgtype='std_msgs/msg/Header'), pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype='atwork_commander_msgs/msg/Object'), atwork_commander_msgsmsgObject(object=15, target=0, decoy=False, pose=geometry_msgsmsgPoseStamped(header=std_msgsmsgHeader(seq=0, stamp=builtin_interfacesmsgTime(sec=0, nanosec=0, __msgtype='builtin_interfaces/msg/Time'), frame_id='', __msgtype='std_msgs/msg/Header'), pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype='atwork_commander_msgs/msg/Object'), atwork_commander_msgsmsgObject(object=16, target=0, decoy=False, pose=geometry_msgsmsgPoseStamped(header=std_msgsmsgHeader(seq=0, stamp=builtin_interfacesmsgTime(sec=0, nanosec=0, __msgtype='builtin_interfaces/msg/Time'), frame_id='', __msgtype='std_msgs/msg/Header'), pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype='atwork_commander_msgs/msg/Object')], name='WS03', type='10', pose=geometry_msgsmsgPose(position=geometry_msgsmsgPoint(x=0.0, y=0.0, z=0.0, __msgtype='geometry_msgs/msg/Point'), orientation=geometry_msgsmsgQuaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype='geometry_msgs/msg/Quaternion'), __msgtype='geometry_msgs/msg/Pose'), __msgtype='atwork_commander_msgs/msg/Workstation')], prep_time=builtin_interfacesmsgDuration(sec=180, nanosec=0, __msgtype='builtin_interfaces/msg/Duration'), exec_time=builtin_interfacesmsgDuration(sec=300, nanosec=0, __msgtype='builtin_interfaces/msg/Duration'), type='BMT', id=2194554, config='', commit=0, __msgtype_='atwork_commander_msgs/msg/Task')"

# input_string = "atwork_commander_msgs__msg__Task(header=std_msgs__msg__Header(seq=12, stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), execute_on=[], arena_start_state=[atwork_commander_msgs__msg__Workstation(objects=[atwork_commander_msgs__msg__Object(object=12, target=0, decoy=False, pose=geometry_msgs__msg__PoseStamped(header=std_msgs__msg__Header(seq=0, stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype__='atwork_commander_msgs/msg/Object'), atwork_commander_msgs__msg__Object(object=15, target=0, decoy=False, pose=geometry_msgs__msg__PoseStamped(header=std_msgs__msg__Header(seq=0, stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype__='atwork_commander_msgs/msg/Object'), atwork_commander_msgs__msg__Object(object=16, target=0, decoy=False, pose=geometry_msgs__msg__PoseStamped(header=std_msgs__msg__Header(seq=0, stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype__='atwork_commander_msgs/msg/Object')], name='WS01', type='10', pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='atwork_commander_msgs/msg/Workstation'), atwork_commander_msgs__msg__Workstation(objects=[], name='WS03', type='10', pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='atwork_commander_msgs/msg/Workstation')], arena_target_state=[atwork_commander_msgs__msg__Workstation(objects=[], name='WS01', type='10', pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='atwork_commander_msgs/msg/Workstation'), atwork_commander_msgs__msg__Workstation(objects=[atwork_commander_msgs__msg__Object(object=12, target=0, decoy=False, pose=geometry_msgs__msg__PoseStamped(header=std_msgs__msg__Header(seq=0, stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype__='atwork_commander_msgs/msg/Object'), atwork_commander_msgs__msg__Object(object=15, target=0, decoy=False, pose=geometry_msgs__msg__PoseStamped(header=std_msgs__msg__Header(seq=0, stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype__='atwork_commander_msgs/msg/Object'), atwork_commander_msgs__msg__Object(object=16, target=0, decoy=False, pose=geometry_msgs__msg__PoseStamped(header=std_msgs__msg__Header(seq=0, stamp=builtin_interfaces__msg__Time(sec=0, nanosec=0, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='geometry_msgs/msg/PoseStamped'), EMPTY=0, ATWORK_START=11, F20_20_B=11, F20_20_G=12, S40_40_B=13, S40_40_G=14, M20_100=15, M20=16, M30=17, R20=18, ATWORK_END=18, ADVANCED_START=20, Axis2=20, Bearing2=21, Housing=22, Motor2=23, Spacer=24, Screwdriver=25, Wrench=26, Drill=27, AllenKey=28, ADVANCED_END=28, ROCKIN_START=30, BEARING_BOX=31, BEARING=32, AXIS=33, DISTANCE_TUBE=34, MOTOR=35, ROCKIN_END=35, CONTAINER_START=40, CONTAINER_RED=40, CONTAINER_BLUE=41, CONTAINER_END=41, CAVITY_START=50, F20_20_H=50, F20_20_V=51, F20_20_F=52, S40_40_H=53, S40_40_V=54, S40_40_F=55, M20_H=56, M20_V=57, M20_F=58, M20_100_H=59, M20_100_V=60, M20_100_F=61, M30_H=62, M30_V=63, M30_F=64, R20_H=65, R20_V=66, R20_F=67, CAVITY_END=67, __msgtype__='atwork_commander_msgs/msg/Object')], name='WS03', type='10', pose=geometry_msgs__msg__Pose(position=geometry_msgs__msg__Point(x=0.0, y=0.0, z=0.0, __msgtype__='geometry_msgs/msg/Point'), orientation=geometry_msgs__msg__Quaternion(x=0.0, y=0.0, z=0.0, w=0.0, __msgtype__='geometry_msgs/msg/Quaternion'), __msgtype__='geometry_msgs/msg/Pose'), __msgtype__='atwork_commander_msgs/msg/Workstation')], prep_time=builtin_interfaces__msg__Duration(sec=180, nanosec=0, __msgtype__='builtin_interfaces/msg/Duration'), exec_time=builtin_interfaces__msg__Duration(sec=300, nanosec=0, __msgtype__='builtin_interfaces/msg/Duration'), type='BMT', id=2194554, config='', commit=0, __msgtype__='atwork_commander_msgs/msg/Task')"

# parser = RosbagParser(input_string)
# task_data_list = parser.parse_tasks()
# print(task_data_list)
# print("------------------------------")
# print(task_data_list[0]["arena_start_state"][0]["pose"]["position"])
# import ast
# objects_pose_string = " {'type': 'F20_20_G', 'pose': {'position': {'x': 22.0, 'y': 11.0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': 15.0, 'w': 30.0}}}/{'type': 'M20', 'pose': {'position': {'x': 0.0, 'y': 66.0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 77.0}}}"
# split_strings = objects_pose_string.split('/')

#         # Strip leading and trailing whitespace from each segment
# split_strings = [s.strip() for s in split_strings]

# # Convert each segment to a dictionary
# object_poses = [ast.literal_eval(obj_str) for obj_str in split_strings]

# locations = task_data_list[0]["arena_start_state"]

# for location in locations:
#     objects = location["objects"]
#     for obj in objects:
#         for obj_pose in object_poses:
#             if (obj["type"] == obj_pose["type"]):
#                 obj["pose"] = obj_pose["pose"]

# print(task_data_list)
# print(task_data_list[0]['arena_start_state'][0]['objects'][0]["type"])
# print(task_data_list[0]["arena_start_state"][0]["pose"]["position"]["x"])
# print(task_data_list[0]["arena_start_state"])
# print(len(task_data_list[0]["arena_start_state"]))
# current_location = task_data_list[0]["arena_start_state"][0]
# first_obj = current_location["objects"][0]
# print(current_location)
# current_location["pose"]["orientation"]["w"] = 88
# current_location["pose"]["position"]["y"] = 111
# print(current_location["pose"]["position"])
# print(current_location["pose"]["orientation"])
# x = current_location["pose"]["position"]["y"]
# print(x)
# print(first_obj)



# array_obj = []
# obj1 = task_data_list[0]["arena_start_state"][0]["objects"][0]
# obj2 = task_data_list[0]["arena_start_state"][0]["objects"][1]
# obj3 = task_data_list[0]["arena_start_state"][0]["objects"][2]
# if task_data_list[0]["arena_start_state"][1]["objects"]:
#     obj4 = task_data_list[0]["arena_start_state"][1]["objects"][0]
#     array_obj.append(obj4)
# array_obj.append(obj1)
# array_obj.append(obj2)
# array_obj.append(obj3)
# print(obj1)
# first_obj_id = array_obj.pop(0)["id"]
# print(first_obj_id)
# locations = task_data_list[0]["arena_target_state"]
# target_location = None
# for location in locations:
#     objects = location["objects"]
#     for obj in objects:
#         if obj["id"] == obj1["id"]:
#             target_location = location
#             break
#     if target_location:
#         break

# if target_location:
#     print(target_location["name"])
# else:
#     print("Target location not found.")


# ws_pose_dict = {
#             'WS01': {
#                 'pose': {
#                     'position': {'x': 77.0, 'y': 88.0, 'z': 99.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS02': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS03': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 33.0, 'y': 22.0, 'z': 44.0, 'w': 0.0}
#                 }
#             },
#             'WS04': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS05': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS06': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS07': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS08': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS09': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS10': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS11': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS12': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS13': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS14': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             },
#             'WS15': {
#                 'pose': {
#                     'position': {'x': 0.0, 'y': 0.0, 'z': 0.0},
#                     'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}
#                 }
#             }
#         }

# locations = task_data_list[0]["arena_start_state"]

# for location in locations:
#     location["pose"] = ws_pose_dict[location["name"]]

# print(task_data_list[0]["arena_start_state"][0]["name"])
# print(task_data_list[0]["arena_start_state"][0]["pose"])
# print(task_data_list[0]["arena_start_state"][1]["name"])
# print(task_data_list[0]["arena_start_state"][1]["pose"])