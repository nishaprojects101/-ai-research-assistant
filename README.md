 AI Research Assistant

A full-stack multi-agent AI system that researches any topic
and generates professional reports using 4 specialized AI agents.

Tech Stack
Python, FastAPI, LangChain, Groq LLaMA 3.1, ChromaDB

Agents
1. Research Agent -> generates 3 sub-questions with answers
2. Summariser Agent ->extracts 5 key bullet points
3. Critic Agent -> identifies gaps and improves quality
4. Report Writer Agent -> formats professional final report

 Setup
1. pip install -r requirements.txt
2. Add GROQ_API_KEY to .env
3. uvicorn Main:app --reload
## Live Demo
Frontend: https://nishaprojects101.github.io/ai-research-assistant-frontend
Backend:  https://ai-research-assistant-znno.onrender.com/docs