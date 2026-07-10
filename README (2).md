# AI Travel Planner Agent

This is my project for IBM SkillsBuild AICTE 2026 (Problem Statement No. 5).

I built an AI-powered travel planner that helps users plan their trips. You just tell it where you want to go, how many days, your budget, and what you like - and it gives you a complete day-by-day travel plan.

---

## What this project does

I made this using IBM Granite model through WatsonX. The app has two ways to use it:

1. You can fill in the sidebar with destination, number of days, budget and interests and click generate
2. Or you can just chat with it like a normal conversation

It gives you things like:
- Day wise itinerary with morning afternoon and evening plans
- Hotel and restaurant suggestions
- Local food tips
- Transport options
- Everything based on your budget (low medium or high)

---

## Tools and Technologies I used

- IBM Granite 3-8B Instruct model - this is the main AI model
- WatsonX Orchestrate - for building the agent
- IBM Cloud Lite - for the API and project
- Streamlit - for making the web interface
- Python - for the backend code
- IBM IAM - for authentication

---

## How to run this project

First make sure you have Python and Anaconda installed.

Step 1 - Create a conda environment
```
conda create -n travel_agent python=3.9
conda activate travel_agent
```

Step 2 - Install the required libraries
```
pip install -r requirements.txt
```

Step 3 - Open app.py and add your IBM credentials
```
IBM_API_KEY = "your api key here"
PROJECT_ID = "your project id here"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
```

Step 4 - Run the app
```
streamlit run app.py
```

Step 5 - Open your browser and go to
```
http://localhost:8501
```

---

## Files in this repository

- app.py - the main application code
- requirements.txt - all the libraries needed
- README.md - this file
- presentation.pptx - project presentation

---

## How I built this

First I set up my IBM Cloud account and created a WatsonX project. Then I connected the IBM Granite model to my Python code using the WatsonX API. I also created a Travel Planner Agent in WatsonX Orchestrate where I configured the budget rules in Indian Rupees and set up the agent instructions.

The Streamlit interface took some time to set up but finally it worked. The main challenge was getting the API authentication right and figuring out the correct region for my WatsonX project.

---

## What I learned

- How to use IBM Granite model through WatsonX API
- How to build an Agentic AI using WatsonX Orchestrate  
- How to create a web app using Streamlit
- How to handle IBM IAM token authentication
- How to debug API errors and fix region issues

---

Made by Sandesh Padwal
MIT Academy of Engineering, Alandi Pune
IBM SkillsBuild AICTE 2026
