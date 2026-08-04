# UNSW-NB15 External Validation

This directory contains the reproducibility artifacts for the
UNSW-NB15 external validation of the evidence-grounded intrusion
reporting framework presented in:

**From Intrusion Detection to Evidence-Grounded Incident Reporting:
An Explainable AI and Large Language Model Framework**

## Purpose

The UNSW-NB15 experiment evaluates whether the framework developed
with CIC-IDS2017 remains applicable to an independent intrusion-
detection dataset with different classes, distributions, and feature
semantics.

This experiment is described as:

- cross-dataset validation;
- external validation; or
- independent dataset replication.

It is not conventional k-fold cross-validation.

## Dataset protocols

Two UNSW-NB15 protocols were implemented:

- Protocol A: official training and testing partitions;
- Protocol B: conservative leakage-controlled evaluation.

The raw UNSW-NB15 dataset is not redistributed.

## Reporting population

The report-generation evaluation uses a class-balanced subset of
300 events:

- 10 classes;
- 30 events per class;
- 150 correctly classified events;
- 150 misclassified events.

Ground-truth information was stored separately from the evidence
bundles supplied to the language model.

## Reporting configurations

- A0: deterministic template baseline;
- A1: unconstrained Qwen generation;
- A2: constrained Qwen generation without local SHAP evidence;
- A3: constrained Qwen generation with full local evidence;
- A4: evidence-contract-bound deterministic verifier and renderer.

The language model was:

`Qwen/Qwen2.5-1.5B-Instruct`

Deterministic decoding was used.

## Main reporting results

For the 300-event class-balanced subset:

- A4 strict structural compliance: 100%;
- A4 prediction-contract compliance: 100%;
- A4 evidence-contract compliance: 100%;
- A4 automatic unsupported-claim indicator rate: 0%;
- A4 verifier quality gates: 300/300.

Raw A3 full-evidence generation achieved:

- strict structural compliance: 0%;
- prediction-contract compliance: 42.0%;
- evidence-contract compliance: 19.33%;
- token-limit occurrence: 7.0%.

## Directory contents

- `evidence_bundles/`: LLM-facing and evaluation-only evidence;
- `prompts/`: frozen prompt bank;
- `reports/`: A0-A4 reports;
- `generation_summaries/`: Qwen generation summaries;
- `verifier/`: A4 verifier outputs;
- `evaluation/`: corrected report-level evaluation;
- `statistics/`: paired statistical tests;
- `manuscript/`: manuscript tables, figures, and results text;
- `validation/`: checksums and validation records;
- `environment/`: software environment information;
- `notebooks/`: project notebook;
- `scripts/`: reproducibility checker.

## Reproducibility status

The final validation completed with:

- 83/83 checks passed;
- 80/80 mandatory checks passed;
- zero mandatory failures;
- ZIP integrity passed.

Use:

`validation/sha256_checksums.csv`

to verify the packaged files.

## Data and model availability

The raw UNSW-NB15 dataset is excluded. Users must obtain the dataset
from an authorized source and comply with its distribution terms.

The Qwen model weights are also excluded. The recorded model
identifier can be used to obtain the model separately.
