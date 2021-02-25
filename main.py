import entities
import simulation

data = entities.read_inputs()
simulation.simulate(data)
entities.write_schedule(data)