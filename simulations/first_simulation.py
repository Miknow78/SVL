#!/usr/bin/env python3
#
# Copyright (c) 2019-2021 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#
import time

from environs import Env
import lgsvl
from lgsvl import Vector

print("Python API Quickstart #5: Ego vehicle driving in circle")
env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host),
                      env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))
if sim.current_scene == "45dd30b0-4be1-4eb7-820a-3e175b0117fc":     # ModernCity map
    sim.reset()
else:
    sim.load("45dd30b0-4be1-4eb7-820a-3e175b0117fc")

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
forward = lgsvl.utils.transform_to_forward(spawns[0])
state.transform.position += 5 * forward  # 5m forwards
npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

state2 = lgsvl.AgentState()
state2.transform = spawns[0]
forward = lgsvl.utils.transform_to_forward(spawns[0])
state2.transform.position -= 5 * forward
ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5),
                    lgsvl.AgentType.EGO, state2)

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

input("Press Enter to start driving for 30 seconds")


def on_lane_change(agent):
    print(f'{agent} changed lanes motherquakers')


for controllable in sim.get_controllables():
    if controllable.type == "signal":
        controllable.control("green=1;loop")


# VehicleControl objects can only be applied to EGO vehicles
# You can set the steering (-1 ... 1), throttle and braking (0 ... 1), handbrake and reverse (bool)
npc.follow_closest_lane(True, 120)

npc.on_lane_change(on_lane_change)
print(npc.state.speed)
sim.run(2)
npc.change_lane(False)
print(npc.state.speed)
sim.run(1)
npc.change_lane(True)
print(npc.state.speed)
sim.run(2)
print(npc.state.speed)
