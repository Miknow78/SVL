from environs import Env
import lgsvl
from lgsvl import Vector

env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host),
                      env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))


def main():
    print("--- START OF SIMULATION --- ")
    if sim.current_scene == "bd77ac3b-fbc3-41c3-a806-25915c777022":  # Highway map
        sim.reset()
    else:
        sim.load("bd77ac3b-fbc3-41c3-a806-25915c777022")

    try:
        state_ego = lgsvl.AgentState()
        state_ego.transform.position = lgsvl.Vector(-385, 35, 105)
        state_ego.transform.rotation.y = -90

        state_npc = lgsvl.AgentState()
        state_npc.transform.position = lgsvl.Vector(-390, 35, 105)
        state_npc.transform.rotation.y = -90

        npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state_npc)
        ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5),
                            lgsvl.AgentType.EGO, state_ego)

        print("Current time = ", sim.current_time)
        print("Current frame = ", sim.current_frame)

        input("Press Enter to start driving")

        def on_lane_change(agent):
            print(f'{agent} changed lane')


        # turn all of traffic lights green
        for controllable in sim.get_controllables():
            if controllable.type == "signal":
                controllable.control("green=1;loop")


        # VehicleControl objects can only be applied to EGO vehicles
        # You can set the steering (-1 ... 1), throttle and braking (0 ... 1), handbrake and reverse (bool)
        npc.follow_closest_lane(True, 10)
        npc.on_lane_change(on_lane_change)

        # Change Weather
        sim.weather = lgsvl.WeatherState(rain=0.8, fog=0, wetness=0, cloudiness=0, damage=0)


        for sim.current_frame in range (0, 1000):
            sim.run()
            print(npc.state.position)


    finally:
        print("END SIMULATION")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')

