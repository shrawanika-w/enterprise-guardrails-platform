from pathlib import Path
import yaml

BASE=Path(__file__).resolve().parent.parent/'policies'

def load_policy(version:str):
    path=BASE/version/'safety.yaml'
    if not path.exists():
        return {"error":"policy not found","version":version}
    return yaml.safe_load(path.read_text())
