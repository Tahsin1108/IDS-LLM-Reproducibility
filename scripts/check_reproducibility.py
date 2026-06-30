import os
import sys
import json
import pandas as pd

try:
    import yaml
except Exception:
    yaml = None

try:
    import joblib
except Exception:
    joblib = None


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

failures = []
warnings = []


def rel(path):
    return os.path.join(ROOT, path)


def check_exists(path, required=True):
    full_path = rel(path)
    if os.path.exists(full_path):
        print(f"[FOUND] {path}")
        return True
    if required:
        print(f"[MISSING] {path}")
        failures.append(path)
    else:
        print(f"[OPTIONAL MISSING] {path}")
        warnings.append(path)
    return False


def check_csv_value(path, row_filter_col, row_filter_value, metric_col, expected, tol=1e-4):
    full_path = rel(path)
    if not os.path.exists(full_path):
        failures.append(path)
        print(f"[MISSING] {path}")
        return

    df = pd.read_csv(full_path)

    if row_filter_col not in df.columns or metric_col not in df.columns:
        failures.append(path)
        print(f"[FAIL] {path}: missing expected columns")
        return

    row = df[df[row_filter_col].astype(str) == str(row_filter_value)]

    if row.empty:
        failures.append(path)
        print(f"[FAIL] {path}: row not found for {row_filter_value}")
        return

    observed = float(row.iloc[0][metric_col])

    if abs(observed - expected) <= tol:
        print(f"[PASS] {path}: {row_filter_value} {metric_col} = {observed}")
    else:
        failures.append(path)
        print(
            f"[FAIL] {path}: {row_filter_value} {metric_col} "
            f"expected {expected}, observed {observed}"
        )


print("=" * 80)
print("IDS-LLM Reproducibility Checker")
print("=" * 80)

print("\n[1] Checking core files")
core_files = [
    "README.md",
    "REPRODUCIBILITY.md",
    "requirements.txt",
    "runtime_info.txt",
    "configs/main_config.yaml",
    "configs/risk_policy.yaml",
    "data/README_CICIDS2017.md",
    "notebooks/Test.ipynb",
]

for f in core_files:
    check_exists(f)


print("\n[2] Checking model and preprocessing artifacts")
artifact_files = [
    "artifacts/models/rf_model.pkl",
    "artifacts/models/decision_tree_table_i_exact.joblib",
    "artifacts/models/rf_model_params.json",
    "artifacts/models/decision_tree_params.json",
    "artifacts/preprocessing/feature_columns.pkl",
    "artifacts/preprocessing/label_encoder.pkl",
    "artifacts/preprocessing/preprocessing_summary.csv",
]

for f in artifact_files:
    check_exists(f)


print("\n[3] Checking risk-policy artifacts")
risk_files = [
    "artifacts/risk_policy/stage_severity_table.csv",
    "artifacts/risk_policy/raw_label_stage_severity_table.csv",
    "artifacts/risk_policy/action_threshold_table.csv",
    "artifacts/risk_policy/asset_factor_sensitivity_300.csv",
    "artifacts/risk_policy/risk_zone_distribution_300.csv",
    "artifacts/risk_policy/risk_policy_event_audit_300.csv",
]

for f in risk_files:
    check_exists(f)


print("\n[4] Checking evidence, prompt, and report artifacts")
evidence_files = [
    "artifacts/evidence/local_shap_evidence_300.csv",
    "artifacts/evidence/instance_level_evidence_bundle_300.csv",
    "artifacts/prompts/instance_level_llm_prompts_300.csv",
    "artifacts/reports/instance_level_llm_reports_300.csv",
    "prompts/evidence_constrained_prompt_template.txt",
]

for f in evidence_files:
    check_exists(f)


print("\n[5] Checking result tables")
result_files = [
    "artifacts/results/table_i_model_comparison.csv",
    "artifacts/results/table_ii_stage_classification.csv",
    "artifacts/results/table_iii_stage_severity_zones.csv",
    "artifacts/results/table_iv_asset_sensitivity.csv",
    "artifacts/results/table_v_factual_consistency.csv",
    "artifacts/results/table_vi_300_event_composition.csv",
    "artifacts/results/table_vii_rare_class_detection.csv",
    "artifacts/results/table_viii_dt_rf_uncertainty_utility.csv",
    "artifacts/results/table_vi_dt_vs_rf_calibration.csv",
    "artifacts/results/confidence_review_routing_dt_vs_rf.csv",
    "artifacts/results/risk_coverage_dt_vs_rf.csv",
    "artifacts/results/dt_vs_rf_event_confidence.csv",
    "artifacts/results/dt_exact_reproduction_check.csv",
]

for f in result_files:
    check_exists(f)


print("\n[6] Checking figures")
figure_files = [
    "figures/fig_1_architecture.png",
    "figures/fig_2_raw_confusion_matrix.png",
    "figures/fig_3_stage_confusion_matrix.png",
    "figures/fig_4_global_feature_importance.png",
    "figures/fig_5_risk_score_distribution_policy_zones_300.png",
    "figures/fig_6_confidence_vs_risk_by_action_300.png",
    "figures/fig_7_explanation_quality_comparison.png",
    "figures/fig_8_hallucination_analysis.png",
    "figures/fig_9_confidence_distribution_dt_vs_rf.png",
    "figures/fig_10_risk_coverage_dt_vs_rf.png",
]

