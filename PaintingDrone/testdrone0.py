
import time
import os
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

#points vers la droite
class Drone:
    def __init__(self, path, sim, initial_position, target_points):
        self.path = path  
        self.sim = sim   
        self.handle = sim.getObject(path)  
        self.sensor = sim.getObject(path + "/Proximity_sensor")  
        self.initial_position = initial_position  
        self.set_position(initial_position)  
        self.target_points = target_points  
        self.current_target_index = 0  

    def get_position(self):
        return self.sim.getObjectPosition(self.handle, -1)  

    def set_position(self, position):
        self.sim.setObjectPosition(self.handle, -1, position) 

    def move_vertical(self, distance):
        current_position = self.get_position()
        new_position = [current_position[0], current_position[1] + distance, current_position[2]]
        self.set_position(new_position) 

    def move_horizontal(self, distance):
        current_position = self.get_position()
        new_position = [current_position[0] + distance, current_position[1], current_position[2]]
        self.set_position(new_position)

    def check_collision_with_wall(self):
        result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = self.sim.readProximitySensor(self.sensor)
        if result == 1:
            s = f'{self.path} [s] - {distance:.2f}'
            print(s)
        return result

    def move_to_next_target(self):
        if self.current_target_index >= len(self.target_points):
            print("Tous les points cibles ont été atteints.")
            return
        
        target_position = self.target_points[self.current_target_index]
        self.move_to_position(target_position)
        self.current_target_index += 1  

    def move_to_position(self, position):
        current_position = self.get_position()
        backward_position = [current_position[0], current_position[1], current_position[2] - 0.1]  
        self.set_position(backward_position)  
        time.sleep(1)
        self.set_position(position)  
        time.sleep(1)

def move_drone_towards_wall(drone):
    move = 0.05
    if not drone.check_collision_with_wall():
        drone.move_vertical(move)  
    else:
        drone.move_horizontal(0.05)  
        time.sleep(1)

client = RemoteAPIClient()  
sim = client.getObject('sim') 
sceneFile = "drone 1.ttt"
sim.loadScene(os.path.join(os.getcwd(), sceneFile)) 

initial_position1 = [-1.0, 1.0, 1.0]
initial_position2 = [-1.0, 1.0, 1.1]

target_points_drone1 = [
]

target_points_drone2 = [
]

drone1 = Drone("/Quadcopter", sim, initial_position1, target_points_drone1)
drone2 = Drone("/Quadcopter1", sim, initial_position2, target_points_drone2)

duration_to_wall = 3  

sim.setStepping(True)
clientID = sim.startSimulation()  

while sim.getSimulationTime() < duration_to_wall:
    move_drone_towards_wall(drone1)
    move_drone_towards_wall(drone2)
    time.sleep(0.2)  
    print(sim.getSimulationTime())  
    sim.step()  

sim.stopSimulation()

while sim.getSimulationState() != sim.simulation_stopped:
    time.sleep(0.1)