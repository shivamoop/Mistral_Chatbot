# Llama 3 Chatbot

## Overview
This project is a Streamlit-based chatbot powered by Llama 3 (via Ollama), LangChain, and SerpApi. It uses the ReAct (Reason + Act) framework to handle a variety of user queries, including product recommendations, financial calculations, summarization, and comparisons. The chatbot provides structured responses with web-sourced references and maintains chat history for contextual follow-up questions.

## Features
- **Intent Classification**: Automatically identifies query types (e.g., summarization, math, code, itinerary, product recommendations).
- **Web Search Integration**: Uses SerpApi to fetch relevant references from Google search results.
- **Structured Responses**: Delivers clear, formatted outputs with optional comparison tables for queries like product or policy comparisons.
- **Chat History**: Maintains context for follow-up questions using Streamlit's session state.
- **Local LLM Processing**: Uses Ollama with the Mistral model for local inference, ensuring privacy and control.
- **Supported Query Types**:
  - eCommerce product recommendations (e.g., phones, appliances, air conditioners)
  - Financial calculations (e.g., discounts, taxes, totals)
  - Taxation queries (e.g., VAT, import/export tax)
  - Summarization (e.g., reviews, policies)
  - Comparisons (e.g., products, tax rates, platforms)

## Prerequisites
- Python 3.8+
- A valid [SerpApi API key](https://serpapi.com/) for web search functionality
- Ollama installed locally with the `mistral` model pulled
- Required Python packages (see `requirements.txt`)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama**:
   - Follow the [Ollama installation guide](https://ollama.ai/) for your operating system.
   - Pull the Mistral model:
     ```bash
     ollama pull mistral
     ```

5. **Set Environment Variables**:
   - Set your SerpApi API key:
     ```bash
     export SERPAPI_API_KEY='your-api-key'  # On Windows: set SERPAPI_API_KEY=your-api-key
     ```

## Usage
1. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
   This will launch the chatbot in your default web browser.

2. **Interact with the Chatbot**:
   - Enter queries in the chat input box (e.g., "Compare iPhone 15 and Samsung Galaxy S23", "Summarize Amazon's return policy", or "Calculate total cost of a $500 item with 20% VAT").
   - The chatbot will process the query, classify its intent, and provide a structured response with web references if applicable.
   - Chat history is maintained for contextual follow-ups.

3. **Sidebar Information**:
   - The sidebar provides details about the technologies used (Streamlit, Ollama, SerpApi, LangChain).

## File Structure
- `app.py`: Main application file containing the chatbot logic, Streamlit interface, and ReAct agent implementation.
- `requirements.txt`: List of Python dependencies.
- `README.md`: This file.

## Dependencies
Listed in `requirements.txt`:
```
streamlit
langchain
langchain_community
serpapi
sentence-transformers
faiss-cpu
numpy
```

## Example Queries
- **Product Recommendation**: "Find the best smartphones under $500."
- **Financial Calculation**: "What is the final price of a $120 item after 20% VAT and 10% discount?"
- **Summarization**: "Summarize Amazon's return policy in 3 bullet points."
- **Comparison**: "Compare sales tax in California vs New York for online goods."
- **Code Assistance**: "How do I write a Python loop to sum numbers?"

## Notes
- **SerpApi Key**: Ensure the `SERPAPI_API_KEY` environment variable is set, or web search functionality will fail.
- **Ollama Setup**: The Mistral model must be available via Ollama for local inference.
- **Performance**: Response time depends on the local machine's hardware and Ollama's performance. For faster responses, consider using a GPU-enabled setup with Ollama.
- **Limitations**: The chatbot currently supports a maximum of one iteration for response refinement. Adjust `max_iterations` in `ollama_react_agent` for more complex queries if needed.

## Troubleshooting
- **SerpApi Error**: If you see "Error: SERPAPI_API_KEY not set in environment," ensure the API key is correctly set.
- **Ollama Not Found**: Verify that Ollama is installed and the `mistral` model is pulled (`ollama list` to check).
- **Streamlit Issues**: Ensure all dependencies are installed correctly. Run `pip install -r requirements.txt` again if errors occur.
- **FAISS or Sentence Transformers Errors**: Ensure `faiss-cpu` and `sentence-transformers` are compatible with your Python version.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or support, please open an issue on the repository or contact the maintainer.