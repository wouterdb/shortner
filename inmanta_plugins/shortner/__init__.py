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

import urllib.parse
from typing import Dict, Optional

import requests

from inmanta.agent.handler import (
    CRUDHandler,
    HandlerContext,
    LoggerABC,
    ResourcePurged,
    provider,
)
from inmanta.resources import PurgeableResource, resource


class ShlinkClient:

    def __init__(self, server_url: str, api_key: str) -> None:
        self.api_key = api_key
        self.server_url = server_url

    def find_instance_for(
        self, long_url: str, logger: Optional[LoggerABC] = None
    ) -> Optional[dict]:
        url = urllib.parse.urljoin(self.server_url, "rest/v3/short-urls")
        headers = {"Accept": "application/json", "X-Api-Key": self.api_key}
        # this matches sub strings, so needs another filter to prevent confusing
        # it.co and it.com
        body = {"searchTerm": long_url, "itemsPerPage": 100}
        response = requests.get(url, headers=headers, params=body)
        response.raise_for_status()

        # we don't fully handle paging, as we expect less then 100 results
        connection = response.json()["shortUrls"]
        pages = connection["pagination"]["pagesCount"]
        assert pages <= 1, "Got >100 matches for this URL, this is not supported yet"

        found = [
            record for record in connection["data"] if record["longUrl"] == long_url
        ]
        if logger:
            logger.info("Found records: %(records)s", records=found)
        if len(found) == 0:
            return None
        if len(found) > 1:
            raise Exception("Found multiple matches, aborting")
        return found[0]

    def create(self, long_url: str) -> dict:
        """Create a new url"""
        url = urllib.parse.urljoin(self.server_url, "rest/v3/short-urls")
        headers = {"Accept": "application/json", "X-Api-Key": self.api_key}

        payload = {
            "longUrl": long_url,
            "findIfExists": True,
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def shorten(self, long_url: str) -> str:
        """Create a new shortened URL, return the short form"""
        return self.create(long_url=long_url)["shortUrl"]

    def delete_instance(self, instance_id: str) -> None:
        """Delete a shortened link, given its id"""
        url = urllib.parse.urljoin(self.server_url, f"rest/v3/short-urls/{instance_id}")
        headers = {"Accept": "application/json", "X-Api-Key": self.api_key}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()


@resource("shortner::ShortUrl", agent="server.url", id_attribute="long_url")
class ShortUrl(PurgeableResource):
    fields = ("long_url", "server_url", "api_key")

    @classmethod
    def get_server_url(cls, exporter, resource):
        return resource.server.url

    @classmethod
    def get_api_key(cls, exporter, resource):
        return resource.server.api_key


@provider("shortner::ShortUrl", name="rebrandly")
class RebrandlyHandler(CRUDHandler):

    record_id: str | None

    def read_resource(self, ctx: HandlerContext, resource: ShortUrl) -> None:
        client = ShlinkClient(api_key=resource.api_key, server_url=resource.server_url)

        instance = client.find_instance_for(resource.long_url, ctx)

        if instance is None:
            raise ResourcePurged()

        self.record_id = instance["shortCode"]
        self.publish_facts(ctx, instance)

    def publish_facts(self, ctx: HandlerContext, instance: dict) -> None:
        ctx.set_fact("short_url", instance["shortUrl"])

    def create_resource(self, ctx: HandlerContext, resource: ShortUrl) -> None:
        client = ShlinkClient(api_key=resource.api_key, server_url=resource.server_url)
        instance = client.create(resource.long_url)
        self.publish_facts(ctx, instance)
        ctx.set_created()

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: ShortUrl
    ) -> None:
        raise Exception("update is not supported")

    def delete_resource(self, ctx: HandlerContext, resource: ShortUrl) -> None:
        link_id = self.record_id
        assert link_id is not None
        client = ShlinkClient(api_key=resource.api_key, server_url=resource.server_url)
        client.delete_instance(link_id)
        ctx.set_purged()

    def facts(self, ctx: HandlerContext, resource: ShortUrl) -> Dict[str, object]:
        client = ShlinkClient(api_key=resource.api_key, server_url=resource.server_url)
        instance = client.find_instance_for(resource.long_url, ctx)
        if instance is None:
            return {}

        self.publish_facts(ctx, instance)
        return {}
