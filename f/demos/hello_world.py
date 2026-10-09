from datetime import datetime, timezone


def main(name: str = "Windmill"):
    return {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "success",
    }
