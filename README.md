# P2P Anomaly Detection with RAG-based Explanation

> Combining Machine Learning and Generative AI to make 
> invoice fraud explainable — not just detectable.

This project builds an AI system that automatically detects 
suspicious vendor invoices in a Procure-to-Pay (P2P) process 
and explains why they were flagged — in plain English. A machine 
learning model scans incoming invoices and scores them for risk. 
When a suspicious invoice is found, a RAG (Retrieval-Augmented 
Generation) pipeline searches through procurement policy documents 
and vendor contracts to find relevant context, then uses an LLM 
to generate a clear explanation with a recommended action. The 
result: an AP analyst spends 8 minutes resolving a flagged invoice 
instead of 2.5 hours.