from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage

from state import AgentState
from tools.retrieve_similar_cases import retrieve_similar_cases
from tools.fetch_vendor_history import fetch_vendor_history
from tools.cross_reference_po import cross_reference_po
from tools.generate_sar_report import generate_sar_report

# Bind tools to LLM to make it agentic
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools([
    retrieve_similar_cases,
    fetch_vendor_history,
    cross_reference_po,
    generate_sar_report
])

def investigate_deep_node(state : AgentState) -> AgentState:

    invoice = state["invoice"]
    flags = state["anomaly_flags"]
    flag_names = [f["anomaly_type"] for f in flags]

    # Initial prompt — LLM reads this and decides what to do first
    prompt = f"""
    You are a financial fraud investigator. Investigate this invoice and 
    produce a SAR report.

    Invoice details:
    {invoice}

    Anomalies already detected: {flag_names}
    ML fraud score: {state['ml_score']:.2f}

    Use the available tools to gather evidence, then call generate_sar_report 
    with everything you found. Call generate_sar_report LAST.
    """
    # Every message must be tagged as one of:

       # HumanMessage — the user/investigator speaking
       # AIMessage — the LLM's response (LangChain adds this automatically)
       # ToolMessage — the result returned by a tool
    
    messages = [HumanMessage(content = prompt)]

    # Agentic loop — runs until LLM stops calling tools
    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # If no tool calls, LLM is done
        if not response.tool_calls:
            break
        # Run each tool the LLM requested
        for tool_call in response.tool_calls :
            
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Route to the correct tool
            if tool_name == "retrieve_similar_cases" :
                result = retrieve_similar_cases.invoke(tool_args)
            elif tool_name == "fetch_vendor_history":
                result = fetch_vendor_history.invoke(tool_args)
            elif tool_name == "cross_reference_po":
                result = cross_reference_po.invoke(tool_args)
            elif tool_name == "generate_sar_report":
                result = generate_sar_report.invoke(tool_args)

                state["sar_report"] = result
        
            # Feed result back to LLM
            messages.append(ToolMessage(
                content = str(result),
                tool_call_id = tool_call["id"]
            ))

    state["decision"] = "sar_generated"
    state["explanation"] = "Deep investigation complete. SAR report generated."
    return state