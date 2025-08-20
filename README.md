# Should I?
An example project to demonstrate an Agentic AI solution using the Google Agent Development Kit to retrieve and process useful informaiton from an external API.

## Introduction
A multi-agent system built on the Google Agent Development Kit. It uses weather information, astronomical data, and Google Search to give you advice on whether it's a good idea to do something or not. 

It is designed to demonstrate this common pattern:
- Chatbot clarifies the user's intent
- Once clarified, it is passed on to another agent to execute
- That agent uses a variety of tools to carry out the request, including external API calls

Things to observe:
 - The agent instructions themselves in agent.py are simple and high-level. The agent itself is given wide latitude to make decisions about how to carry out requests.
 - This is made possible, in part, by the verbose docstring annotations you'll see in the tools (functions) that call the Weather.com APIs. The agents read those docstrings to determine which tools to call. The functions themselves are just a few lines of code.




## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/shouldi.git
   cd shouldi
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   - Create a `.env` file by copying the example file:
     ```bash
     cp .env.example .env
     ```
   - **Get API Keys:**
     - **Gemini API Key:** Obtain your key from [Google AI Studio](https://aistudio.google.com/).
     - **WeatherAPI.com Key:** Sign up for a free account at [WeatherAPI.com](https://www.weatherapi.com/signup.aspx).
   - Open the `.env` file and add your API keys:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     WEATHER_API_KEY=your_weather_api_key_here
     ```

## Usage

Run the agent with the following command to launch the interactive runner:

```bash
adk run shouldi_agent
```

Once the runner starts, you will need to initiate the conversation. You can start by simply saying "hello".

### Example Prompts

Here are a few examples of prompts you can use to test the agent.

**Complete Prompts**

These prompts provide all the necessary information (activity, date, and location) for the agent to provide a direct answer.

* "Should I go hiking tomorrow in Boulder, Colorado?"
* "Is it a good idea to go to the beach this weekend in Malibu?"
* "Should I go stargazing tonight in Joshua Tree National Park?"

**Incomplete Prompts**

These prompts are missing some information. They demonstrate the agent's ability to ask clarifying questions to get the details it needs.

* "I want to go for a run tomorrow."
* "Should I go swimming in San Diego?"

**Complex Prompts**

This is a more complex query that requires the agent to find specific, real-world information and connect it to a weather forecast.

* "What are the chances the Pike's Peak Cog Railway will be closed this Thursday due to weather?"


## How It Works

This `agent.py` script defines a multi-agent system using the Google ADK framework to advise users on whether they should do a particular activity.

### Core Functionality

The script's primary purpose is to act as an advisor. A user can ask a question like, "Should I go hiking tomorrow in Boulder, Colorado?" and the agent system will use its tools to gather relevant information (weather, facts about the location, etc.) and provide a recommendation.

### The Agents

The system is composed of three distinct agents, each with a specific role:

1.  **`request_clarifier_agent` (The "Greeter" and "Information Gatherer"):**
    *   **Purpose:** This is the user-facing agent. It's the first one to be invoked.
    *   **Function:** Its job is to chat with the user to gather the three essential pieces of information:
        1.  The **activity** the user wants to do (e.g., hiking, swimming, stargazing).
        2.  The **time** when they want to do it (e.g., "tomorrow", "this weekend", "tonight").
        3.  The **location** where they want to do it (e.g., "Boulder, Colorado", "the local pool").
    *   **Process:** It will continue the conversation until it has this information, confirm it with the user, and then pass a summary to the `should_i_agent`.

2.  **`should_i_agent` (The "Decision Maker"):**
    *   **Purpose:** This agent takes the clarified request from the `request_clarifier_agent` and determines the final advice.
    *   **Function:** It analyzes the user's desired activity and uses its tools to gather relevant data. For example, if the user wants to go hiking, it might check the weather forecast. If they want to go stargazing, it will check the astronomy data.
    *   **Tools:** This agent has a powerful set of tools at its disposal:
        *   `get_current_weather`: Fetches real-time weather for a location.
        *   `get_weather_forecast`: Gets the weather forecast for up to 14 days.
        *   `get_astronomy`: Retrieves astronomical data like sunrise, sunset, and moon phase.
        *   `get_current_date_time`: Gets the current date and time.
        *   `fact_finder_agent`: A sub-agent that can find general facts about activities or locations using Google Search.
    *   **Process:** After gathering the necessary information, it synthesizes it into a structured response with three parts:
        1.  **Tool Use:** A list of the tools it used, why it used them, and what it learned.
        2.  **Analysis:** Its reasoning and how the gathered data influences the advice.
        3.  **Advice:** The final recommendation to the user.

3.  **`fact_finder_agent` (The "Researcher"):**
    *   **Purpose:** This is a specialized sub-agent used by the `should_i_agent`.
    *   **Function:** Its sole job is to use Google Search to find answers to specific questions.
    *   **Tools:** Its only tool is `google_search`.

### Helper Functions (The "Tools")

The agents rely on several Python functions to interact with the outside world:

*   **`get_current_date_time()`:** A simple function to get the current date and time.
*   **Weather Functions (`get_current_weather`, `get_weather_forecast`):** These functions make API calls to the WeatherAPI service to get detailed weather data. They require a `WEATHER_API_KEY` to be set in a `.env` file.
*   **`get_astronomy()`:** This also uses the WeatherAPI to get astronomical information for a given location and date.

### Overall Workflow

1.  The user interacts with the `request_clarifier_agent`.
2.  The `request_clarifier_agent` chats with the user to determine the what, when, and where of their desired activity.
3.  Once clarified, it passes this information to the `should_i_agent`.
4.  The `should_i_agent` analyzes the request and uses its tools (including potentially calling the `fact_finder_agent`) to gather all necessary data.
5.  The `should_i_agent` formulates a detailed recommendation and presents it to the user.
