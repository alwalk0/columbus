# from multiprocessing import Process
# import psutil
# import pytest
# import requests
# import time
# import uvicorn

# HOST = "127.0.0.1"
# PORT = 8765
# WORKERS = 3


# def run_server(host: str, port: int, workers: int, wait: int = 15) -> Process:
#     proc = Process(
#         target=uvicorn.run,
#         args=("columbus.framework.main:app",),
#         kwargs={
#             "host": host,
#             "port": port,
#             "workers": workers,
#         },
#     )
#     proc.start()
#     time.sleep(wait)
#     assert proc.is_alive()
#     return proc


# def shutdown_server(proc: Process):

#     ##### SOLUTION #####
#     pid = proc.pid
#     parent = psutil.Process(pid)
#     for child in parent.children(recursive=True):
#         child.kill()
#     ##### SOLUTION END ####

#     proc.terminate()
#     for _ in range(5):
#         if proc.is_alive():
#             time.sleep(5)
#         else:
#             return
#     else:
#         raise Exception("Process still alive")


# def check_response(host: str, port: int):
#     assert requests.get(f"http://{host}:{port}").text == '"hello world"'


# def check_response_time(host: str, port: int, tol: float = 1e-2):
#     s = time.time()
#     requests.get(f"http://{host}:{port}")
#     e = time.time()
#     assert e-s < tol


# @pytest.fixture(scope="session")
# def server():
#     proc = run_server(HOST, PORT, WORKERS)
#     try:
#         yield
#     finally:
#         shutdown_server(proc)


# def test_main(server):
#     check_response(HOST, PORT)
#     check_response_time(HOST, PORT)
#     check_response(HOST, PORT)
#     check_response_time(HOST, PORT)