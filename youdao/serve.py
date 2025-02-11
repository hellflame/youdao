try:
    import uvicorn
    from fastapi import FastAPI
except ImportError:
    print("""This Service Require Following Dependencies:
    fastapi
    uvicorn
    """)
    exit(1)

import os

from youdao.racer import Race

app = FastAPI(
    title="query dict share service",
    description="""the share service will reuse local sqlite storage by default, 
    try not to start service locally while using query cmd,
    at least use another db by setting env `YD_STORAGE`""")


@app.get("/query")
async def handle(phrase: str):
    return await Race().run(phrase, True)


def main(host=os.getenv("YD_HOST", "0.0.0.0"), port=int(os.getenv("YD_PORT", 3679))):
    uvicorn.run(app, host=host, port=port)

