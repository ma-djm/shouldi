# ShouldI (Should I?)

Ever wondered if the weather will hold up for your plans? `ShouldI` is a conversational AI agent that gives you tailored advice on whether to go ahead with a specific activity.

Built as a demo of the Google Agent Development Kit (ADK), this project demonstrates a multi-agent pattern:

1.  A user-facing **"Clarifier"** agent chats with you to understand what you want to do, when, and where.
2.  Once it has the details, it passes the request to a **"Should I?"** agent that uses a suite of tools—like weather forecasts, astronomy data, and Google Search—to research the answer. These tools, in turn, make calls to public APIs on the web.
3.  Finally, it analyzes the data and gives you a detailed recommendation.

### See It in Action

Here is an example of the agent helping a user plan a trip:


> **[user]:** I have an activity planned for this Thursday, but I'm worried about the weather.
>
> **[request_clarifier]:** I can help with that! What activity are you planning for Thursday, and where will it be taking place?
>
> **[user]:** I want to ride the Pike's Peak Cog Railway
>
> **[request_clarifier]:** Okay, so you want to ride the Pike's Peak Cog Railway this Thursday. Where is the Pike's Peak Cog Railway located?
>
> **[user]:** Colorado Springs
>
> **[request_clarifier]:** So, just to confirm, you want to know if you should ride the Pike's Peak Cog Railway in Colorado Springs this Thursday, correct?
>
> **[user]:** Yes
>
> 
> * In get_current_date_time()
> * In get_weather_forecast(location: Colorado Springs, days: 2)
> 
>
> **[should_i]:**
> **Tool Use:**
> * get_current_date_time: I used this tool to determine that "this Thursday" is August 21, 2025. This allowed me to look at the correct day in the forecast.
> * get_weather_forecast: I used this tool to get the weather forecast for Colorado Springs for Thursday. The key information I obtained was that the high temperature will be 91.8°F, the low will be 58.6°F, it will be sunny with no chance of rain, and the maximum wind speed will be 13.4 mph.
> * fact_finder: I used this tool to learn about the temperature difference between Colorado Springs and the summit of Pikes Peak. I found out that the summit is typically 30°F cooler than the ase.
>
> **Analysis:**
> The weather forecast for your trip to the Pike's Peak Cog Railway on Thursday is excellent. It will be a sunny day with no chance of rain, which means you should have fantastic, clear views from the summit. The winds are also expected to be mild. The most important factor to consider is the significant temperature difference between the base and the summit. While it will be a warm day in Colorado Springs, the summit will be about 30 degrees cooler.
>
> **Advice:**
> Yes, you should definitely go on your Pike's Peak Cog Railway ride this Thursday. The weather conditions are ideal for this activity, with plenty of sunshine and no rain in the forecast, which will make for breathtaking views.
>
> However, be sure to prepare for the temperature change. I recommend dressing in layers. While it may be warm at the base, it will be significantly cooler at the 14,115-foot summit. A light jacket or a fleece would be a good idea to bring with you to ensure you are comfortable while enjoying the stunning panorama.

### Key Concepts for Developers

This project is a great way to learn the Google ADK. A few things to observe in the code:

-   **Simple, High-Level Instructions:** The prompts for the agents in `agent.py` are straightforward. The agent has wide latitude to decide which tools to use to carry out the request.
-   **Docstrings as Tool Definitions:** The tools (the Python functions that call the WeatherAPI) have highly detailed docstrings. The ADK uses these to help the agent understand how to use the tool and what to expect in return. Good documentation directly improves agent performance.
-   **Debugging Output:** As a demo, the agent prints the tools it's using and its reasoning. In a production app, this data would more likely be structured (e.g., as JSON) and saved to the session state.




## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ma-djm/shouldi.git
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
