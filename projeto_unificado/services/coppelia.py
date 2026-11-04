from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math

client = RemoteAPIClient()
sim = client.require('sim')

def simulationStart():
    try:
        sim.startSimulation()
        return {"status": "Simulation successfully started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def simulationStop():    
    try:
        sim.stopSimulation()
        return {"status": "Simulation successfully stopped"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def simulationPause():
    try:
        if sim.getSimulationState() == 0:
            return {"status": "Simulation is not currently running"}

        sim.pauseSimulation()
        return {"status": "Simulation paused"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def simulationEstado():
    try:
        simulationState = sim.getSimulationState()
        states = {
            0: "stopped",
            17: "running",
            8: "paused"
        }
        return {"Simulation state": {
            "handle": simulationState,
            "name": states.get(simulationState, "unknown")
        }}
    except Exception as e:
        return {"status": "error", "message": str(e)}

#------------------------------------------------------------------------------------------------------

def objectHandle(object_name):
        return sim.getObject('/' + object_name)

def getObjectList():
    try:
        all_handles = sim.getObjectsInTree(sim.handle_scene, sim.handle_all) or []
        objects_filtered = []
        allowed_names = ["UR5", "Cuboid", "proximitySensor"]
        for h in all_handles:
            parent = sim.getObjectParent(h)
            if parent == -1:
                name = sim.getObjectAlias(h, 1)
                clean_name = name.lstrip('/')
                if any(clean_name.startswith(allowed) for allowed in allowed_names):
                    objects_filtered.append({
                        "handle": h,
                        "name": clean_name
                    })
        return {"objects": objects_filtered}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def getObjectPosition(object_name):
    try:
        handle = objectHandle(object_name)
        position = sim.getObjectPosition(handle, -1)
        position_appre = [round(v, 5) for v in position]
        return {"position": position_appre}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def setObjectPosition(object_name, x, y, z):
    try:
        handle = objectHandle(object_name)
        sim.setObjectPosition(handle, -1, [x, y, z])
        return {"message": f"Position of {object_name} set to: {[x, y, z]}(x, y, z)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def getObjectOrientation(object_name):
    try:
        handle = objectHandle(object_name)
        orientation = sim.getObjectOrientation(handle, -1)
        orientation_appre = [round(math.degrees(v), 4) for v in orientation]
        return {"orientation": orientation_appre}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def setObjectOrientation(object_name, a, b, g):
    try:
        handle = objectHandle(object_name)
        orientation_rad = [math.radians(a), math.radians(b), math.radians(g)]
        sim.setObjectOrientation(handle, -1, orientation_rad)
        return {"message": f"Orientation of {object_name} set to: {[a, b, g]}(α, β, γ)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