for f in figure_files:
    check_exists(f, required=False)


print("\n[7] Checking config values")
if yaml is None:
    warnings.append("pyyaml not installed")
    print("[WARN] pyyaml not installed, skipping YAML checks")
else:
    main_config_path = rel("configs/main_config.yaml")
    risk_config_path = rel("configs/risk_policy.yaml")

    if os.path.exists(main_config_path):
        with open(main_config_path, "r") as f:
            main_config = yaml.safe_load(f)

        seed = main_config.get("seed")
        if seed == 42:
            print("[PASS] main_config seed = 42")
        else:
            failures.append("main_config seed")
            print(f"[FAIL] main_config seed expected 42, observed {seed}")

        rf = main_config.get("random_forest", {})
        expected_rf = {
            "n_estimators": 150,
            "max_depth": 20,
            "class_weight": "balanced_subsample",
            "random_state": 42,
        }

        for k, expected in expected_rf.items():
            observed = rf.get(k)
            if observed == expected:
                print(f"[PASS] random_forest.{k} = {observed}")
            else:
                failures.append(f"random_forest.{k}")
                print(f"[FAIL] random_forest.{k} expected {expected}, observed {observed}")

    if os.path.exists(risk_config_path):
        with open(risk_config_path, "r") as f:
            risk_config = yaml.safe_load(f)

        asset_default = risk_config.get("asset_criticality", {}).get("experimental_default")
        if float(asset_default) == 1.0:
            print("[PASS] asset_criticality.experimental_default = 1.0")
        else:
            failures.append("asset criticality default")
            print(f"[FAIL] asset default expected 1.0, observed {asset_default}")

        thresholds = risk_config.get("thresholds", {})
        expected_thresholds = {
            "monitor_max": 2.0,
            "alert_max": 5.0,
            "block_max": 7.0,
            "isolation_max": 8.5,
        }

        for k, expected in expected_thresholds.items():
            observed = float(thresholds.get(k))
            if abs(observed - expected) <= 1e-9:
                print(f"[PASS] thresholds.{k} = {observed}")
            else:
                failures.append(f"thresholds.{k}")
                print(f"[FAIL] thresholds.{k} expected {expected}, observed {observed}")


print("\n[8] Checking Table I values")
if os.path.exists(rel("artifacts/results/table_i_model_comparison.csv")):
    check_csv_value(
        "artifacts/results/table_i_model_comparison.csv",
        "Model",
        "Random Forest",
        "Accuracy",
        0.9952,
        tol=1e-4,
    )

    check_csv_value(
        "artifacts/results/table_i_model_comparison.csv",
        "Model",
        "Random Forest",
        "Macro_F1",
        0.7423,
        tol=1e-4,
    )

    check_csv_value(
        "artifacts/results/table_i_model_comparison.csv",
        "Model",
        "Decision Tree",
        "Accuracy",
        0.9969,
        tol=1e-4,
    )

    check_csv_value(
        "artifacts/results/table_i_model_comparison.csv",
        "Model",
        "Decision Tree",
        "Macro_F1",
        0.8065,
        tol=1e-4,
    )


print("\n[9] Checking model parameter dumps")
for param_file in [
    "artifacts/models/rf_model_params.json",
    "artifacts/models/decision_tree_params.json",
]:
    full_path = rel(param_file)
    if not os.path.exists(full_path):
        continue

    with open(full_path, "r") as f:
        params = json.load(f)

    print(f"[INFO] {param_file}")
    for key in ["n_estimators", "max_depth", "class_weight", "random_state"]:
        if key in params:
            print(f"       {key}: {params[key]}")


print("\n[10] Evidence-bundle sanity check")
bundle_path = rel("artifacts/evidence/instance_level_evidence_bundle_300.csv")

if os.path.exists(bundle_path):
    df = pd.read_csv(bundle_path)

    print(f"[INFO] evidence bundle shape: {df.shape}")

    lower_cols = [c.lower() for c in df.columns]

    concept_keywords = {
        "predicted label": ["predicted", "label"],
        "confidence": ["confidence"],
        "attack stage": ["stage"],
        "risk score": ["risk"],
        "recommended action": ["action"],
    }

    for concept, keywords in concept_keywords.items():
        found = any(all(k in col for k in keywords) for col in lower_cols)
        if found:
            print(f"[PASS] evidence bundle contains {concept}")
        else:
            warnings.append(f"evidence bundle missing {concept}")
            print(f"[WARN] evidence bundle may be missing {concept}")


print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

if warnings:
    print("\nWarnings:")
    for w in warnings:
        print(f"- {w}")

if failures:
    print("\nFailures:")
    for f in failures:
        print(f"- {f}")

    print("\nREPRODUCIBILITY CHECK: FAILED")
    sys.exit(1)

print("\nREPRODUCIBILITY CHECK: PASSED")
sys.exit(0)
