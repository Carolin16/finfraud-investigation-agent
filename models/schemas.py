from pydantic import BaseModel

"""
    Invoice data validation for invoice request
"""
class InvoiceRequest(BaseModel):
    invoice_id:str
    vendor_id: str
    amount : float
    po_amount : float
    gr_amount : float
    is_new_vendor : bool
    days_since_last_invoice:int