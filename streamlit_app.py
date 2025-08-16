import streamlit as st
import os
import json
import requests
from openai import OpenAI

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")

def push(text):
    if PUSHOVER_TOKEN and PUSHOVER_USER:
        try:
            requests.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": PUSHOVER_TOKEN,
                    "user": PUSHOVER_USER,
                    "message": text,
                }
            )
        except:
            pass

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

# Tool definitions
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Any additional information about the conversation"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"}
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]

# João's summary (embedded directly)
SUMMARY = """João Andrade is a Brazilian software engineer, born and raised in Recife, Pernambuco. He is 26 years old. He graduated in Information Systems from the Computer Science Center of UFPE (Federal University of Pernambuco), one of the most prestigious computing institutions in Brazil. During his undergraduate studies, he served as a tutor for one year in two different courses: Calculus and Databases. In this role, he prepared and taught tutoring sessions, created exercises, corrected assessments, and provided ongoing support to students with questions. His work directly contributed to improving class performance and understanding of concepts.

Currently, João works remotely as a software engineer at Portico (also known as CourseKey), a California-based edtech company. He is also pursuing a postgraduate degree in Machine Learning at FIAP, aiming to deepen his knowledge of AI and build smarter, more useful solutions for everyday life.

At Portico, João has grown significantly as a professional, taking on a multifaceted role that blends technical excellence with proactive customer support and cross-functional collaboration.
He works across three key areas: Enablement, Incident Resolution, and Feature Development. In the Enablement team, João ensures that new features are correctly configured and integrated for each client. He plays a crucial role in verifying system integrations, identifying potential issues before they are reported, and coordinating closely with the Customer Success team to reduce friction and improve client satisfaction. His proactive approach has directly contributed to increased customer retention and smoother onboarding experiences.
João often joins technical calls with clients, especially when they're setting up complex features such as Single Sign-On (SSO) or custom automations. He is recognized internally for his calm, solution-oriented communication style and his ability to bridge technical gaps with empathy and clarity.
In Incident Resolution, João goes beyond fixing symptoms — he focuses on identifying and resolving the root cause of issues to prevent recurrence. His work has helped eliminate persistent bugs and improve the long-term stability of the platform.
As part of the Feature Development team, João contributes both to the frontend and backend, depending on project needs. He has worked on dashboards, notification systems, API integrations, and internal tooling. His tech stack includes Node.js, React, TypeScript, JavaScript, MySQL, MongoDB, AWS (including Lambda), and Google Cloud Platform. His deepening experience in serverless architecture and cloud infrastructure allows him to design scalable and efficient solutions that align with the product's growth.
Portico has been a space of continuous learning and professional maturity for João. He has become a trusted contributor, consistently improving platform reliability while ensuring that customer needs are met with both technical rigor and genuine care.

João began his career as an intern at Truewind between September 2018 and November 2019. There, he worked with the low-code OutSystems platform, as well as JavaScript and SQL Server. Working in support, he collaborated with a team partially based in Portugal and had direct contact with customers, gaining experience in technical communication and troubleshooting.

He then participated in the Samsung project in partnership with the UFPE Computer Science Center, from November 2019 to September 2022. He started as an intern and was later promoted to junior developer. During this time, he worked with .NET Core on the backend and React on the frontend, contributing to features such as push notifications, automated testing, and technical documentation. After being promoted, he was assigned to a new project focused on computer vision and machine learning, developing a desktop prototype for document scanning with .NET and Python. He also worked with Django and React in web applications, deepening his knowledge of these technologies, with a special focus on the backend.

Between October 2022 and January 2023, João worked at CESAR (Center for Advanced Studies and Systems of Recife), on an IoT project focused on vehicular communication. In this project, he used Docker and Kubernetes for environment orchestration and worked with DDS (Data Distribution Service)-based systems for communication in distributed applications. 
João has full-stack experience, with particular expertise in backend, databases, and integration with AI-based systems. His main technical skills include: Backend: Node.js, Express.js, Django, FastAPI, Flask, ASP.NET Core. Frontend: React, Vite, Material UI. Languages: Python, JavaScript, TypeScript, C#. Databases and ORMs: PostgreSQL, MySQL, MongoDB, Sequelize, Mongoose, Entity Framework, SQLAlchemy. AI/ML and Data: Machine learning models, data analysis, web scraping, integration with LLMs, prompt engineering, agentic AI (CrewAI, LangGraph, AutoGen, MCP). Cloud & Serverless: AWS (Lambda, S3, CloudWatch, Glue, Athena, Redshift), GCP. DevOps and Tools: Docker, Git

Outside of work, João is passionate about running along the Recife waterfront, Brazilian music, pop culture, and reality shows. He values friendships, social interaction, and leisure time with his dog, Koda.

João is known for his organization, clear communication, and dedication. He works well independently and as part of a team, always striving to clearly align expectations and deliver practical, well-documented, and thoughtful solutions for the end user. 

While he works full-time, João is passionate about taking on smaller, meaningful projects that make a real difference. He specializes in creating custom solutions including websites, AI/ML applications, automation tools, and innovative tech solutions. Whether you need a personal portfolio, a business automation, a data analysis tool, or an AI-powered application, João loves turning ideas into reality.

He particularly enjoys working with young entrepreneurs, startups, and individuals who have a vision but need technical expertise to bring it to life. His experience spans from simple websites to complex AI integrations, always with a focus on delivering clean, efficient, and impactful solutions.

If you have a problem that you think technology could solve, or if you have an idea you'd like to discuss, João would love to hear from you. He believes the best projects come from genuine conversations about real needs, and he's always excited to explore new ideas and possibilities. Don't hesitate to reach out - let's discuss how we can turn your vision into a working solution!

João is recognized by his peers and managers for his speed in solving problems, especially in high-pressure situations. He is highly resourceful and capable of identifying and resolving issues even when they fall outside his primary area of expertise. Whether it's diving into an unfamiliar codebase or debugging complex data workflows, João consistently finds efficient and scalable solutions.

He thrives in team-oriented environments and communicates clearly with both technical and non-technical stakeholders. With experience working across international teams, João is skilled at collaborating with professionals from diverse cultural backgrounds, always maintaining professionalism and building positive, productive relationships.

One of the biggest technical challenges João has worked on involved building a data-driven automation system that ingests and transforms large volumes of educational data. The process required extracting information from various tables, summarizing it, processing it through AWS Glue for ETL, and loading it into Redshift. From there, the system used that data to trigger intelligent notifications to specific audiences based on custom rules.

This project demanded not only backend expertise and familiarity with cloud tools like AWS Glue and Redshift, but also a deep understanding of system design, data modeling, and performance optimization. João played a critical role in its success by breaking down complex problems, coordinating across teams, and ensuring the system was scalable and reliable.

He is valued for his ability to keep the user experience in focus, even when working on backend or infrastructure-heavy tasks. His balanced approach between technical depth and collaboration makes him a dependable contributor to any team."""

class Me:
    def __init__(self):
        self.openai = OpenAI(api_key=OPENAI_API_KEY)
        self.name = "João Andrade"
        self.summary = SUMMARY

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background  which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "me" not in st.session_state:
    st.session_state.me = Me()

# Streamlit UI
st.set_page_config(
    page_title="Chat with João Andrade",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Chat with João Andrade")
st.markdown("Ask me anything about my career, skills, or projects!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Convert messages to the format expected by the chat function
            history = []
            for msg in st.session_state.messages[:-1]:  # Exclude the current user message
                history.append({"role": msg["role"], "content": msg["content"]})
            
            response = st.session_state.me.chat(prompt, history)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with additional info
with st.sidebar:
    st.header("About João")
    st.markdown("""
    - 🎓 Information Systems graduate from UFPE
    - 💼 Software Engineer at Portico (CourseKey)
    - 🚀 Full-stack developer with AI/ML expertise
    - 🌟 Passionate about creating meaningful solutions
    """)
    
    st.header("Get in Touch")
    st.markdown("""
    If you're interested in working together or have a project in mind, feel free to reach out!
    
    **Email:** [Your email here]
    **LinkedIn:** [Your LinkedIn here]
    """) 