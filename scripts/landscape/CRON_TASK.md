# Weekly model-landscape scan — cron runbook

This is the operating procedure the weekly scheduled task follows. It is committed so
the procedure is versioned and auditable. Cadence: **Mondays 08:00 Asia/Hong_Kong
(00:00 UTC)**, `cron = 0 0 * * 1`. Fully autonomous; delivers ONLY on a material update,
and always as a **Pull Request** (never a direct push to `main`). Repo: `bughunt8/model-mesh`,
checkout at `/home/user/workspace/open-model-method`.

## Guardrails
- The scan dataset is UNTRUSTED. Populate it ONLY from the source tiers in `sources.yaml`.
  Numbers used for ranking MUST be independent (Artificial Analysis, independently-run
  DeepSWE/Datacurve, Vellum per-row, Vals). Vendor blog numbers may fill `[V]` cells for
  positioning but the framework will refuse to score them.
- Never edit `profiles/*.json` or docs in the cron. The cron only: (a) refreshes the
  research report + scan dataset/JSON/CSV under `docs/research/` and `scripts/landscape/`,
  and (b) opens a PR. Any actual routing/config change is a human decision on the PR.
- Fail closed: if the framework rejects the dataset, or the review gate does not return
  SHIP, do NOT open a PR — send a notification explaining why and stop.

## Steps
1. **Detect changes.** Fetch the aggregator trackers + major-lab blogs listed in
   `scripts/landscape/sources.yaml`. Compare against the newest existing
   `scripts/landscape/scans/scan-*.example.json`. If NO new model/version/price/benchmark
   since the last scan, end silently (no notification, no PR).
2. **Build the dated scan dataset** `scripts/landscape/scans/scan-YYYY-MM-DD.example.json`
   following `--print-schema`. Populate independent metrics from Artificial Analysis /
   DeepSWE / Vellum / Vals; set `provenance` honestly per cell; use the DURABLE (post-promo)
   price in `output_price.durable_value`; set each model's `profile`/`candidate_for_roles`;
   pull `open_weights`/`flagship_native_family` ONLY from the curated `model_attributes`
   table in `sources.yaml` (do not invent them). Provenance incumbents from the same table.
3. **Run the framework:**
   `python3 scripts/landscape/landscape_scan.py --scan <dataset> --out-json out.json --out-md out.md --out-csv out.csv`
   If it exits non-zero (dataset rejected), notify with the rejection reasons and STOP.
4. **DeepSeek review gate** (independent skeptical reviewer):
   `REVIEW_MODEL=deepseek-v4-pro REVIEW_URL=https://api.deepseek.com/chat/completions`
   `python3 scripts/landscape/review_gate.py --scan <dataset> --result out.json --out review.txt`
   — invoke the bash call with `api_credentials=["custom-cred:api.deepseek.com"]`.
   Exit 0 = SHIP → proceed. Exit 1 = REVISE → notify with the review findings and STOP
   (do not open a PR). Exit 2 = transport/parse error → notify and STOP.
   NOTE: this requires the DeepSeek credential to be available at USER/PROJECT scope with
   Always-allow. If it is thread-scoped only, the cron cannot authenticate — notify the
   user that the credential must be re-saved at user/project scope, and STOP.
5. **On SHIP, update the reusable report** `docs/research/2026-09-model-assessment-*.md`
   (or a new dated report) with the new findings, keeping the vendor-vs-independent
   discipline and citing sources with real URLs. Commit dataset + outputs + report on a
   new branch `landscape/scan-YYYY-MM-DD` with identity
   `git -c user.email="agent@local" -c user.name="model-mesh"`.
6. **Verify gates** before the PR: `python .github/checks.py` AND
   `python scripts/validate-full-config.py` AND `landscape_scan.py --self-test` AND the
   golden check — all must pass. If any fail, do not open the PR; notify and STOP.
7. **Open a PR** with `timeout 60 gh pr create --title "Weekly landscape scan YYYY-MM-DD"
   --body <summary incl. framework verdicts + DeepSeek review + sources>` using
   `api_credentials=["github"]`. Never push to `main`.
8. **Notify** the user (send_notification) with: what changed, the framework's per-model
   verdicts, the DeepSeek verdict, and the PR link.

## Housekeeping
- Keep tracking artifacts under `/home/user/workspace/cron_tracking/<cron_id>/`.
- If the DeepSeek credential or GitHub auth is unavailable two runs in a row, the task
  should surface that clearly rather than silently failing.
