from .models import RepositoryFile, RepositorySnapshot

IGNORED_PREFIXES = (".git/", "node_modules/", "dist/", "build/", ".next/", "coverage/")

def build_snapshot(repo: dict, tree: dict, ref: str, commit_sha: str) -> RepositorySnapshot:
    files: list[RepositoryFile] = []
    for item in tree.get("tree", []):
        if item.get("type") != "blob":
            continue
        path = item.get("path", "")
        if path.startswith(IGNORED_PREFIXES):
            continue
        files.append(RepositoryFile(path=path, size=int(item.get("size") or 0), sha=item.get("sha")))
    return RepositorySnapshot(owner=repo["owner"]["login"], name=repo["name"], full_name=repo["full_name"], default_branch=repo.get("default_branch", "main"), ref=ref, commit_sha=commit_sha, files=files)
