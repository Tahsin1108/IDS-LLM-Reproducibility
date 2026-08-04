from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

VALIDATION_FILE = (
    ROOT
    / "validation"
    / "final_validation_checks.csv"
)

MANIFEST_FILE = (
    ROOT
    / "validation"
    / "final_reproducibility_manifest.json"
)

CHECKSUM_FILE = (
    ROOT
    / "validation"
    / "sha256_checksums.csv"
)


def to_boolean(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.astype(bool)

    normalized = (
        series.astype(str)
        .str.strip()
        .str.lower()
    )

    return normalized.map({
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "1.0": True,
        "0.0": False,
    })


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as input_file:
        while chunk := input_file.read(1024 * 1024):
            digest.update(chunk)

    return digest.hexdigest()


def main() -> int:
    required_files = [
        VALIDATION_FILE,
        MANIFEST_FILE,
        CHECKSUM_FILE,
    ]

    missing_files = [
        path
        for path in required_files
        if not path.exists()
    ]

    if missing_files:
        print("Missing required files:")

        for path in missing_files:
            print(f"- {path}")

        return 1

    validation = pd.read_csv(
        VALIDATION_FILE,
        low_memory=False
    )

    validation["passed"] = to_boolean(
        validation["passed"]
    )

    with MANIFEST_FILE.open(
        "r",
        encoding="utf-8"
    ) as input_file:
        manifest = json.load(input_file)

    mandatory_failures = validation[
        (
            validation["severity"]
            .astype(str)
            .str.lower()
            == "mandatory"
        )
        &
        (
            ~validation["passed"]
        )
    ]

    checksum_table = pd.read_csv(
        CHECKSUM_FILE,
        low_memory=False
    )

    checksum_failures = []

    for row in checksum_table.to_dict(
        orient="records"
    ):
        relative_path = Path(
            row["relative_path"]
        )

        packaged_file = ROOT / relative_path

        if not packaged_file.exists():
            checksum_failures.append(
                f"Missing: {relative_path}"
            )
            continue

        observed_hash = sha256_file(
            packaged_file
        )

        expected_hash = str(
            row["sha256"]
        )

        if observed_hash != expected_hash:
            checksum_failures.append(
                f"Hash mismatch: {relative_path}"
            )

    assertions = {
        "validation_status_pass":
            manifest.get(
                "overall_validation_status"
            ) == "PASS",
        "total_reports_1500":
            manifest.get(
                "total_reports_evaluated"
            ) == 1500,
        "A4_quality_gates_300":
            manifest.get(
                "A4_quality_gate_passes"
            ) == 300,
        "ground_truth_not_exposed":
            manifest.get(
                "ground_truth_exposed_to_llm"
            ) is False,
        "mandatory_failures_zero":
            len(mandatory_failures) == 0,
        "checksum_failures_zero":
            len(checksum_failures) == 0,
    }

    print("=" * 72)
    print("UNSW-NB15 REPRODUCIBILITY CHECK")
    print("=" * 72)

    for check_name, passed in assertions.items():
        print(
            f"{check_name:<34}: "
            f"{'PASS' if passed else 'FAIL'}"
        )

    if checksum_failures:
        print("\nChecksum problems:")

        for failure in checksum_failures:
            print(f"- {failure}")

    overall_pass = all(
        assertions.values()
    )

    print(
        "\nOVERALL STATUS:",
        "PASS" if overall_pass else "FAIL"
    )

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
