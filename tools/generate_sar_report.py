from langchain_core.tools import tool
# langchain_openai is a LangChain wrapper that enables bind_tools()
# which is the one method that makes the LLM aware of your tools and able to call them.
from langchain_openai import ChatOpenAI

# temperature=0 — deterministic, always picks the most likely next word. 
# What we want for fraud investigation — consistent, factual, no hallucination.
# temperature=1 — creative, random. Good for writing - not SAR reports
llm = ChatOpenAI(model = "gpt-4o",temperature=0)

@tool
def generate_sar_report(investigation_summary : str) -> str:

    """
    Generate a formal Suspicious Activity Report (SAR) based on the 
    completed investigation. 
    Call this LAST, only after we have gathered evidence from other tools. 
    Input should be a  summary of everything we found during the investigation.

    """

    prompt =  f"""You are a compliance officer writing a Suspicious Activity Report (SAR) for FinCEN.
 
    STRICT FORMAT RULES — you MUST follow these exactly:
    - Start each section with "=== SECTION TITLE" on its own line (the === and title on the SAME line)
    - Use "- " (dash space) at the start of each bullet point
    - Each bullet must be on its own line
    - Never run sections together in one paragraph
    - Never repeat invoice details (vendor name, ID, amounts, dates) — those are shown separately
    - Never use markdown bold (**) or any other markdown formatting
    - Do NOT include a Subject Information section — invoice data is displayed elsewhere
    
    Write the report using this EXACT structure:
    
    === SUSPICIOUS ACTIVITY
    [2-3 sentences on separate lines describing what was detected and why it is suspicious.]
    
    === EVIDENCE SUMMARY
    - [Finding 1 label]: [detailed explanation]
    - [Finding 2 label]: [detailed explanation]
    - [Finding 3 label]: [detailed explanation]
    - [Finding 4 label]: [detailed explanation]
    
    === RISK ASSESSMENT
    - Severity Level: [HIGH / MEDIUM / LOW]
    - Confidence Level: [HIGH / MEDIUM / LOW]
    - ML Fraud Score: [score]
    [1-2 sentences explaining the risk assessment rationale on separate lines.]
    
    === RECOMMENDED ACTION
    - [Action 1]
    - [Action 2]
    - [Action 3]
    
    Investigation findings:
    {investigation_summary}
    
    Write in formal regulatory language. Be specific with amounts and dates. Follow the structure EXACTLY. Do NOT add any sections beyond the four listed above."""    
    response = llm.invoke(prompt)
    return response.content