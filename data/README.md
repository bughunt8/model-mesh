# Data files

## model-scores.csv

Eight-dimension scores per model. Columns: `model,AE,TO,IP,R,CR,VD,LC,REL,price_per_task,hermes_index,notes`.

`price_per_task` is the Hermes Index cost per task in USD. `hermes_index` is the
composite. Both are included for chain-economics checks; neither feeds the
dimension scores directly.

## profile-fits.csv

Per-profile slot weights and computed fits. Columns:
`profile,slot,model,dimensions,weights,fit,slot_weight,weighted,cxr`.

`dimensions` and `weights` are pipe-separated. `fit` is the weighted dimension
score before CXR. `weighted` is `fit * slot_weight`. `cxr` is the penalty
subtracted at the chain level.

## sources.yaml

Every benchmark source with URL, snapshot date, and harness notes. This is the
provenance record. If a number in the CSV cannot be traced to an entry here, it
is unverified and must be re-checked.

