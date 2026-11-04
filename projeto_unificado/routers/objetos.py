from fastapi import APIRouter
from services import coppelia

router = APIRouter()

@router.get("/objects/list")
def list_objects():
    return coppelia.getObjectList()

@router.get("/objects/{object_name}/position")
def get_position(object_name: str):
    return coppelia.getObjectPosition(object_name)

@router.post("/objects/{object_name}/position")
def set_position(object_name: str, x: float, y: float, z: float):
    return coppelia.setObjectPosition(object_name, x, y, z)

@router.get("/objects/{object_name}/orientation")
def get_orientation(object_name: str):
    return coppelia.getObjectOrientation(object_name)

@router.post("/objects/{object_name}/orientation")
def set_orientation(object_name: str, a: float, b: float, g: float):
    return coppelia.setObjectOrientation(object_name, a, b, g)