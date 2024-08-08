from collections import deque

# class TaskGenerator:
#     def __init__(self, start_state, target_state):
#         self.start_state = start_state
#         self.target_state = target_state
#         self.object_locations = self._map_object_locations()
#         self.task_array = [deque(), deque()]  # [pick_tasks, place_tasks]
#         self.picked_objects = set()
#         self._generate_tasks()

#     def _map_object_locations(self):
#         object_locations = {}
#         for ws, objects in self.start_state.items():
#             for obj in objects:
#                 object_locations[obj['object']] = ws
#         return object_locations

#     def _generate_tasks(self):
#         current_location = None

#         for target_ws, target_objects in self.target_state.items():
#             pick_obj_queue = deque()
#             place_obj_queue = deque()
#             for obj in target_objects:
#                 obj_id = obj['object']
#                 obj_type = obj['object_type']
#                 current_ws = self.object_locations.get(obj_id)
                
#                 if current_ws == target_ws:
#                     continue
                
#                 if obj_id not in self.picked_objects:
#                     pick_obj_queue.append({
#                         'object_id': obj_id,
#                         'object_type': obj_type
#                     })
#                     self.picked_objects.add(obj_id)
                
#                 if obj_id in self.picked_objects:
#                     place_obj_queue.append({
#                         'object_id': obj_id,
#                         'object_type': obj_type
#                     })

#             if pick_obj_queue:
#                 self.task_array[0].append({target_ws: pick_obj_queue})
#             if place_obj_queue:
#                 self.task_array[1].append({target_ws: place_obj_queue})

#     def get_next_pick_task(self):
#         if self.task_array[0]:
#             workstation_task = self.task_array[0][0]
#             workstation, objects = next(iter(workstation_task.items()))
#             if objects:
#                 obj_info = objects.popleft()
#                 if not objects:
#                     self.task_array[0].popleft()
#                 return workstation, obj_info
#         return None, None

#     def get_next_place_task(self):
#         if self.task_array[1]:
#             workstation_task = self.task_array[1][0]
#             workstation, objects = next(iter(workstation_task.items()))
#             if objects:
#                 obj_info = objects.popleft()
#                 if not objects:
#                     self.task_array[1].popleft()
#                 return workstation, obj_info
#         return None, None

# # Example usage
# start_state = {
#     'WS03': [{'object': 17, 'target': 0, 'object_type': 'M30'}, {'object': 14, 'target': 0, 'object_type': 'S40_40_G'}, {'object': 24, 'target': 0, 'object_type': 'DISTANCE_TUBE'}, {'object': 11, 'target': 0, 'object_type': 'F20_20_B'}, {'object': 22, 'target': 0, 'object_type': 'BEARING'}],
#     'WS01': []
# }

# target_state = {
#     'WS03': [],
#     'WS01': [{'object': 17, 'target': 0, 'object_type': 'M30'}, {'object': 14, 'target': 0, 'object_type': 'S40_40_G'}, {'object': 24, 'target': 0, 'object_type': 'DISTANCE_TUBE'}, {'object': 11, 'target': 0, 'object_type': 'F20_20_B'}, {'object': 22, 'target': 0, 'object_type': 'BEARING'}]
# }

# task_generator = TaskGenerator(start_state, target_state)
# tasks = []

# while True:
#     workstation, obj_info = task_generator.get_next_pick_task()
#     if workstation is None:
#         break
#     tasks.append(f"Move to {workstation} and pick {obj_info}")

# while True:
#     workstation, obj_info = task_generator.get_next_place_task()
#     if workstation is None:
#         break
#     tasks.append(f"Move to {workstation} and place {obj_info}")

# for task in tasks:
#     print(task)













# class TaskGenerator:
#     def __init__(self, start_state, target_state):
#         """
#         Initialize TaskGenerator with start_state and target_state.
        
