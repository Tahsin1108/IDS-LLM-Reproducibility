# IDS-LLM-Reproducibility

This repository contains the reproducibility package for the paper:

**From Intrusion Detection to Evidence-Grounded Incident Reporting: An Explainable AI and Large Language Model Framework**

The framework uses CIC-IDS2017, Random Forest classification, per-instance SHAP evidence, transparent risk scoring, and evidence-constrained LLM reporting.

## Main components

- CIC-IDS2017 preprocessing and split configuration
- Seven-model IDS classifier comparison
- Random Forest IDS model
- Decision Tree baseline reproduction
- Attack-stage mapping
- Risk-score and response-action policy
- Per-instance SHAP evidence extraction
- Evidence-constrained LLM prompt construction
- LLM incident-report generation
- Factual-consistency and hallucination checks
- DT-vs-RF uncertainty utility analysis

## Reproducibility

The key fixed seed is `42`.

The main notebook is located at:

`notebooks/Test.ipynb`

Configuration files are located at:

- `configs/main_config.yaml`
- `configs/risk_policy.yaml`

The raw CIC-IDS2017 dataset is not redistributed in this repository. It should be downloaded from the Canadian Institute for Cybersecurity.
