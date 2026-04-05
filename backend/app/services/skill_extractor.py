"""
Skill extraction service — vocabulary-based matching with alias support.
Uses a curated list of real skills + common variations/aliases.
"""
import re
from typing import List, Set, Dict

# ── Skill aliases map: alias → canonical skill name ───────────────────────────
# This allows matching "node.js", "nodejs", "node js" → "node.js"
SKILL_ALIASES: Dict[str, str] = {
    "nodejs": "node.js",
    "node js": "node.js",
    "node": "node.js",
    "reactjs": "react",
    "react.js": "react",
    "vuejs": "vue",
    "vue.js": "vue",
    "angularjs": "angular",
    "nextjs": "next.js",
    "nuxtjs": "nuxt",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "k8s": "kubernetes",
    "gke": "kubernetes",
    "tf": "terraform",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "powerbi": "power bi",
    "ms sql": "sql server",
    "mssql": "sql server",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "gen ai": "generative ai",
    "genai": "generative ai",
    "llms": "llm",
    "nlp": "nlp",
    "cv": "computer vision",
    "dl": "deep learning",
    "ci cd": "ci/cd",
    "cicd": "ci/cd",
    "devops engineer": "devops",
    "aws cloud": "aws",
    "microsoft azure": "azure",
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "amazon web services": "aws",
    "spring boot": "spring boot",
    "rest api": "rest",
    "restful api": "rest",
    "restful": "rest",
    "ui ux": "ui/ux",
    "ux ui": "ui/ux",
    "figma design": "figma",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "ms office": "microsoft office",
    "ms word": "word",
    "unit test": "unit testing",
    "test automation": "test automation",
    "automated testing": "test automation",
    "nosql": "nosql",
    "agile methodology": "agile",
    "scrum methodology": "scrum",
    "project mgmt": "project management",
    "stakeholder mgmt": "stakeholder management",
}

# ── Canonical skill vocabulary ────────────────────────────────────────────────
SKILL_LIST: Set[str] = {
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go",
    "rust", "kotlin", "swift", "php", "ruby", "scala", "r", "matlab",
    "perl", "dart", "cobol", "fortran", "haskell", "elixir", "groovy",
    "assembly", "vba", "powershell", "shell", "bash",

    # Web — frontend
    "react", "angular", "vue", "next.js", "nuxt", "svelte",
    "astro", "jquery", "bootstrap", "tailwind", "sass", "css", "html",
    "html5", "css3", "webpack", "vite", "redux", "graphql",

    # Web — backend
    "node.js", "django", "flask", "fastapi", "spring boot", "spring",
    "express", "rails", "laravel", "asp.net", "nestjs",

    # Mobile
    "react native", "flutter", "android", "ios", "xcode", "swiftui",
    "jetpack compose",

    # Databases
    "sql", "postgresql", "mysql", "sqlite", "mongodb", "redis",
    "elasticsearch", "cassandra", "dynamodb", "neo4j", "oracle",
    "mariadb", "couchdb", "firestore", "supabase", "db2",
    "sql server", "nosql",

    # Cloud
    "aws", "azure", "gcp", "ec2", "s3", "lambda", "rds",
    "azure functions", "cloudflare", "vercel", "heroku",

    # DevOps / Infrastructure
    "docker", "kubernetes", "terraform", "ansible", "jenkins",
    "github actions", "gitlab ci", "circleci", "helm",
    "prometheus", "grafana", "nginx", "apache", "linux", "ci/cd", "devops",

    # Data / Analytics
    "pandas", "numpy", "spark", "hadoop", "airflow", "dbt",
    "tableau", "power bi", "looker", "excel", "google analytics",
    "data analysis", "data science", "data engineering",
    "etl", "data warehouse", "snowflake", "bigquery", "dax",
    "statistics", "a/b testing", "matplotlib", "seaborn",
    "data visualization", "data modeling",

    # AI / ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "hugging face",
    "llm", "generative ai", "langchain", "openai", "xgboost",
    "random forest", "neural network", "reinforcement learning",
    "artificial intelligence",

    # Security
    "cybersecurity", "penetration testing", "owasp", "ssl", "tls",
    "encryption", "firewalls", "soc", "siem", "vulnerability assessment",
    "information security",

    # Testing
    "unit testing", "integration testing", "selenium", "cypress",
    "jest", "pytest", "junit", "mocha", "playwright", "qa",
    "test automation", "manual testing", "performance testing",

    # APIs & Architecture
    "rest", "soap", "grpc", "websockets", "oauth", "jwt", "api",
    "microservices", "serverless", "event-driven", "system design",
    "distributed systems", "message queue",

    # Tools
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "figma", "postman", "swagger", "kafka", "rabbitmq", "celery",
    "notion", "slack", "trello", "vs code", "intellij", "linux",

    # Business / Office tools
    "salesforce", "sap", "erp", "crm", "hubspot", "zendesk",
    "sharepoint", "microsoft office", "google workspace",
    "powerpoint", "word", "google sheets", "ms project",

    # Design
    "ui/ux", "wireframing", "prototyping", "adobe xd",
    "photoshop", "illustrator", "sketch",

    # Finance / Accounting
    "accounting", "financial analysis", "budgeting", "forecasting",
    "financial modelling", "quickbooks", "tally", "ifrs", "gaap",
    "auditing", "taxation", "valuation", "risk management",

    # HR / Recruitment (only real skills, not context words)
    "recruitment", "talent acquisition", "performance management",
    "employee relations", "onboarding", "payroll", "hris",

    # Project/Operations
    "agile", "scrum", "kanban", "waterfall", "prince2", "pmp",
    "six sigma", "lean", "tdd", "bdd", "project management",
    "stakeholder management", "client management", "vendor management",
    "business analysis", "requirements gathering", "product management",

    # Networking
    "tcp/ip", "dns", "vpn", "networking", "cisco", "http",

    # Soft skills — only concrete/measurable ones
    "leadership", "communication", "team management",
    "mentoring", "training", "presentation", "documentation",
    "problem solving", "critical thinking", "time management",
}


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def _resolve_aliases(text: str) -> str:
    """Replace known aliases with canonical skill names."""
    for alias, canonical in SKILL_ALIASES.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        text = re.sub(pattern, canonical, text)
    return text


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text: alias-resolves first, then matches canonical vocabulary.
    Returns sorted, deduplicated list.
    """
    normalized = _normalize(text)
    normalized = _resolve_aliases(normalized)
    found: Set[str] = set()
    for skill in SKILL_LIST:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, normalized):
            found.add(skill)
    return sorted(found)


def extract_missing_skills(resume_text: str, job_text: str) -> List[str]:
    """
    Return skills present in the job description but absent from the resume.
    """
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))
    return sorted(job_skills - resume_skills)
