import os
import lgsvl
import copy
from environs import Env

env = Env()
sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host),
                      env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))

# BorregasAve default map must be added to your personal library
if sim.current_scene == "bd77ac3b-fbc3-41c3-a806-25915c777022":  # Highway map
    sim.reset()
else:
    sim.load("bd77ac3b-fbc3-41c3-a806-25915c777022")

spawns = sim.get_spawn()
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# EGO
state = lgsvl.AgentState()
state.transform = spawns[0]
ego_state = copy.deepcopy(state)
ego_state.transform.position += 50 * forward
ego_state.transform.position -= 3 * right

# The Lincoln2017MKZ default vehicle must be added to your vehicle library
a = sim.add_agent(os.environ.get("LGSVL__VEHICLE_0"), lgsvl.AgentType.EGO, ego_state)

# NPC
npc_state = copy.deepcopy(state)
npc_state.transform.position += 10 * forward
npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npc_state)

vehicles = {
  a: "EGO",
  npc: "Sedan",
}

# This block creates the list of waypoints that the NPC will follow
# Each waypoint is an position vector paired with the speed that the NPC will drive to it
waypoints = []
x_max = 2
z_delta = 12

layer_mask = 0
layer_mask |= 1 << 0 # 0 is the layer for the road (default)

for i in range(20):
  speed = 24# if i % 2 == 0 else 12
  px = 0
  pz = (i + 1) * z_delta
  # Waypoint angles are input as Euler angles (roll, pitch, yaw)
  angle = spawns[0].rotation
  # Raycast the points onto the ground because BorregasAve is not flat
  hit = sim.raycast(spawns[0].position + pz * forward, lgsvl.Vector(0,-1,0), layer_mask)

  # NPC will wait for 1 second at each waypoint
  wp = lgsvl.DriveWaypoint(hit.point, speed, angle, 1)
  waypoints.append(wp)

# The NPC needs to be given the list of waypoints.
# A bool can be passed as the 2nd argument that controls whether or not the NPC loops over the waypoints (default false)
npc.follow(waypoints)

sim.run(20)