#         Args:
#         - start_state (dict): Initial state of workstations and objects.
#         - target_state (dict): Target state where objects need to be placed.
#         """
#         self.start_state = start_state
#         self.target_state = target_state
#         self.object_locations = self._map_object_locations()  # Map object locations
#         self.picked_objects = set()  # Track picked objects

#     def _map_object_locations(self):
#         """
#         Map object IDs to their current workstation locations based on start_state.
        
#         Returns:
#         - object_locations (dict): Dictionary mapping object IDs to workstation IDs.
#         """
#         object_locations = {}
#         for ws, objects in self.start_state.items():
#             for obj in objects:
#                 object_locations[obj['object']] = ws
#         return object_locations

#     def _generate_move_commands(self, from_ws, to_ws):
#         """
#         Generate move commands to move from one workstation to another.
        
#         Args:
#         - from_ws (str): Current workstation ID.
#         - to_ws (str): Target workstation ID.
        
#         Returns:
#         - commands (list): List of move commands (strings).
#         """
#         if from_ws != to_ws:
#             return [f"move_to_{to_ws}"]
#         return []

#     def generate_tasks(self):
#         """
#         Generate tasks to move objects from start_state to target_state.
        
#         Returns:
#         - tasks (list): List of tasks (strings) representing actions to be performed.
#         """
#         tasks = []
#         current_location = None

#         for target_ws, target_objects in self.target_state.items():
#             for obj in target_objects:
#                 obj_id = obj['object']
#                 current_ws = self.object_locations.get(obj_id)
                
#                 # Skip objects that are already at their target workstation
#                 if current_ws == target_ws:
#                     continue
                
#                 # Move to current workstation if not already there
#                 if current_ws and current_ws != target_ws:
#                     tasks.extend(self._generate_move_commands(current_location, current_ws))
#                     current_location = current_ws
                
#                 # Pick object if it hasn't been picked yet
#                 if obj_id not in self.picked_objects:
#                     tasks.append(f"pick_object_{obj_id}")
#                     self.picked_objects.add(obj_id)
                
#                 # Check if we need to place objects
#                 if len(self.picked_objects) == 3:
#                     tasks.extend(self._generate_move_commands(current_location, target_ws))
#                     current_location = target_ws
                    
#                     for placed_obj_id in self.picked_objects.copy():
#                         if placed_obj_id in [o['object'] for o in target_objects]:
#                             tasks.append(f"place_object_{placed_obj_id}")
#                             self.picked_objects.remove(placed_obj_id)
                    
#                     if current_location != target_ws:
#                         tasks.extend(self._generate_move_commands(target_ws, current_location))
        
#         # Place remaining picked objects
#         if self.picked_objects:
#             tasks.extend(self._generate_move_commands(current_location, target_ws))
#             current_location = target_ws
            
#             for placed_obj_id in self.picked_objects.copy():
#                 if placed_obj_id in [o['object'] for o in target_objects]:
#                     tasks.append(f"place_object_{placed_obj_id}")
#                     self.picked_objects.remove(placed_obj_id)
            
#             if current_location != target_ws:
#                 tasks.extend(self._generate_move_commands(target_ws, current_location))

#         # Move back to initial location (if needed)
#         if current_location is not None and current_location != 'WS01':
#             tasks.extend(self._generate_move_commands(current_location, 'WS01'))

#         return tasks

# # Example usage
# start_state = {
#     'WS03': [{'object': 17, 'target': 0}, {'object': 14, 'target': 0}],
#     'WS02': [{'object': 24, 'target': 0}, {'object': 11, 'target': 0}],
#     'WS01': [{'object': 22, 'target': 0}]
# }

# target_state = {
#     'WS03': [],
#     'WS02': [],
#     'WS01': [{'object': 17, 'target': 0}, {'object': 14, 'target': 0}, {'object': 24, 'target': 0}, {'object': 11, 'target': 0}, {'object': 22, 'target': 0}]
# }

# task_generator = TaskGenerator(start_state, target_state)
# tasks = task_generator.generate_tasks()
# for task in tasks:
#     print(task)



