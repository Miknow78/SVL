from environs import Env
import lgsvl
import numpy as np
from sim_utils import *

from lgsvl import Vector, Simulator

print("-- START SIMULATION -- ")
env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host),
                      env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))

if sim.current_scene == "bd77ac3b-fbc3-41c3-a806-25915c777022":  # Highway map
    sim.reset()
else:
    sim.load("bd77ac3b-fbc3-41c3-a806-25915c777022")

state_ego = lgsvl.AgentState()
state_ego.transform.position = lgsvl.Vector(-385, 35, 105)
state_ego.transform.rotation.y = -90

state_npc = lgsvl.AgentState()
state_npc.transform.position = lgsvl.Vector(-390, 35, 105)
state_npc.transform.rotation.y = -90

npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state_npc)
ego = sim.add_agent(name="ebe26b91-3930-4753-bfa4-c1fec3f2877e", agent_type=lgsvl.AgentType.EGO, state=state_ego)

# add random traffic
sim.add_random_agents(lgsvl.AgentType.NPC)

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to start driving")


print(npc.state)

vehicles = {
    ego: "EGO",
    npc: "Sedan",
}

sensors = ego.get_sensors()
for s in sensors:
    print(s.name)


def on_lane_change(agent):
    print(f'{agent} changed lane')


def on_collision(agent1, agent2, contact):
    name1 = vehicles[agent1]
    name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
    print("{} collided with {} at {}".format(name1, name2, contact))


# def onCustom(agent, kind, context):
#     print(context, kind, agent)


# turn all of traffic lights green
for controllable in sim.get_controllables():
    if controllable.type == "signal":
        controllable.control("green=1;loop")


# VehicleControl objects can only be applied to EGO vehicles
# You can set the steering (-1 ... 1), throttle and braking (0 ... 1), handbrake and reverse (bool)
npc.follow_closest_lane(True, 10)
npc.on_lane_change(on_lane_change)
npc.on_collision(on_collision)

# Change Weather
sim.weather = lgsvl.WeatherState(rain=0.8, fog=0, wetness=0, cloudiness=0, damage=0)
sim.set_time_of_day(19, fixed=True)

npc_dimension = get_dimension(npc)
ego_dimension = get_dimension(ego)

get_weather(sim)

while True:
    sim.run(0.1)
    ego_speed = get_velocity(ego.state)
    ego_location = get_location(ego.state)

    print("Current speed: {:.1f} [km/h]".format(ego_speed))

    if sim.current_frame == 400:
        npc.change_lane(True)
    if sim.current_frame == 500:
        npc.change_lane(False)

    if sim.current_time >= 30:
        sim.stop()
        break

# print(str(npc.state.speed * 3600 / 1000))
# print(ego.state.position)
