from pydantic import BaseModel
from typing import List,Optional

""" Request schemas
    Invoice data validation for invoice request
"""
class InvoiceRequest(BaseModel):
    invoice_id:str
    vendor_id: str
    vendor_name: str
    vendor_category: str
    po_reference:str
    po_amount : float
    invoice_amount : float
    gr_amount : float
    deviation_pct: float
    is_new_vendor : bool
    days_since_last_invoice:int
    three_way_match:bool
    invoice_date:str

class ExplainRequest(BaseModel):
    invoice: dict
    flags : list

class InvestigateResponse(BaseModel):
    invoice_id : str
    risk_level : str
    decision : str
    ml_score : float
    anomaly_flags : List[dict]
    explanation : str
    sar_report : Optional[str] = None
