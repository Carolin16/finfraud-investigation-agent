from fastapi import FastAPI
from pydantic import BaseModel

from models.schemas import InvoiceRequest,ExplainRequest,InvestigateResponse
from orchestrator.anomaly_orchestrator import AnomalyOrchestrator
from detectors.duplicate_detector import DuplicateDetector
from detectors.new_vendor_risk_detector import NewVendorRiskDetector
from detectors.overbilling_detector import OverbillingDetector
from detectors.phantom_delivery_detector import PhantomDeliveryDetector

from rag import RAGExplainer
from agent import agent

import joblib
import numpy as np
import threading

# load pickle file
model = joblib.load("models/random_forest.joblib")

# lazy loading on endpoint hit
rag_ready = threading.Event()
ragExplainer = None

def _warm_rag():
    global ragExplainer
    # loads BERT + encodes cases + docs
    ragExplainer = RAGExplainer()  
    # signal RAG ready
    rag_ready.set()  
    print("[RAG] Pre-warm complete")

# Kick off on startup — server is live immediately, RAG loads in parallel
threading.Thread(target=_warm_rag, daemon=True).start()

def get_rag():
    # blocks only if someone calls before it's done
    rag_ready.wait()  
    return ragExplainer

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

    explanation = get_rag().explain(

        invoice = request.invoice,
        flags = request.flags
    )

    return {

        "explanation" : explanation
    }

@app.post("/investigate",response_model=InvestigateResponse)
def investigate(invoice_data : InvoiceRequest):

    invoice_dict = invoice_data.model_dump()
    # initalise state
    initial_state = {
        
        "invoice" : invoice_dict,
        "anomaly_flags" : [],
        "ml_score" : 0.0,
        "risk_level" : "",
        "decision" : "",
        "similar_cases" : [],
        "sar_report" : None,
        "explanation" : ""
    }

    result = agent.invoke(initial_state)

    # return response
    return InvestigateResponse(
        invoice_id=invoice_data.invoice_id,
        risk_level=result["risk_level"],
        decision=result["decision"],
        ml_score=result["ml_score"],
        anomaly_flags=result["anomaly_flags"],
        explanation=result["explanation"],
        sar_report=result.get("sar_report")
    )