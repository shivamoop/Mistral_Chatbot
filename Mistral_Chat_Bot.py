import os
import requests
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import serpapi
from serpapi import GoogleSearch
from tavily import TavilyClient
import streamlit as st
from requests.exceptions import RequestException
from uuid import uuid4
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='agent_logs.log', filemode='a')
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(os.environ["Tavily_API_KEY"])
serpapi_key = os.environ["SERPAPI_API_KEY"]
def search_web_serpapi(query):
    """Fetch web search results using SerpApi."""
    try:
        logger.debug(f"Searching SerpApi for query: {query}")
        params = {
            "engine": "google",
            "q": query,
            "api_key": serpapi_key,
            "num": 3
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        if not organic_results:
            return []
        references = []
        for result in organic_results[:3]:
            references.append({
                "title": result.get("title", "No title"),
                "link": result.get("link", "No link"),
                "snippet": result.get("snippet", "No snippet")
            })
        return references
    except RequestException as e:
        logger.error(f"SerpApi network error: {str(e)}")
        return [{"title": "Error", "link": "", "snippet": f"Network error while fetching SerpApi references: {str(e)}"}]
    except ValueError as e:
        logger.error(f"SerpApi configuration error: {str(e)}")
        return [{"title": "Error", "link": "", "snippet": f"Invalid SerpApi key or configuration: {str(e)}"}]
    except Exception as e:
        logger.error(f"SerpApi unexpected error: {str(e)}")
        return [{"title": "Error", "link": "", "snippet": f"Unexpected error fetching SerpApi references: {str(e)}"}]

def search_web_tavily(query):
    """Fetch web search results using Tavily."""
    try:
        logger.debug(f"Searching Tavily for query: {query}")
        response = tavily_client.search(query, max_results=3)
        results = response.get("results", [])
        if not results:
            return []
        references = []
        for result in results:
            references.append({
                "title": result.get("title", "No title"),
                "link": result.get("url", "No link"),
                "snippet": result.get("content", "No snippet")
            })
        return references
    except Exception as e:
        logger.error(f"Tavily error: {str(e)}")
        return [{"title": "Error", "link": "", "snippet": f"Error fetching Tavily references: {str(e)}"}]

def combine_search_results(query):
    """Combine and deduplicate results from SerpApi and Tavily."""
    serpapi_results = search_web_serpapi(query)
    tavily_results = search_web_tavily(query)
    all_results = serpapi_results + tavily_results
    seen_links = set()
    deduplicated_results = []
    for result in all_results:
        link = result["link"]
        if link and link not in seen_links:
            deduplicated_results.append(result)
            seen_links.add(link)
    if not deduplicated_results:
        return "No references found for the query."
    return "\n".join([f"- [{r['title']}]({r['link']}): {r['snippet']}" for r in deduplicated_results])
def ollama_react_agent(query, chat_history='', max_iterations=3, simplify=True):
    """ReAct agent with simplified mode, using both SerpApi and Tavily."""
    try:
        llm = Ollama(model="mistral", base_url="http://34.46.52.66:11434")
        logger.debug(f"Initialized Ollama with model: mistral")
        
        react_prompt = PromptTemplate(
            input_variables=["query", "chat_history"],
            template="""
            You are a helpful assistant answering queries in a structured manner.
            Use the chat history to maintain context (e.g., location, budget).
            You have access to two search APIs:
            - SerpApi: For detailed Google search results.
            - Tavily: For concise, AI-optimized search results.
            Choose the appropriate API based on the query:
            - Use Tavily for factual, concise answers (e.g., 'What is the capital of France?').
            - Use SerpApi for detailed SERP data (e.g., 'Compare iPhone 15 and Samsung Galaxy S24').
            - Combine both for complex queries (e.g., itineraries).
            Generate a response in markdown format as a continuous text, starting with a brief summary (1-2 sentences) followed by detailed information.
            - For itineraries, include a day-wise plan with activities, times, and costs, and a budget breakdown.
            - For comparisons, list key specs, pros, and cons for each item.
            - Do not include references in the response; references will be appended separately.
            - Do not include internal reasoning steps (e.g., Thought, Action, Observation).
            - Avoid adding section titles like 'Query,' 'Summary,' or 'Key Information or Results.'
            
            Query: {query}
            Chat History: {chat_history}
            """
        )
        chain = LLMChain(llm=llm, prompt=react_prompt)
        logger.debug(f"Initialized LLMChain with prompt: {react_prompt.template[:100]}...")

        if simplify:
            # Simplified mode: Single LLMChain call
            logger.debug("Running in simplified mode")
            run_id = str(uuid4())
            logger.debug(f"Generated run_id: {run_id}")
            # Determine which API to use based on query type
            if "compare" in query.lower() or "vs" in query.lower():
                references = search_web_serpapi(query)
                references = "\n".join([f"- [{r['title']}]({r['link']}): {r['snippet']}" for r in references]) if references else "No references found."
            elif "itinerary" in query.lower() or "plan" in query.lower():
                references = combine_search_results(query)
            else:
                references = search_web_tavily(query)
                references = "\n".join([f"- [{r['title']}]({r['link']}): {r['snippet']}" for r in references]) if references else "No references found."
            response = chain.run(query=query, chat_history=chat_history, run_id=run_id)
            logger.debug(f"Simplified response: {response}")
            return f"{response}\n\n**References**:\n{references}"

        # Full ReAct loop
        current_query = query
        iteration = 0
        while iteration < max_iterations:
            logger.debug(f"Iteration {iteration + 1}: Running chain with query: {current_query}, chat_history: {chat_history}")
            run_id = str(uuid4())
            logger.debug(f"Generated run_id: {run_id}")
            response = chain.run(query=current_query, chat_history=chat_history, run_id=run_id)
            logger.debug(f"Response: {response}")

            evaluation_prompt = PromptTemplate(
                input_variables=["query", "response", "chat_history"],
                template="""
                Evaluate if the response fully answers the query in a structured, clear, and concise manner,
                respecting the chat history (e.g., location, budget).
                For itineraries, check for day-wise plans and budget details.
                For comparisons, check for specs, pros, and cons.
                If not, suggest a refined query.
                Query: {query}
                Response: {response}
                Chat History: {chat_history}
                """
            )
            evaluation_chain = LLMChain(llm=llm, prompt=evaluation_prompt)
            evaluation_run_id = str(uuid4())
            logger.debug(f"Evaluation run_id: {evaluation_run_id}")
            evaluation = evaluation_chain.run(query=current_query, response=response, chat_history=chat_history, run_id=evaluation_run_id)
            logger.debug(f"Evaluation: {evaluation}")

            if "fully answers" in evaluation.lower() or "fully addresses" in evaluation.lower():
                references = combine_search_results(current_query)
                return f"{response}\n\n**References**:\n{references}"

            refine_prompt = PromptTemplate(
                input_variables=["query", "evaluation", "chat_history"],
                template="""
                Suggest a refined query to improve the response's structure and completeness,
                respecting the chat history (e.g., location, budget).
                Original Query: {query}
                Evaluation: {evaluation}
                Chat History: {chat_history}
                """
            )
            refine_chain = LLMChain(llm=llm, prompt=refine_prompt)
            refine_run_id = str(uuid4())
            logger.debug(f"Refine run_id: {refine_run_id}")
            current_query = refine_chain.run(query=current_query, evaluation=evaluation, chat_history=chat_history, run_id=refine_run_id)
            logger.debug(f"Refined Query: {current_query}")
            iteration += 1

        references = combine_search_results(current_query)
        return f"{response}\n\n**References**:\n{references}"

    except Exception as e:
        logger.error(f"Error in ollama_react_agent: {str(e)}")
        return f"Error processing query: {str(e)}"
# Set page configuration
st.set_page_config(page_title="Mistral Chatbot", page_icon="🤖")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm powered by Mistral. Ask me to compare smartphones, plan a trip, or anything else, and I'll provide a clear, structured response with references."}]

# Display title
st.title("Mistral Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("Thinking..."):
            chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages[:-1]])
            logger.debug(f"User prompt: {prompt}")
            logger.debug(f"Chat history: {chat_history}")
            response = ollama_react_agent(prompt, chat_history=chat_history, max_iterations=3, simplify=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    except Exception as e:
        logger.error(f"Error in Streamlit handler: {str(e)}")
        error_message = f"Oops, something went wrong: {str(e)}. Please try again or check your API keys."
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        with st.chat_message("assistant"):
            st.markdown(error_message)

# Sidebar with instructions and debug options
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot uses:
    - **Streamlit**: For the chat interface
    - **Ollama (Mistral)**: For local Mistral processing
    - **SerpApi**: For detailed Google search results
    - **Tavily**: For AI-optimized search results
    - **LangChain**: For structured responses and ReAct reasoning
    
    Enter your query below to get a clear, structured answer with references.
    """)
    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm powered by Mistral. Ask me anything!"}]
        st.experimental_rerun()
