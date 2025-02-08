"""
    fetch result from the backup server
    btw: customized server is not a must, but it will speed up a little the query progress
"""

import os
import httpx


class Customize(object):
    def __init__(self, service=os.getenv("YD_SERVICE", "http://127.0.0.1:3679/query")):
        self.service = service

    async def fetch(self, query):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.service, params={"phrase": query})
                resp.raise_for_status()
                return resp.json()
        except httpx.ConnectError:
            pass

    @staticmethod
    def parse(content):
        return content




