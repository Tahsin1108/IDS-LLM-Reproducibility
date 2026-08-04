# Cross-Dataset Validation

## Datasets

| Dataset | Experimental role | Main evaluation |
|---|---|---|
| CIC-IDS2017 | Primary development dataset | IDS, SHAP evidence, risk policy, and evidence-grounded reporting |
| UNSW-NB15 | Independent external-validation dataset | Dataset-specific IDS replication and A0-A4 reporting ablation |

## Shared framework components

Both dataset experiments evaluate:

1. train-only or leakage-aware preprocessing;
2. Random Forest intrusion prediction;
3. confidence and uncertainty;
4. attack-stage mapping;
5. risk and response-policy assignment;
6. per-event SHAP evidence;
7. evidence-constrained LLM reporting;
8. unsupported-claim indicators;
9. verifier-controlled report construction.

## Methodological interpretation

CIC-IDS2017 and UNSW-NB15 have different feature spaces, class
taxonomies, and traffic distributions. Therefore, a classifier
trained directly on CIC-IDS2017 was not evaluated on raw UNSW-NB15
features.

Dataset-specific IDS models were trained and evaluated under their
respective protocols. Cross-dataset generalization was assessed at
the framework level using harmonized reporting, evidence, uncertainty,
policy, and verification procedures.

## UNSW-NB15 reporting evaluation

The UNSW-NB15 reporting experiment used 300 class-balanced events:

- 10 classes;
- 30 events per class;
- 150 correct predictions;
- 150 misclassifications.

The same events were evaluated under five reporting configurations:

- A0: deterministic template;
- A1: unconstrained language-model generation;
- A2: constrained generation without SHAP;
- A3: constrained generation with full SHAP evidence;
- A4: evidence-contract verifier and deterministic renderer.

Evaluation-only ground truth was not exposed to the language model.

## Reproducibility artifacts

The UNSW-NB15 artifacts are stored under:

`datasets/unsw_nb15/`

The raw datasets and Qwen model weights are not included.
