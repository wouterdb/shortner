from pytest_inmanta.plugin import Project

import inmanta_plugins.shortner
from inmanta.agent.handler import HandlerContext


def test_handler(
    project: Project, shlink: inmanta_plugins.shortner.ShlinkClient, test_url: str
):
    def make_model(purged=False):
        project.compile(
            f"""
            import shortner

            server = shortner::ShlinkServer(
                url = "{shlink.server_url}",
                api_key = "{shlink.api_key}",
            )
            
            shortner::ShortUrl(
                long_url = "{test_url}",
                server = server,
                purged = {str(purged).lower()}
            )

        """
        )

    make_model()
    r = project.get_resource("shortner::ShortUrl")
    assert r
    assert r.api_key == shlink.api_key
    assert r.server_url == shlink.server_url
    assert r.long_url == "https://inmanta.com/"

    result = project.dryrun_resource_v2("shortner::ShortUrl")
    assert "purged" in result.changes

    result = project.deploy_resource_v2("shortner::ShortUrl")
    # facts pushed on create
    assert "short_url" in [x["id"] for x in result.ctx._facts]

    result = project.dryrun_resource_v2("shortner::ShortUrl")
    assert not result.changes
    # facts pushed on dryrun
    facts_by_id = {x["id"]: x for x in result.ctx._facts}
    assert "short_url" in facts_by_id
    short_url = facts_by_id["short_url"]["value"]

    # get_facts
    resource = project.get_resource("shortner::ShortUrl")
    handler = project.get_handler(resource, False)
    ctx = HandlerContext(resource)
    handler.facts(ctx, resource)
    facts_by_id = {x["id"]: x for x in ctx._facts}
    assert "short_url" in facts_by_id
    assert short_url == facts_by_id["short_url"]["value"]

    # delete
    make_model(purged=True)

    result = project.dryrun_resource_v2("shortner::ShortUrl")
    assert "purged" in result.changes

    project.deploy_resource_v2("shortner::ShortUrl")

    result = project.dryrun_resource_v2("shortner::ShortUrl")
    assert not result.changes
