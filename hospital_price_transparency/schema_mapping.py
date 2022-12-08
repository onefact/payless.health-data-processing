import polars as pl
import csv
import requests
import json
import itertools
from pathlib import Path

PRICE_COLUMN_NAMES = ["charge", "price", "gross_charge"]

BILLING_CODE_TYPE_TO_COLUMN_NAMES = {
    "cpt": ["cpt"],
    "ndc": ["drug", "national_drug_code"],
    "hcpcs": ["hcpcs_code", "hcpcs"],
    "revenue_code": ["rc", "revenue-code", "revenue code"],
    "icd": ["icd", "icd_code"],
    "drg": ["drg_code", "drg", "drg-code"],
    "apr-drg": ["all_patients", "apr-drg"],
}

COLUMN_NAME_TO_BILLING_CODE = {
    sub_value: key
    for key, value in BILLING_CODE_TYPE_TO_COLUMN_NAMES.items()
    for sub_value in value
}

BILLING_CODE_COLUMN_NAMES = list(itertools.chain(*[v for _, v in BILLING_CODE_TYPE_TO_COLUMN_NAMES.items()]))


def read_data(filename: str) -> pl.DataFrame:
    """Reads hospital data from https://www.dolthub.com/repositories/onefact/paylesshealth/data/main"""
    df = pl.read_csv(filename, infer_schema_length=0)
    return df.with_column(pl.col("cdm_url").str.split("|")).explode("cdm_url")


def read_csv_header(url: str, num_rows: int) -> dict:
    """Read the header of a CSV file."""
    rows = []

    with requests.get(url, stream=True) as r:
        for idx, row in enumerate(r.raw):
            rows.append(row.decode())
            if idx > 5:
                break

    last_row = rows.pop()
    dialect = csv.Sniffer().sniff(last_row)
    records = csv.reader(rows, dialect)
    header = next(records)
    # print('headers', header)
    # for row in records:
    #     print(row)
    return header


def infer_schema_map(column_names: list) -> dict:
    """Compute the map from the source name to the target name for each column of a schema."""
    schema_map = {}
    for source_column_name in column_names:
        column_name = source_column_name.lower().strip()
        if any(billing_col_name in column_name for billing_col_name in BILLING_CODE_COLUMN_NAMES):
            schema_map[source_column_name] = "billing_code"
            # schema_map["billing_code_type"] = next(
            #     v for k, v in COLUMN_NAME_TO_BILLING_CODE.items() if k in source_name
            # )
        elif "descr" in column_name:
            target_name = "description"
        elif any(price_name in column_name for price_name in PRICE_COLUMN_NAMES):
            target_name = "total_charge"
        elif "proc" in column_name and "code" in column_name:
            target_name = "procedure_code"
        elif "code" in column_name:
            target_name = "unknown_code"
        else:
            target_name = "unknown_column"
        schema_map[source_column_name] = target_name
    return schema_map


def write_schema_map(schema_map: dict, out_file: Path) -> None:
    """Write a schema map to a file with readable formatting."""
    with open(out_file, "w") as f:
        f.write(json.dumps(schema_map, indent=2))
