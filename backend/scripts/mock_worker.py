"""Mock worker script: only demonstrates API workflow calls."""
import random
import time

import requests

BASE_URL = "http://127.0.0.1:8000"
WORKER_TOKEN = "replace_with_worker_token"
WORKER_ID = "mock-worker-01"
HEADERS = {"X-API-Key": WORKER_TOKEN}


def post(path: str, payload: dict):
    resp = requests.post(f"{BASE_URL}{path}", json=payload, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


def run_once():
    post("/api/worker/heartbeat", {"worker_id": WORKER_ID, "worker_name": "Mock Worker", "concurrency_limit": 1})
    claim = post("/api/worker/claim", {"worker_id": WORKER_ID})
    task = claim.get("data")
    if not task:
        print("No queued task")
        return
    task_id = task["id"]
    post(f"/api/tasks/{task_id}/start", {"worker_id": WORKER_ID})
    time.sleep(1)
    if random.random() > 0.2:
        result = post(
            f"/api/tasks/{task_id}/success",
            {
                "worker_id": WORKER_ID,
                "kugou_id": f"kg-{task_id}",
                "recharge_cost": "8.80",
                "validity_value": 30,
                "validity_unit": "day",
                "app_month_price": "10.00",
                "app_season_price": "27.00",
                "app_year_price": "90.00",
                "web_month_price": "10.00",
                "web_season_price": "27.00",
                "web_year_price": "90.00",
                "pc_month_price": "10.00",
                "pc_season_price": "27.00",
                "pc_year_price": "90.00",
            },
        )
    else:
        result = post(
            f"/api/tasks/{task_id}/fail",
            {"worker_id": WORKER_ID, "fail_code": "ERR_DEMO", "fail_reason": "mock random failure"},
        )
    print(result)


if __name__ == "__main__":
    run_once()
