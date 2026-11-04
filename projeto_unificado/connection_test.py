from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

estado = sim.getSimulationState()
print(f"Simulation state: {estado}")