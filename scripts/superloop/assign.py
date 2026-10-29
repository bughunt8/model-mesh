"""Link a superloop run to one validated row of the orchestration matrix.

The run names a situation, a profile and an option. This module reads that option from
examples/orchestration/matrix.example.json and returns the author, orchestrator, reviewer and
aggregator seats with their harnesses and model families, using the same family rules as
scripts/validate-orchestration.py. The profile and option are frozen for the whole run.
"""
import importlib.util, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MATRIX = os.path.join(ROOT, "examples", "orchestration", "matrix.example.json")
_spec = importlib.util.spec_from_file_location("_vo", os.path.join(ROOT, "scripts", "validate-orchestration.py"))
vo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vo)


def load_matrix(path=MATRIX):
    return json.load(open(path, encoding="utf-8"))


def seat(matrix, profile, s):
    ids = [matrix["models"][profile][m]["id"] for m in s["chain"]]
    return {"role": s.get("role"), "harness": s["harness"], "chain": list(s["chain"]), "model_ids": ids,
            "families": sorted(vo.families(matrix, profile, s["chain"]))}


def assignment(matrix, situation, profile, option):
    sit = next((s for s in matrix["situations"] if s["id"] == situation), None)
    if sit is None:
        raise KeyError(f"unknown situation {situation}")
    opt = next((o for o in sit["profiles"][profile]["options"] if o["name"] == option), None)
    if opt is None:
        raise KeyError(f"{situation}/{profile} has no option {option}")
    authors = [seat(matrix, profile, a) for a in opt["authors"]]
    routes = [seat(matrix, profile, {"role": "category:" + k, "harness": authors[0]["harness"], "chain": v})
              for k, v in opt.get("category_routes", {}).items()]
    return {
        "situation": situation, "title": sit["title"], "profile": profile, "option": option,
        "pattern": opt["pattern"], "lenses": list(sit.get("lenses", [])), "gates": dict(sit.get("gates", {})),
        "orchestrator": seat(matrix, profile, opt["orchestrator"]) if opt.get("orchestrator") else None,
        "authors": authors + routes,
        "reviewers": [dict(seat(matrix, profile, r), lenses=list(r.get("lenses", []))) for r in opt["reviewers"]],
        "aggregator": seat(matrix, profile, opt["aggregator"]),
        "hk_policy": profile == "ultimate",
    }


def family_of(model_id):
    return vo.model_family(model_id)
