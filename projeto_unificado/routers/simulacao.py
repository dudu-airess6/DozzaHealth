from fastapi import APIRouter
from services import coppelia

router = APIRouter()

@router.post("/simulation/start")
def start_simulation():
    return coppelia.simulationStart()

@router.post("/simulation/stop")
def stop_simulation():
    return coppelia.simulationStop()

@router.post("/simulation/pause")
def pause_simulation():
    return coppelia.simulationPause()

@router.get("/simulation/state")
def get_simulation_state():
    return coppelia.simulationEstado()
