from dataclasses import dataclass
from typing import Any

@dataclass
class GitHubClient:
    """Transport boundary; HTTP/auth is injected by the application layer."""
    transport: Any

    def get_repository(self, owner: str, name: str) -> dict:
        return self.transport.get(f"/repos/{owner}/{name}")

    def get_tree(self, owner: str, name: str, ref: str) -> dict:
        return self.transport.get(f"/repos/{owner}/{name}/git/trees/{ref}?recursive=1")
