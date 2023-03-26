import os     
     
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    pid = os.getpid()
    os.kill(pid, 9)