from inmanta.agent.handler import HandlerContext


def test_handler(api_key, project, rebrandly):
    def make_model(purged=False):
        project.compile(
            f"""
            import shortner

            shortner::ShortUrl(
                long_url="https://inmanta.com/",
                api_key="{api_key}",
                purged={str(purged).lower()}
            )

        """
        )

    make_model()
    r = project.get_resource("shortner::ShortUrl")
    assert r
    assert r.api_key == api_key
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

    make_model(purged=True)

    result = project.dryrun_resource_v2("shortner::ShortUrl")
    assert "purged" in result.changes

    project.deploy_resource_v2("shortner::ShortUrl")

    result = project.dryrun_resource_v2("shortner::ShortUrl")
    assert not result.changes
