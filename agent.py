from langgraph.graph import StateGraph , END
from state import AgentState

#import all nodes
from nodes.validate_node import validate_invoice
from nodes.detect_node import detect_anomalies
from nodes.get_ml_score_node import get_ml_score
from nodes.decide_risk_node import decide_risk_node

from nodes.auto_approve_node import auto_approve
from nodes.flag_for_review_node import flag_for_review
from nodes.investigate_deep_node import investigate_deep_node

# Router function (reads state, returns a string)
def route_by_risk(state : AgentState) -> str:

    return state["risk_level"]

# Build the graph
def build_agent():

    # Create the graph, tell it what state looks like
    graph = StateGraph(AgentState)

    # Register all nodes
    graph.add_node("validate_invoice", validate_invoice)
    graph.add_node("detect_anomalies", detect_anomalies)
    graph.add_node("get_ml_score", get_ml_score)
    graph.add_node("decide_risk_node", decide_risk_node)
    
    graph.add_node("auto_approve", auto_approve)
    graph.add_node("flag_for_review", flag_for_review)
    graph.add_node("investigate_deep", investigate_deep_node)
    
    # Make edges
    graph.set_entry_point("validate_invoice")
    graph.add_edge("validate_invoice", "detect_anomalies")
    graph.add_edge("detect_anomalies", "get_ml_score")
    graph.add_edge("get_ml_score", "decide_risk_node")

    # Conditional edge (router decides which branch)
    graph.add_conditional_edges(

        "decide_risk_node", # from this node
        route_by_risk, # call this function to get the route
        {
            "HIGH" : "investigate_deep", # if returns "HIGH" go here
            "MEDIUM" : "flag_for_review",
            "LOW" : "auto_approve"
        }
    )

    # All branches end the graph
    graph.add_edge("auto_approve" , END)
    graph.add_edge("flag_for_review" , END)
    graph.add_edge("investigate_deep" , END)

    # Compile and return
    return graph.compile()

agent = build_agent()