# Make sure to have the add-on "ZMQ remote API"
# running in CoppeliaSim
#
# All CoppeliaSim commands will run in blocking mode (block
# until a reply from CoppeliaSim is received). For a non-
# blocking example, see simpleTest-nonBlocking.py

# DOC : https://www.coppeliarobotics.com/helpFiles/en/apiFunctions.htm

import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import os

duration = 20
proxSensorName = '/BubbleRob/Proximity_sensor'
sceneFile = "BubbleRob.ttt"
leftMotorName = '/BubbleRob/leftMotor'
rightMotorName = '/BubbleRob/rightMotor'

client = RemoteAPIClient()
sim = client.getObject('sim')

# Load Scene from TTT File
sim.loadScene(os.path.join(os.getcwd(), sceneFile))

# Enable real-time simulation (Ajout de cette ligne)
sim.setBoolParam(sim.boolparam_realtime_simulation, True)

# When simulation is not running, ZMQ message handling could be a bit
# slow, since the idle loop runs at 8 Hz by default. So let's make
# sure that the idle loop runs at full speed for this program:
defaultIdleFps = sim.getInt32Param(sim.intparam_idle_fps)
sim.setInt32Param(sim.intparam_idle_fps, 0)

# Get Motors
left_motor = sim.getObject(leftMotorName)
right_motor = sim.getObject(rightMotorName)

# Get Proximity Sensor
proxSensor = sim.getObject(proxSensorName)
property = sim.getObjectProperty(proxSensor)

result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(proxSensor)
print(distance)

# Run a simulation in asynchronous mode:
clientID = sim.startSimulation()
while (t := sim.getSimulationTime()) < duration:
    result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(proxSensor)
    s = f'Simulation time: {t:.2f} [s] - {distance:.2f} (simulation running asynchronously to client, i.e. non-stepped)'
    print(s)
    sim.addLog(sim.verbosity_scriptinfos, s)

    if t <= 5:
        sim.setJointTargetVelocity(left_motor, 1)
        sim.setJointTargetVelocity(right_motor, 1)
    elif t <= 10:
        sim.setJointTargetVelocity(left_motor, 1)
        sim.setJointTargetVelocity(right_motor, 0)
    elif t <= 15:
        sim.setJointTargetVelocity(left_motor, 0)
        sim.setJointTargetVelocity(right_motor, 1)
    elif t <= 20:
        sim.setJointTargetVelocity(left_motor, 0)
        sim.setJointTargetVelocity(right_motor, 0)

sim.stopSimulation()
# Wait until the simulation is actually stopped
while sim.getSimulationState() != sim.simulation_stopped:
    time.sleep(0.1)

# Restore the original idle loop frequency:
sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps)

# Check if real-time simulation is enabled
realtime_simulation_enabled = sim.getBoolParam(sim.boolparam_realtime_simulation)
print("Real-time simulation enabled:", realtime_simulation_enabled)