import pandas as pd
from langchain_core.tools import tool

df = pd.read_csv("data/p2p_invoices.csv")

@tool
def cross_reference_po(po_reference : str) -> str:
    """
        Cross-reference a purchase order to validate whether the invoice 
        amount is consistent with the authorized PO amount. 
        Use this when overbilling is suspected or when you need to confirm what amount 
        was originally approved.
        Input should be the po_reference string from the invoice.
    """

    po_matches = df[df["po_reference"] == po_reference]

    if po_matches.empty:
        return f"PO {po_reference} not found in system. This may indicate a fictitious purchase order."
    
    # take the matching record
    po_match_data = po_matches.iloc[0]
    po_amount = po_match_data["po_amount"]
    invoice_amount = po_match_data["invoice_amount"]
    deviation_pct = po_match_data["deviation_pct"]
    vendor_name = po_match_data["vendor_name"]
    vendor_category = po_match_data["vendor_category"]

    if invoice_amount > po_amount:
        status = f"OVERBILLED by ${invoice_amount - po_amount:,.2f} ({deviation_pct:.1f}% over PO)"

    elif invoice_amount == po_amount:
        status = "Invoice matches PO exactly — no overbilling detected"
    
    else:
        status = f"Invoice is UNDER PO amount by ${po_amount - invoice_amount:,.2f}"
    
    return (
        f"PO {po_reference}: vendor={vendor_name}, category={vendor_category}, "
        f"authorized=${po_amount:,.2f}, invoiced=${invoice_amount:,.2f}. "
        f"Status: {status}"
    )