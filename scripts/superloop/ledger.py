"""Append-only, hash-chained run records and the cumulative provenance ledger.

events.jsonl gets one line per event. Each line carries the hash of the previous line, so a
deleted or edited line breaks the chain. The provenance ledger records every harness and model
family that authored or orchestrated work in this run's lineage, across all fallback rungs,
because the answering rung is not always known. A reviewer is acceptable only if it shares no
harness and no family with anything in the ledger.
"""
import hashlib, json, os


class EventLog:
    def __init__(self, path, clock):
        self.path, self.clock = path, clock
        self.prev = "0" * 64
        self.count = 0
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()

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
