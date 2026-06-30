# Reproducibility Protocol

This repository provides the reproducibility package for the IDS-to-LLM incident reporting framework.

## Dataset

The raw CIC-IDS2017 dataset is not redistributed in this repository.
Download it from the Canadian Institute for Cybersecurity:

https://www.unb.ca/cic/datasets/ids-2017.html

Expected dataset: CIC-IDS2017 CSV flow records.

## Main seed

All deterministic components use:

```text
random_state = 42
seed = 42
```

## Data split

The experiment uses an 80/20 stratified train-test split.

Expected split size:

```text
Training samples: 320,000
Test samples: 80,000
```

## Main model

Random Forest:

```text
n_estimators = 150
max_depth = 20
class_weight = balanced_subsample
random_state = 42
n_jobs = -1
```

## Decision Tree baseline

Decision Tree:

```text
criterion = gini
max_depth = 20
class_weight = balanced
random_state = 42
```

## Risk scoring

Risk score:

```text
risk_score = clip(stage_severity * confidence * asset_criticality, 0, 10)
```

Default experimental asset criticality:

```text
asset_criticality = 1.0
```

Deployment tiers:

```text
low = 0.8
standard = 1.0
high = 1.2
```

Thresholds:

```text
0 <= R <= 2      -> Monitor
2 < R <= 5       -> Alert SOC Analyst
5 < R <= 7       -> Block Source IP
7 < R <= 8.5     -> Isolate Host
R > 8.5          -> Isolate Host and Escalate Immediately
```

## LLM

The LLM used in the paper is:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

The LLM is used only as an evidence-constrained report generator.
It is not used as an independent detector.

## Main reproducibility files

```text
notebooks/Test.ipynb
configs/main_config.yaml
configs/risk_policy.yaml
requirements.txt
runtime_info.txt
```

## Important artifact folders

```text
artifacts/models/
artifacts/preprocessing/
artifacts/risk_policy/
artifacts/evidence/
artifacts/prompts/
artifacts/reports/
artifacts/results/
figures/
```

## How to verify

1. Install dependencies from requirements.txt.
2. Download CIC-IDS2017.
3. Run notebooks/Test.ipynb.
4. Confirm that generated tables match artifacts/results/.
5. Confirm that the risk policy matches configs/risk_policy.yaml.
6. Confirm that evidence bundles, prompts, and reports use the same event IDs.

## Notes

The risk-policy values are author-defined, domain-informed heuristics.
They are not learned from the dataset and are not directly derived from CVSS.