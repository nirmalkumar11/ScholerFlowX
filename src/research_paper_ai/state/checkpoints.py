import json
from dataclasses import asdict


class CheckpointManager:

    @staticmethod
    def save(state, filepath):
        with open(filepath, "w") as f:
            json.dump(asdict(state), f, indent=2)

    @staticmethod
    def load(filepath):
        with open(filepath, "r") as f:
            return json.load(f)