class TaskGenerator:
    def __init__(self, start_state, target_state):
        """
        Initialize TaskGenerator with start_state and target_state.
        
        Args:
        - start_state (dict): Initial state of workstations and objects.
        - target_state (dict): Target state where objects need to be placed.
        """
        self.start_state = start_state
        self.target_state = target_state
        self.object_locations = self._map_object_locations()  # Map object locations
        self.picked_objects = set()  # Track picked objects

    def _map_object_locations(self):
        """
        Map object IDs to their current workstation locations based on start_state.
        
        Returns:
        - object_locations (dict): Dictionary mapping object IDs to workstation IDs.
        """
        object_locations = {}
        for ws, objects in self.start_state.items():
            for obj in objects:
                object_locations[obj['object']] = ws
        return object_locations

    def _generate_move_commands(self, from_ws, to_ws):
        """
        Generate move commands to move from one workstation to another.
        
        Args:
        - from_ws (str): Current workstation ID.
        - to_ws (str): Target workstation ID.
        
        Returns:
        - commands (list): List of move commands (strings).
        """
        if from_ws != to_ws:
            return [f"move_to_{to_ws}"]
        return []

    def generate_tasks(self):
        """
        Generate tasks to move objects from start_state to target_state.
        
        Returns:
        - tasks (list): List of tasks (strings) representing actions to be performed.
        """
        tasks = []
        current_location = None

        for target_ws, target_objects in self.target_state.items():
            for obj in target_objects:
                obj_id = obj['object']
                current_ws = self.object_locations.get(obj_id)
                
                # Skip objects that are already at their target workstation
                if current_ws == target_ws:
                    continue
                
                # Move to current workstation if not already there
                if current_ws and current_ws != target_ws:
                    tasks.extend(self._generate_move_commands(current_location, current_ws))
                    current_location = current_ws
                
                # Pick object if it hasn't been picked yet
                if obj_id not in self.picked_objects:
                    tasks.append(f"pick_object_{obj_id}")
                    self.picked_objects.add(obj_id)
                
                # Check if we need to place objects
                if len(self.picked_objects) == 3:
                    tasks.extend(self._generate_move_commands(current_location, target_ws))
                    current_location = target_ws
                    
                    for placed_obj_id in self.picked_objects.copy():
                        if placed_obj_id in [o['object'] for o in target_objects]:
                            tasks.append(f"place_object_{placed_obj_id}")
                            self.picked_objects.remove(placed_obj_id)
                    
                    if current_location != target_ws:
                        tasks.extend(self._generate_move_commands(target_ws, current_location))
        
        # Place remaining picked objects
        if self.picked_objects:
            tasks.extend(self._generate_move_commands(current_location, target_ws))
            current_location = target_ws
            
            for placed_obj_id in self.picked_objects.copy():
                if placed_obj_id in [o['object'] for o in target_objects]:
                    tasks.append(f"place_object_{placed_obj_id}")
                    self.picked_objects.remove(placed_obj_id)
            
            if current_location != target_ws:
                tasks.extend(self._generate_move_commands(target_ws, current_location))

        # Move back to initial location (if needed)
        if current_location is not None and current_location != 'WS01':
            tasks.extend(self._generate_move_commands(current_location, 'WS01'))

        return tasks

# Example usage
start_state = {
    'WS03': [{'object': 17, 'target': 0}, {'object': 14, 'target': 0}],
    'WS02': [{'object': 24, 'target': 0}, {'object': 11, 'target': 0}],
    'WS01': [{'object': 22, 'target': 0}]
}

target_state = {
    'WS03': [],
    'WS02': [],
    'WS01': [{'object': 17, 'target': 0}, {'object': 14, 'target': 0}, {'object': 24, 'target': 0}, {'object': 11, 'target': 0}, {'object': 22, 'target': 0}]
}

task_generator = TaskGenerator(start_state, target_state)
tasks = task_generator.generate_tasks()
for task in tasks:
    print(task)