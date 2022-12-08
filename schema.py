"""Schema for the Payless Health Data Standard.

References:

https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/in-network-rates#negotiated-price-object
"""
import pyarrow as pa

HOSPITAL_PRICE_TRANSPARENCY_SCHEMA = pa.schema(
    [
        ("total_charge", pa.float32()),  ## Total cost of a line item
        ("description", pa.string()),  ## Description of the item or service
        (  ## CMS Certification Number assigned by the Centers for Medicare & Medicaid Services (CMS) to every hospital that bills Medicare & Medicaid
            "ccn",
            pa.int32(),
        ),
        (  ## Employer Identification Number, assigned by Internal Revenue Service
            "ein",
            pa.int32(),
        ),
        (  ## See the references for allowed billing code types like CPT, DRG, ICD
            "billing_code_type",
            pa.string(),
        ),
        ("billing_code", pa.string()),  ## Code like CPT, DRG, ICD
        (  ## Negotiated price for the covered item or service
            "negotiated_rate",
            pa.float32(),
        ),
        (  ## Some billing code types allow for modifiers
            "billing_code_modifier",
            pa.string(),
        ),
    ]
)
