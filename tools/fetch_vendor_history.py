import pandas as pd
from langchain_core.tools import tool

df = pd.read_csv("data/p2p_invoices.csv")

@tool
def fetch_vendor_history(vendor_id : str) -> str:
    """
    Fetch the transaction history for a specific vendor from the 
    internal payment database. Use this to check if a vendor has 
    prior fraud incidents, unusual payment patterns, or no history 
    at all. Input should be the vendor_id string from the invoice.
    """
    history = df[df["vendor_id"] == vendor_id]
    if history.empty:
        return f"No transaction history found for vendor {vendor_id}.Vendor may be new or fictitious."
    
    summary = {
        "total_invoices": len(history),
        "total_amount": history["invoice_amount"].sum(),
        "avg_amount": history["invoice_amount"].mean(),
        "prior_fraud_count": history["is_anomaly"].sum()  if "is_anomaly" in history.columns else "unknown"
    }
    
    return (
        f"Vendor {vendor_id} history: "
        f"{summary['total_invoices']} invoices, "
        f"total ${summary['total_amount']:,.2f}, "
        f"avg ${summary['avg_amount']:,.2f}, "
        f"prior anomalies: {summary['prior_fraud_count']}"
    )