"""Generates structured, actionable improvement suggestions based on missing skills."""
from typing import List

# Detailed advice per skill: what to learn + how to demonstrate it
_SKILL_ADVICE: dict[str, str] = {
    # Languages
    "python": "Add Python to your skills — build a project (web scraper, data pipeline, or REST API) and push it to GitHub to demonstrate hands-on experience",
    "java": "Add Java experience — build a Spring Boot REST API or an Android app and document it in your portfolio",
    "javascript": "Add JavaScript — build an interactive front-end project (React or vanilla JS) and host it on GitHub Pages or Vercel",
    "typescript": "Add TypeScript — migrate an existing JS project to TypeScript and highlight it on your resume",
    "c++": "Add C++ — solve competitive programming problems on LeetCode or contribute to a systems-level open-source project",
    "go": "Add Go — write a REST microservice or CLI tool in Go and publish it on GitHub",
    "rust": "Add Rust — work through Rust by Example and build a small systems utility",
    "kotlin": "Add Kotlin — build an Android app or a Kotlin-based backend (Ktor) and publish it",
    "swift": "Add Swift — build and publish an iOS app to the App Store or TestFlight",
    "php": "Add PHP — build a web project using Laravel and deploy it on a shared host",
    "ruby": "Add Ruby — build a Ruby on Rails CRUD application and deploy it to Heroku",
    "scala": "Add Scala — work through Functional Programming in Scala and build a Spark data pipeline",
    "r": "Add R — complete a data analysis project and publish your findings as an R Markdown report",
    "vba": "Add VBA — automate a repetitive Excel workflow and document the macro in your portfolio",

    # Web frontend
    "react": "Add React — build a multi-page React app with hooks and state management (Redux or Context API) and deploy it on Vercel",
    "angular": "Add Angular — create a full CRUD app using Angular + TypeScript and deploy it",
    "vue": "Add Vue — develop a Vue 3 project with Pinia for state management and host it",
    "next.js": "Add Next.js — build an SSR/SSG web app with Next.js and deploy it on Vercel",
    "css": "Add CSS skills — practise Flexbox/Grid layouts on Frontend Mentor challenges",
    "html": "Add HTML — build a portfolio website with semantic HTML5 and accessible markup",
    "tailwind": "Add Tailwind CSS — redesign an existing project's UI using Tailwind utility classes",
    "redux": "Add Redux — implement global state management in a React project using Redux Toolkit",

    # Web backend
    "node.js": "Add Node.js — build a RESTful API with Express.js, include JWT auth, and deploy it",
    "django": "Add Django — build a full-stack web app with Django REST Framework and a React frontend",
    "flask": "Add Flask — create a REST API with Flask-SQLAlchemy and deploy it on Railway or Render",
    "fastapi": "Add FastAPI — build an async REST API with FastAPI and auto-generated Swagger docs",
    "spring boot": "Add Spring Boot — build a production-ready Java REST API with Spring Boot, JPA, and security",
    "express": "Add Express.js — build a Node.js API with Express, middleware, and MongoDB",

    # Databases
    "sql": "Improve SQL skills — practise advanced queries (window functions, CTEs, subqueries) on LeetCode SQL or HackerRank",
    "postgresql": "Add PostgreSQL — set up a local instance, design a normalised schema, and write complex queries",
    "mysql": "Add MySQL — build a relational database for a CRUD application and optimise queries with indexes",
    "mongodb": "Add MongoDB — build a Node.js + MongoDB project demonstrating CRUD, aggregation, and indexes",
    "redis": "Add Redis — implement caching for a backend API and show measurable speed improvements",
    "elasticsearch": "Add Elasticsearch — index a dataset and build full-text search with filtering and ranking",
    "dynamodb": "Add DynamoDB — design a single-table DynamoDB model for a serverless application",

    # Cloud
    "aws": "Add AWS — complete the AWS Cloud Practitioner certification and deploy a project using EC2, S3, and RDS",
    "azure": "Add Azure — take the AZ-900 certification and deploy a web app using Azure App Service",
    "gcp": "Add GCP — deploy a project using Cloud Run or App Engine and complete the Google Cloud Digital Leader course",

    # DevOps
    "docker": "Add Docker — containerise an existing application with a Dockerfile and docker-compose, and push it to Docker Hub",
    "kubernetes": "Add Kubernetes — set up a local cluster with Minikube, deploy your Dockerised app, and document the process",
    "terraform": "Add Terraform — write IaC to provision cloud infrastructure (at minimum an EC2 + RDS setup)",
    "ci/cd": "Add CI/CD — set up a GitHub Actions pipeline that runs tests and deploys on every push to main",
    "github actions": "Add GitHub Actions — configure a workflow with linting, testing, and deployment stages",
    "jenkins": "Add Jenkins — set up a Jenkins pipeline for a multi-stage build, test, and deploy process",
    "ansible": "Add Ansible — write playbooks to automate server setup and application deployment",
    "linux": "Add Linux — practise administration on a VPS (set up a server, configure nginx, manage users and permissions)",
    "devops": "Add DevOps practices — implement CI/CD, containerisation, and monitoring in a personal or team project",

    # Data / Analytics
    "pandas": "Add Pandas — complete an end-to-end data cleaning and analysis project and publish it on Kaggle or GitHub",
    "numpy": "Add NumPy — implement ML algorithms from scratch using NumPy to demonstrate mathematical understanding",
    "spark": "Add Apache Spark — process a large public dataset using PySpark and document performance comparisons",
    "tableau": "Add Tableau — build an interactive dashboard from a public dataset and publish it on Tableau Public",
    "power bi": "Add Power BI — create a business dashboard connecting to multiple data sources and publish it",
    "excel": "Add Excel/advanced spreadsheet skills — demonstrate pivot tables, VLOOKUP/XLOOKUP, and macro automation",
    "data analysis": "Add Data Analysis — complete an end-to-end project (data cleaning → visualisation → insights) and publish it",
    "data science": "Add Data Science — complete a Kaggle competition or publish a data science project with clear insights",
    "etl": "Add ETL experience — design and implement a pipeline that extracts, transforms, and loads data to a warehouse",
    "data visualization": "Add data visualisation skills — create dashboards or charts using Tableau, Power BI, or Matplotlib/Seaborn",
    "statistics": "Add Statistics — demonstrate applied statistics through A/B testing, hypothesis testing, or regression analysis",

    # AI / ML
    "machine learning": "Add Machine Learning — complete an end-to-end ML project (data → model → evaluation → deployment) and document it",
    "deep learning": "Add Deep Learning — implement and train a neural network (image classifier or text model) using PyTorch or TensorFlow",
    "nlp": "Add NLP — build a text classification, summarisation, or sentiment analysis pipeline and publish it",
    "tensorflow": "Add TensorFlow — complete the TensorFlow Developer Certificate or build and deploy a neural network",
    "pytorch": "Add PyTorch — replicate a published research paper or fine-tune a pre-trained model on a custom dataset",
    "scikit-learn": "Add scikit-learn — implement a full ML pipeline (preprocessing → model selection → cross-validation → evaluation)",
    "llm": "Add LLM experience — build an application using OpenAI API or Hugging Face models (chatbot, summariser, or RAG system)",
    "generative ai": "Add Generative AI — build a project using LLMs, diffusion models, or similar (e.g., RAG chatbot, image generator)",
    "langchain": "Add LangChain — build a retrieval-augmented generation (RAG) application using LangChain and a vector database",

    # Testing
    "unit testing": "Add unit testing — write test suites with pytest (Python) or JUnit (Java) achieving >80% coverage for a project",
    "selenium": "Add Selenium — write end-to-end browser automation tests for a web application",
    "cypress": "Add Cypress — write E2E tests for a React or JavaScript web application",
    "jest": "Add Jest — write unit and integration tests for a Node.js/React project",
    "pytest": "Add pytest — write comprehensive test suites for Python projects with fixtures and mocking",
    "test automation": "Add test automation — set up a full test suite (unit + integration + E2E) integrated with a CI/CD pipeline",
    "qa": "Add QA experience — document a test plan, write test cases, and demonstrate bug reporting skills",

    # Security
    "cybersecurity": "Add Cybersecurity — complete the CompTIA Security+ or CEH certification",
    "penetration testing": "Add penetration testing — practise on TryHackMe or HackTheBox and document findings",

    # APIs & Architecture
    "rest": "Add REST API design — build a well-documented RESTful API following OpenAPI spec with proper error handling",
    "graphql": "Add GraphQL — add a GraphQL layer to an existing REST API or build a new API using Apollo or Strawberry",
    "microservices": "Add Microservices experience — decompose a monolithic project into services and deploy them with Docker Compose",
    "system design": "Add System Design knowledge — study Grokking System Design and practise designing scalable systems",

    # Tools / Methodologies
    "git": "Add advanced Git skills — practise branching strategies (Gitflow), rebasing, and cherry-picking",
    "agile": "Add Agile — get a Scrum certification (PSM I) or actively practise Agile in a team project",
    "scrum": "Add Scrum — get the Professional Scrum Master (PSM I) certification or lead a sprint in a project",
    "jira": "Add Jira — use Jira to manage a project backlog, write user stories, and track sprints",
    "figma": "Add Figma — design a mobile or web UI mockup with components and a design system",

    # Business tools
    "salesforce": "Add Salesforce — complete the Salesforce Administrator certification (Trailhead platform is free)",
    "sap": "Add SAP — complete an SAP Business Suite module training course or certification",

    # Finance
    "financial analysis": "Add Financial Analysis — build a financial model (DCF, LBO, or comparable analysis) and document your assumptions",
    "accounting": "Add Accounting — demonstrate bookkeeping, P&L analysis, and financial reporting skills in a project",
    "budgeting": "Add Budgeting — create a detailed budget model with scenario analysis and variance tracking",

    # HR
    "recruitment": "Add Recruitment experience — document end-to-end hiring experience (sourcing, screening, interviewing, offer)",
    "talent acquisition": "Add Talent Acquisition — describe your sourcing channels, interview processes, and key hiring metrics",
    "payroll": "Add Payroll management — demonstrate experience with payroll processing software and compliance",

    # Soft skills
    "leadership": "Add Leadership — describe specific instances of leading teams, mentoring, or driving projects end-to-end",
    "project management": "Add Project Management — pursue a PMP, PRINCE2, or Agile certification, or document a complex project you managed",
    "stakeholder management": "Add Stakeholder Management — describe how you managed cross-functional communication and expectation setting",
    "business analysis": "Add Business Analysis — document requirements gathering, process mapping, or gap analysis you have performed",
    "communication": "Add Communication — highlight presentations, technical documentation, or cross-team collaboration in your work history",
    "ui/ux": "Add UI/UX Design — complete Google's UX Design Certificate (Coursera) and build a portfolio of Figma prototypes",

    # Networking
    "networking": "Add Networking — study TCP/IP, subnetting, and DNS; get the CompTIA Network+ or Cisco CCNA certification",
}

_DEFAULT_SUGGESTION = (
    "Your resume closely matches the job description — "
    "tailor your bullet points to mirror the exact language and keywords used in the job posting"
)


def generate_suggestions(missing_skills: List[str]) -> List[str]:
    """Return specific, actionable suggestion for each missing skill."""
    suggestions: List[str] = []
    for skill in missing_skills:
        advice = _SKILL_ADVICE.get(skill.lower())
        if advice:
            suggestions.append(advice)
        else:
            suggestions.append(
                f"Add '{skill.title()}' to your resume — include it in your Skills section "
                f"and reference it in at least one job bullet point or project description"
            )
    if not suggestions:
        suggestions.append(_DEFAULT_SUGGESTION)
    return suggestions
