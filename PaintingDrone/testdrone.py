import time
import os
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

class Drone:
    def __init__(self, path, sim, initial_position):
        self.path = path  
        self.sim = sim   
        self.handle = sim.getObject(path)  
        self.sensor = sim.getObject(path + "/Proximity_sensor")  
        self.initial_position = initial_position  
        self.set_position(initial_position)  

    def get_position(self):
        return self.sim.getObjectPosition(self.handle, -1)  

    def set_position(self, position):
        self.sim.setObjectPosition(self.handle, -1, position) 

    def move_vertical(self, distance):
        current_position = self.get_position()
        new_position = [current_position[0], current_position[1], current_position[2] + distance]
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

def move_drone(drone, move_horizontal_duration, move_vertical_duration):
    start_time = sim.getSimulationTime()
    while sim.getSimulationTime() - start_time < move_horizontal_duration:
        move = 0.05
        if not drone.check_collision_with_wall():
            drone.move_horizontal(move)
        else:
            drone.move_vertical(move)
        time.sleep(0.2)
        sim.step()
        
    start_time = sim.getSimulationTime()
    while sim.getSimulationTime() - start_time < move_vertical_duration:
        move = 0.05
        if not drone.check_collision_with_wall():
            drone.move_vertical(move)
        else:
            drone.move_horizontal(move)
        time.sleep(0.2)
        sim.step()

    start_time = sim.getSimulationTime()
    while sim.getSimulationTime() - start_time < move_horizontal_duration:
        move = -0.05
        if not drone.check_collision_with_wall():
            drone.move_horizontal(move)
        else:
            drone.move_vertical(move)
        time.sleep(0.2)
        sim.step()

    start_time = sim.getSimulationTime()
    while sim.getSimulationTime() - start_time < move_vertical_duration:
        move = -0.05
        if not drone.check_collision_with_wall():
            drone.move_vertical(move)
        else:
            drone.move_horizontal(move)
        time.sleep(0.2)
        sim.step()
client = RemoteAPIClient()  
sim = client.getObject('sim') 
sceneFile = "drone 1.ttt"
sim.loadScene(os.path.join(os.getcwd(), sceneFile)) 

initial_position1 = [-1.0, 1.0, 1.0]
initial_position2 = [-1.0, 1.0, 1.1]

drone1 = Drone("/Quadcopter", sim, initial_position1)
drone2 = Drone("/Quadcopter1", sim, initial_position2)

move_horizontal_duration = 1
move_vertical_duration = 1
  

sim.setStepping(True)
clientID = sim.startSimulation()  

move_drone(drone1, move_horizontal_duration, move_vertical_duration)
move_drone(drone2, move_horizontal_duration, move_vertical_duration)

sim.stopSimulation()

while sim.getSimulationState() != sim.simulation_stopped:
    time.sleep(0.1)
