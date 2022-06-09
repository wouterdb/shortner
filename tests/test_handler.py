from inmanta.agent.handler import HandlerContext

def test_handler(api_key, project):
    def make_model(purged = False):
        project.compile(f"""
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

    changes = project.dryrun_resource("shortner::ShortUrl")
    assert "purged" in changes

    project.deploy_resource("shortner::ShortUrl")
    # facts pushed on create
    assert "short_url" in [x["id"] for x in project.ctx._facts]

    changes = project.dryrun_resource("shortner::ShortUrl")
    assert not changes
    # facts pushed on dryrun
    facts_by_id = {x["id"]:x for x in project.ctx._facts}
    assert "short_url" in facts_by_id
    short_url = facts_by_id["short_url"]["value"]

    #get_facts
    resource = project.get_resource("shortner::ShortUrl")
    handler = project.get_handler(resource, False)
    ctx = HandlerContext(resource)
    facts = handler.facts(ctx, resource)
    assert facts == {"short_url":short_url}

    make_model(purged=True)

    changes = project.dryrun_resource("shortner::ShortUrl")
    assert "purged" in changes

    project.deploy_resource("shortner::ShortUrl")

    changes = project.dryrun_resource("shortner::ShortUrl")
    assert not changes



