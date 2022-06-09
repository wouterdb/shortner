"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
from calendar import c
from inmanta.plugins import plugin

from inmanta.resources import PurgeableResource, resource
from inmanta.agent.handler import provider, ResourcePurged, HandlerContext, CRUDHandler
from typing import Optional, Dict
import requests

@resource("shortner::ShortUrl", agent="agent", id_attribute="long_url")
class ShortUrl(PurgeableResource):
    fields = ("long_url", "api_key")

@provider("shortner::ShortUrl", name="rebrandly")
class RebrandlyHandler(CRUDHandler):

    def find_instance(self, ctx: HandlerContext, resource: ShortUrl) -> Optional[dict]:
        url = "https://api.rebrandly.com/v1/links"
        headers = {
            "Accept": "application/json",
            "apikey": resource.api_key
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        found = [record for record in response.json() if record["destination"] == resource.long_url]
        ctx.info("Found records: %(records)s", records=found)
        if len(found) == 0:
            return None
        if len(found) > 1:
            raise Exception("Found multiple matches, aborting")
        return found[0]

    def read_resource(self, ctx: HandlerContext, resource: ShortUrl) -> None:
        instance = self.find_instance(ctx, resource)
        if instance is None:
            raise ResourcePurged()
       
        ctx.set("record_id", instance["id"])
        # No values to set on the resources
        ctx.set_fact("short_url", instance["shortUrl"])

    def create_resource(self, ctx: HandlerContext, resource: ShortUrl) -> None:
        url = "https://api.rebrandly.com/v1/links"
        payload = {"destination": resource.long_url}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": resource.api_key,
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        ctx.set_fact("short_url", response.json()["shortUrl"])
        
    def update_resource(self, ctx: HandlerContext, changes: dict, resource: ShortUrl) -> None:
        raise Exception("update is not supported")
        
    def delete_resource(self, ctx: HandlerContext, resource: ShortUrl) -> None:
        link_id = ctx.get("record_id")
        url = f"https://api.rebrandly.com/v1/links/{link_id}"
        headers = {
            "Accept": "application/json",
            "apikey": resource.api_key
        }
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

    def facts(self, ctx: HandlerContext, resource: ShortUrl) -> Dict[str, object]:
        instance = self.find_instance(ctx, resource)
        if instance is None:
            return {}
       
        return {"short_url": instance["shortUrl"]}