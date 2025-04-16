from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="markeos",
    version="0.1.0",
    description="Analisador de cursos usando IA através da API OpenHouter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MarkeOS",
    author_email="contato@markeos.com",
    url="https://github.com/seu-usuario/markeos",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "fastapi>=0.109.2",
        "uvicorn>=0.27.1",
        "pydantic>=2.6.1",
        "python-dotenv>=1.0.1",
        "aiohttp>=3.9.3",
        "openai>=1.12.0",
        "python-multipart>=0.0.9"
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.1",
            "pytest-asyncio>=0.23.5",
            "httpx>=0.26.0",
            "pytest-env>=1.1.3",
            "black>=24.1.1",
            "mypy>=1.8.0"
        ]
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "markeos-analyzer=markeos.course_analyzer:run_course_analyzer_service",
            "markeos-check-env=markeos.check_env:check_env"
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/seu-usuario/markeos/issues",
        "Source": "https://github.com/seu-usuario/markeos",
    },
)