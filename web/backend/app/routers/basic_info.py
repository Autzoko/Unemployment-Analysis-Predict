from fastapi import APIRouter
from app.services.basic_info_service import load_state_mapping

router = APIRouter()

state_mappings = load_state_mapping()

def generate_state_code_mapping():
    code_to_name = []
    for full_code, state_name in state_mappings.items():
        code_to_name.append({
            "state_name": state_name,
            "full_code": full_code
        })

    return code_to_name

@router.get("/basic_info")
def get_basic_info():
    return generate_state_code_mapping