# Evidence, Prompt, and Report Artifacts

This folder contains the final per-instance evidence and LLM-reporting artifacts used in the paper.

## Files

- `artifacts/evidence/local_shap_evidence_300.csv`
  - Top per-instance SHAP features for the 300-event explanation subset.

- `artifacts/evidence/instance_level_evidence_bundle_300.csv`
  - Machine-readable evidence bundle for each event.
  - Includes predicted label, confidence, attack stage, risk score, policy zone, recommended action, and SHAP evidence.

- `artifacts/prompts/instance_level_llm_prompts_300.csv`
  - Final evidence-constrained prompts supplied to the LLM.

- `artifacts/reports/instance_level_llm_reports_300.csv`
  - LLM-generated incident reports for the same 300 events.

- `prompts/evidence_constrained_prompt_template.txt`
  - Generic prompt template used to construct the evidence-constrained prompts.

## Important

The older `xir_*` files are not used in the final reproducibility package because they were generated from an earlier risk-policy implementation.
