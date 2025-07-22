# Mistral Chatbot

A ReAct-style AI agent built with LangChain, Ollama, SerpAPI, and Tavily for answering queries with structured responses and web search integration. This chatbot is designed to handle free-text queries, integrate multiple tools, and provide user-friendly outputs with references, as part of an AI Agent Engineer interview task.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Install Python**:
   - Ensure Python 3.8+ is installed. Verify with:
     ```powershell
     python --version
     ```

3. **Install Dependencies**:
   - Create a virtual environment and install required packages:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```

4. **Set Up Ollama**:
 - Follow the [Ollama installation guide](https://ollama.ai/) for your operating system.
   - Pull the Mistral model:
     ```powershell
     ollama pull mistral
     ```
     ```powershell
     Start-Process ollama -ArgumentList "run mistral" -NoNewWindow
     ```

5. **Configure Environment Variables**:
   - Create a `.env` file in the project directory:
     ```
     SERPAPI_API_KEY=your-serpapi-key
     TAVILY_API_KEY=your-tavily-key
     ```
   - Alternatively, set in PowerShell:
     ```powershell
     $env:SERPAPI_API_KEY = "your-serpapi-key"
     $env:TAVILY_API_KEY = "your-tavily-key"
     ```
   - Obtain API keys from [SerpAPI](https://serpapi.com) and [Tavily](https://tavily.com).

6. **Run the App**:
   - Activate the virtual environment and start the Streamlit app:
     ```powershell
     .\venv\Scripts\Activate.ps1
     streamlit run mistral_chatbot.py
     ```
   - Open your browser at `http://localhost:8501` to use the chatbot.

## Usage Instructions

- **Interface**: The chatbot runs in a browser with a chat input field at the bottom. Enter a query and press Enter to receive a response.
- **Example Queries**:
  - "Plan a 2-day itinerary for Delhi with a ₹5,000 budget per person for 2-3 people in mid-December."
  - "Compare the top 3 smartphones under ₹20,000 in India."
  - "Summarize the latest Indian income tax updates for 2023."
- **Features**:
  - Responses include a brief summary, key information (e.g., itinerary or comparison details), and references from SerpAPI and Tavily.
  - Use the sidebar "Clear Chat History" button to reset the conversation.
- **Notes**: Ensure the Ollama server is running and API keys are valid before querying.

## Demo

### Demo 1: 2-Day Itinerary for Delhi
**Query**: "Plan a 2-day itinerary for Delhi with a ₹5,000 budget per person for 2-3 people in mid-December."

**Response**:
<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/5e312da5-874e-4043-9314-22b4a9a3f25e" />

### Demo 2: Compare Smartphones Under ₹20,000
**Query**: "Compare the top 3 smartphones under ₹20,000 in India."

**Response**:

<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/0780482f-eaeb-4c04-9f5c-6cee20b24118" />


## Notes
- **SerpApi Key & Tavily key**: Ensure the `SERPAPI_API_KEY` and `TAVILY_API_KEY` environment variable is set, or web search functionality will fail.
- **Ollama Setup**: The Mistral model must be available via Ollama for local inference.
- **Performance**: Response time depends on the local machine's hardware and Ollama's performance. For faster responses, consider using a GPU-enabled setup with Ollama.
- **Limitations**: The chatbot currently supports a maximum of one iteration for response refinement. Adjust `max_iterations` in `ollama_react_agent` for more complex queries if needed.

## Troubleshooting
- **SerpApi Error**: If you see "Error: SERPAPI_API_KEY not set in environment," ensure the API key is correctly set.
- **Tavily Error**: If you see "Error: TAVILY_API_KEY not set in environment," ensure the API key is correctly set.
- **Ollama Not Found**: Verify that Ollama is installed and the `mistral` model is pulled (`ollama list` to check).
- **Streamlit Issues**: Ensure all dependencies are installed correctly. Run `pip install -r requirements.txt` again if errors occur.


## Requirements

- **Python**: 3.8+
- **Ollama**: With Mistral model
- **API Keys**: SerpAPI and Tavily API keys
- **Environment**: Windows PowerShell (or compatible terminal)

## Notes

- Tested on July 23, 2025, at 04:31 AM IST.
- Ensure the Ollama server remains running during app execution.
- Check PowerShell logs for debugging if issues arise.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or support, please open an issue on the repository or contact the maintainer.
