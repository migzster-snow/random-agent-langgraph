from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph, START, END 
import random

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int
    message: str

def greeting_node(state: AgentState) -> AgentState:
    state['message'] = f"Hello {state['name']}."
    state['counter'] = 0
    state['message'] += " Here are some random numbers:"
    return state

def random_node(state: AgentState) -> AgentState:
    random_number = random.randint(1, 10)
    state['number'].append(random_number)
    state['message'] += f" {random_number}"
    state['counter'] += 1
    return state

def loop_condition(state: AgentState) -> AgentState:
    if state['counter'] < 5:
        return "loop"
    else:
        return "exit"
    
graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")
graph.add_conditional_edges(
    "random",
    loop_condition,
    {
        "loop": "random",
        "exit": END
    }
)

app = graph.compile()

result = app.invoke({"name": "Jonah", "number": [], "counter": 0})

print(result['message'])
# Hello Jonah. Here are some random numbers: 2 3 3 6 10