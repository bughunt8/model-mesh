"""Append-only, hash-chained run records, the cumulative provenance ledger and the lineage
registry.

events.jsonl gets one line per event. Each line carries the hash of the previous line, so a
deleted or edited line breaks the chain. A run never reuses an output directory that already
holds a log.

The provenance ledger records every harness and model family that authored or orchestrated
work in this run's lineage: the frozen cell's author and orchestrator seats with all their
fallback rungs, every model family left in the materialized omo config, every model a worker
session reported, the goal's prior_lineage, and every earlier run on the same branch or goal
found in the lineage registry. A reviewer is acceptable only if it shares no harness and no
family with anything in the ledger.

The lineage registry is a JSON-lines file outside the worktree and the run directory
(default ~/.local/state/model-mesh/superloop-lineage.jsonl, or MM_SUPERLOOP_REGISTRY). The
owner creates it once with `mm-superloop.py --init-registry`; a run refuses to start when it
is missing, because a missing registry is not an empty history. Each admitted run appends its
lineage, keyed by repository (the git common directory, so every branch and worktree of one
clone shares it) and by goal id. A new run in the same repository or on the same goal inherits
every earlier entry, whatever the goal file says. This is conservative: unrelated earlier work
in the same clone also counts. A worker running as the owner's OS user can still delete and
recreate the file; only isolation stops that.
"""
import hashlib, json, os


class EventLog:
    def __init__(self, path, clock):
        self.path, self.clock = path, clock
        self.prev = "0" * 64
        self.count = 0
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "x", encoding="utf-8"):
            pass

    def write(self, kind, **data):
        rec = {"n": self.count, "t": round(self.clock(), 3), "kind": kind, "prev": self.prev}
        rec.update(data)
        line = json.dumps(rec, sort_keys=True, ensure_ascii=False)
        self.prev = hashlib.sha256(line.encode()).hexdigest()
        self.count += 1
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return rec


def verify_chain(path):
    prev = "0" * 64
    for i, line in enumerate(open(path, encoding="utf-8")):
        rec = json.loads(line)
        if rec.get("prev") != prev or rec.get("n") != i:
            return False
        prev = hashlib.sha256(line.rstrip("\n").encode()).hexdigest()
    return True


class Provenance:
    def __init__(self):
        self.harnesses, self.families, self.entries = set(), set(), []

    def record(self, iteration, role, harness, families):
        self.harnesses.add(harness)
        self.families |= set(families)
        self.entries.append({"iteration": iteration, "role": role, "harness": harness, "families": sorted(families)})

    def conflicts(self, harness, families):
        out = []
        if harness in self.harnesses:
            out.append(f"harness {harness} already authored or orchestrated in this run")
        shared = sorted(self.families & set(families))
        if shared:
            out.append(f"families {shared} already authored or orchestrated in this run")
        return out

    def snapshot(self):
        return {"harnesses": sorted(self.harnesses), "families": sorted(self.families)}


def default_registry():
    return os.environ.get("MM_SUPERLOOP_REGISTRY") or os.path.join(
        os.path.expanduser("~"), ".local", "state", "model-mesh", "superloop-lineage.jsonl")


class Registry:
    def __init__(self, path):
        self.path = path

    def exists(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.loads(f.readline() or "{}").get("kind") == "header"
        except (OSError, ValueError):
            return False

    def init(self):
        if self.exists():
            return False
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        with open(self.path, "x", encoding="utf-8") as f:
            f.write(json.dumps({"kind": "header", "format": 1}) + "\n")
        return True

    def binding(self, repository):
        """The git directory the owner's repository id was first bound to, or None."""
        for e in self._entries():
            if e.get("kind") == "bind" and e.get("repository") == repository:
                return e.get("git_dir")
        return None

    def bind(self, repository, git_dir):
        self.append({"kind": "bind", "repository": repository, "git_dir": git_dir})

    def _entries(self):
        try:
            lines = open(self.path, encoding="utf-8").read().splitlines()
        except OSError:
            return []
        out = []
        for line in lines:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def prior(self, repo_key, goal_id):
        out = []
        try:
            for line in open(self.path, encoding="utf-8"):
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if e.get("repo_key") == repo_key or e.get("goal") == goal_id:
                    out.append(e)
        except OSError:
            pass
        return out

    def append(self, entry):
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
