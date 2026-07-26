from dotenv import load_dotenv
load_dotenv()

import uuid
from typing import Literal

import streamlit as st
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_youdotcom import YouSearchTool

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

# ======================================================
# Streamlit Config
# ======================================================

st.set_page_config(
    page_title="LangGraph Multi Agent",
    page_icon="🤖",
    layout="wide"
)

# ======================================================
# LLM
# ======================================================

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile"
)

# ======================================================
# State
# ======================================================

from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class FlowState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    category: Literal["coding", "wheather", "google_search"] = "google_search"
    answer: str = Field(default="")


class QuestionCategory(BaseModel):

    category: Literal[
        "coding",
        "wheather",
        "google_search"
    ] = Field(
        default="google_search",
        description="Question Category"
    )

# ======================================================
# Search Tool
# ======================================================

search = YouSearchTool()

google_agent = create_agent(
    model=llm,
    tools=[search],
    system_prompt="""
You are an intelligent search assistant.

Whenever user asks anything that requires
latest information,
facts,
people,
companies,
news,
history,
general knowledge,
or internet search,

always use the search tool.

Give clean and detailed answers.
"""
)

# ======================================================
# Weather Tool
# ======================================================

import requests
import os

@tool
def get_weather(city: str) -> str:
    """
    Get real-time weather information for a city.
    """

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(url, params=params)

        data = response.json()

        if response.status_code != 200:

            return f"❌ Error: {data.get('message', 'Unable to fetch weather')}"

        weather = data["weather"][0]["description"].title()

        temp = data["main"]["temp"]

        feels = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]

        wind = data["wind"]["speed"]

        city_name = data["name"]

        country = data["sys"]["country"]

        return f"""
🌍 Location: {city_name}, {country}

🌤 Weather: {weather}

🌡 Temperature: {temp}°C

🤗 Feels Like: {feels}°C

💧 Humidity: {humidity}%

💨 Wind Speed: {wind} m/s
"""

    except Exception as e:

        return f"Error: {str(e)}"
weather_agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="""
You are a weather assistant.

Always use the get_weather tool whenever the user asks about weather.

Never answer from your own knowledge.

Always call the tool.
"""
)


weather_agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="""
You are a weather assistant.

Always use the get_weather tool whenever the user asks about weather.

Never answer from your own knowledge.

Always call the tool.
"""
)
# ======================================================
# Sidebar
# ======================================================

with st.sidebar:

    st.title("🤖 LangGraph")

    st.markdown("---")

    st.write("### Supported Agents")

    st.success("💻 Coding")

    st.info("🌦 Weather")

    st.warning("🔍 Google Search")

    st.markdown("---")

    st.write("Built with")

    st.write("• Streamlit")

    st.write("• LangGraph")

    st.write("• LangChain")

    st.write("• Groq")



# ======================================================
# Question Categorization Node
# ======================================================

def question_category(state: FlowState):

    structured = llm.with_structured_output(QuestionCategory)

    last_question = state.messages[-1].content

    response = structured.invoke(
        f"""
Categorize this question:

{last_question}

coding
wheather
google_search

If unsure return google_search.
"""
    )

    state.category = response.category

    return state

# ======================================================
# Router
# ======================================================

def route(state: FlowState):

    return state.category


# ======================================================
# Coding Node
# ======================================================


def coding_node(state: FlowState):

    response = llm.invoke(state.messages)

    state.messages.append(
        AIMessage(content=response.content)
    )

    return state


# ======================================================
# Weather Node
# ======================================================

def weather_node(state: FlowState):

    response = weather_agent.invoke(
        {
            "messages": state.messages
        }
    )

    answer = response["messages"][-1]

    state.messages.append(answer)

    return state


# ======================================================
# Google Search Node
# ======================================================

def google_search_node(state: FlowState):

    response = google_agent.invoke(
        {
            "messages": state.messages
        }
    )

    answer = response["messages"][-1]

    state.messages.append(answer)

    return state

# ======================================================
# Build LangGraph
# ======================================================

graph = StateGraph(FlowState)

graph.add_node(
    "check_question",
    question_category
)

graph.add_node(
    "coding",
    coding_node
)

graph.add_node(
    "wheather",
    weather_node
)

graph.add_node(
    "google_search",
    google_search_node
)

graph.add_edge(
    START,
    "check_question"
)

graph.add_conditional_edges(
    "check_question",
    route
)

graph.add_edge(
    "coding",
    END
)

graph.add_edge(
    "wheather",
    END
)

graph.add_edge(
    "google_search",
    END)


# ======================================================
# Memory
# ======================================================

memory = InMemorySaver()

workflow = graph.compile(
    checkpointer=memory
)


# ======================================================
# Streamlit Dashboard
# ======================================================

st.title("🤖 LangGraph Multi-Agent Assistant")
st.caption("Coding • Weather • Google Search")

st.markdown("---")

# ======================================================
# Session State
# ======================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# ======================================================
# Sidebar Controls
# ======================================================

with st.sidebar:

    st.markdown("---")

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# ======================================================
# Display Previous Chat
# ======================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "assistant":

            if message.get("category"):

                category = message["category"]

                if category == "coding":
                    st.success(f"Category : {category}")

                elif category == "wheather":
                    st.info(f"Category : {category}")

                else:
                    st.warning(f"Category : {category}")

        st.markdown(message["content"])

# ======================================================
# Chat Input
# ======================================================

question = st.chat_input("Ask me anything...")

if question:

    # -----------------------------
    # User Message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # -----------------------------
    # Invoke Graph
    # -----------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            config = {
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            }
            result = workflow.invoke(
                {
                    "messages": [
                        HumanMessage(content=question)
                    ]
                },
                config=config
            )
        answer = result["messages"][-1].content
        category = result["category"]

        # Category Badge

        if category == "coding":
            st.success(f"💻 Category : {category}")

        elif category == "wheather":
            st.info(f"🌦 Category : {category}")

        else:
            st.warning(f"🔍 Category : {category}")

        st.markdown(answer)

    # -----------------------------
    # Save Assistant Message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "category": category
        }
    )