from fastapi import FastAPI
from pydantic import BaseModel
from models.schemas import InvoiceRequest,ExplainRequest
from orchestrator.anomaly_orchestrator import AnomalyOrchestrator
from detectors.duplicate_detector import DuplicateDetector
from detectors.new_vendor_risk_detector import NewVendorRiskDetector
from detectors.overbilling_detector import OverbillingDetector
from detectors.phantom_delivery_detector import PhantomDeliveryDetector
from rag import RAGExplainer
import joblib
import numpy as np

#load pickle file
model = joblib.load("models/random_forest.joblib")
ragExplainer = RAGExplainer()
fraudDetectors = AnomalyOrchestrator([DuplicateDetector(),NewVendorRiskDetector(),OverbillingDetector(),PhantomDeliveryDetector()])
app = FastAPI()

@app.get("/")
def hello():
    return {"message" : "Hello"}

@app.post("/invoice")
def invoice(invoice_data:InvoiceRequest):

    invoiceData = {"invoice_id" : invoice_data.invoice_id,
            "vendor_id" : invoice_data.vendor_id,
            "invoice_amount" : invoice_data.invoice_amount,
            "po_amount" : invoice_data.po_amount,
            "gr_amount" : invoice_data.gr_amount,
            "is_new_vendor" : invoice_data.is_new_vendor,
            "days_since_last_invoice": invoice_data.days_since_last_invoice}

    #training features 
    features = [[
        invoice_data.po_amount,
        invoice_data.invoice_amount, 
        invoice_data.gr_amount,
        invoice_data.deviation_pct,
        invoice_data.days_since_last_invoice,
        invoice_data.is_new_vendor, 
        invoice_data.three_way_match
    ]]    
    
    ml_score = round(float(model.predict_proba(features)[0][1]),4)

    results = fraudDetectors.run(invoiceData)
    if results:
        anomaly = True
    
    else:
        anomaly = False
    
    invoiceData["anomaly"] = anomaly
    invoiceData["flags"] = results
    invoiceData["status"] = "received"
    invoiceData["ml_score"] = ml_score
    return invoiceData

@app.post("/explain")
def explain_invoice(request:ExplainRequest):
    print("explain endpoint hit")        # ← add this
    explanation = ragExplainer.explain(

        invoice = request.invoice,
        flags = request.flags
    )

    return {

        "explanation" : explanation
    }