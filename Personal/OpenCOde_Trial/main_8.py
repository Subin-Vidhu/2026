# -*- coding: utf-8 -*-
import os
import time
import asyncio
import aiofiles   # pip install aiofiles
import httpx
import uvicorn
import threading
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

MY_APP_PORT = 8520
ORTHANC_BASE = "http://localhost:8041"
ORTHANC_AUTH = ("admin", "password")
# SOURCE_PATH = r"F:"
# SOURCE_PATH = r"E:\A"
# SOURCE_PATH = r"E:\87d91272-5d3818d5-3245e9f1-cb76136e-b8630852\IMAGES"
# SOURCE_PATH = r"C:\Users\Subin-PC\Downloads\DIcom_test_data\RADON_TEST_DATA\cd_test_data"
SOURCE_PATH = r"C:\Users\Subin-PC\Downloads\DIcom_test_data\RADON_TEST_DATA\Anonymized - 12608\Anonymized - 12608\Ct Lower Limb Angio"
# SOURCE_PATH = r"C:\Users\Subin-PC\Downloads\DIcom_test_data\RADON_TEST_DATA\12139 INDULAL"
# CHANGE 1: Raise this dramatically — Orthanc is local, no network RTT
# 8 was conservative for a real network. For localhost, 32–64 is safe.
MAX_CONCURRENT_UPLOADS = 48
semaphore = asyncio.Semaphore(MAX_CONCURRENT_UPLOADS)

progress_counter = 0
IGNORED_EXTS = ('.exe', '.inf', '.htm', '.html', '.jar', '.txt', '.xml', '.bmp', '.png', '.ico')

def get_ts():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

async def upload_single_file(client, file_path, total_files):
    global progress_counter

    if file_path.lower().endswith(IGNORED_EXTS):
        return {"outcome": "ignored", "id": None}

    async with semaphore:
        try:
            # CHANGE 2: Use aiofiles for non-blocking reads.
            # Previously, open() was synchronous — it blocked the entire event loop
            # while the CD drive spun up. With aiofiles, the loop stays free to
            # fire off other uploads while one file is being read from disk.
            async with aiofiles.open(file_path, "rb") as f:
                content = await f.read()
            
            if not content:
                return {"outcome": "empty", "id": None}

            response = await client.post(
                f"{ORTHANC_BASE}/instances",
                content=content,
                timeout=60.0
            )

            progress_counter += 1
            if progress_counter % 100 == 0 or progress_counter == total_files:
                percent = (progress_counter / total_files) * 100
                print(f"[{get_ts()}] [PROGRESS] {progress_counter}/{total_files} ({percent:.1f}%)")

            if response.status_code == 200:
                payload = response.json()
                status = payload.get("Status", "")
                if status == "Success":
                    return {"outcome": "stored", "id": payload.get("ID")}
                if status == "AlreadyStored":
                    return {"outcome": "already_stored", "id": payload.get("ID")}
                return {"outcome": "ok_unknown", "id": payload.get("ID")}

            return {"outcome": "failed_http", "id": None}

        except Exception:
            return {"outcome": "failed_exception", "id": None}


@app.post("/fast-import")
async def fast_import():
    global progress_counter
    progress_counter = 0
    t_start = time.monotonic()

    print(f"[{get_ts()}] [SERVER] Scanning {SOURCE_PATH}...")
    files_to_process = [
        os.path.join(root, f)
        for root, _, filenames in os.walk(SOURCE_PATH)
        for f in filenames
    ]
    total_files = len(files_to_process)
    print(f"[{get_ts()}] [SERVER] Found {total_files} files. Starting import...")

    # CHANGE 3: Enable HTTP/2. This lets httpx multiplex all requests over a
    # single connection instead of opening 48 separate TCP connections to
    # Orthanc. Drastically reduces connection-setup overhead.
    # Requires: pip install httpx[http2]  (installs h2 library)
    async with httpx.AsyncClient(
        auth=ORTHANC_AUTH,
        timeout=None,
        http2=True,                          # <-- HTTP/2 multiplexing
        limits=httpx.Limits(
            max_connections=MAX_CONCURRENT_UPLOADS,
            max_keepalive_connections=MAX_CONCURRENT_UPLOADS,
        )
    ) as client:
        tasks = [upload_single_file(client, f, total_files) for f in files_to_process]
        results = await asyncio.gather(*tasks)

    stored_count = sum(1 for r in results if r and r.get("outcome") == "stored")
    already_stored_count = sum(1 for r in results if r and r.get("outcome") == "already_stored")
    accepted_count = stored_count + already_stored_count
    failed_count = sum(1 for r in results if r and r.get("outcome") in ("failed_http", "failed_exception"))
    duration = time.monotonic() - t_start

    print(
        f"[{get_ts()}] [COMPLETE] {duration:.2f}s — "
        f"accepted={accepted_count}, newly_stored={stored_count}, already_stored={already_stored_count}, failed={failed_count}."
    )
    return {
        "status": "completed",
        "total_scanned": total_files,
        "accepted_by_orthanc": accepted_count,
        "newly_stored": stored_count,
        "already_stored": already_stored_count,
        "failed": failed_count,
        "total_time_sec": round(duration, 2),
    }


def start_api():
    uvicorn.run(app, host="127.0.0.1", port=MY_APP_PORT, log_level="error")

async def client_trigger():
    await asyncio.sleep(2)
    print(f"[{get_ts()}] [CLIENT] Triggering import for {SOURCE_PATH}...")
    async with httpx.AsyncClient(timeout=None, http2=True) as client:
        try:
            r = await client.post(f"http://127.0.0.1:{MY_APP_PORT}/fast-import")
            print(f"\n[{get_ts()}] RESULT: {r.json()}")
        except Exception as e:
            print(f"\n[{get_ts()}] [CLIENT ERROR] {e}")

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_api, daemon=True)
    server_thread.start()
    try:
        asyncio.run(client_trigger())
    except KeyboardInterrupt:
        print("\nExiting...")