"""TalkDesk's API as one object: the pages layer (page objects and API clients).

Tests say what they want to do (submit a talk, review it) and only this file
knows the addresses. If an endpoint moves, it changes here, once, instead of
in every test that calls it.
"""


class TalkDeskApi:
    def __init__(self, client):
        self._client = client

    def submit_talk(self, **talk):
        return self._client.post("/api/talks", json=talk)

    def get_talk(self, talk_id):
        return self._client.get(f"/api/talks/{talk_id}")

    def list_talks(self, **filters):
        return self._client.get("/api/talks", params=filters)

    def search_talks(self, words):
        return self._client.get("/api/talks/search", params={"q": words})

    def review_talk(self, talk_id, **review):
        return self._client.patch(f"/api/talks/{talk_id}", json=review)
