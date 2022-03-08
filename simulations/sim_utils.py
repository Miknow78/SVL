import numpy as np


def get_velocity(agent_state):
    current_speed = np.linalg.norm([agent_state.velocity.x, agent_state.velocity.z]) * 3.6
    return current_speed


def get_location(agent_state):
    return agent_state.position


def get_dimension(agent):
    dimension = agent.bounding_box.size
    height = dimension.y
    width = dimension.x
    length = dimension.z
    return dimension


def get_weather(sim):
    rain = sim.weather.rain  # % x100
    fog = sim.weather.fog
    time_of_day = sim.time_of_day  # day > 12


