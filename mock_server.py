"""
Mock API server for testing when there is a need to simulate the operation of an external API.
FastAPI for example.
"""

import multiprocessing
from fastapi import FastAPI, HTTPException
from uvicorn import Server, Config

import config

app = FastAPI()


@app.post("/upload")
async def test(path: str):
    if path == "test":
        return {"detail": "success"}
    else:
        raise HTTPException(status_code=404, detail="error")


class UvicornServer(multiprocessing.Process):
    def __init__(self, config: Config):
        super().__init__()
        self.server = Server(config=config)
        self.config = config

    def stop(self):
        self.terminate()

    def run(self, *args, **kwargs):
        self.server.run()


conf = Config(app, host=config.KIAO_RM_WEB_CRAWLERS_IP_ADDRESS, port=int(config.KIAO_RM_WEB_CRAWLERS_PORT))
mock_server = UvicornServer(config=conf)


# Pytest fixture. Add in conftest.py
@pytest.fixture(autouse=True, scope="session")
async def run_mock_api():
    mock_server.start()
    yield
    mock_server.stop()
    
