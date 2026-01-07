# File2Form

A FastAPI server that receives a file (pdf, docx, txt, ...) and extracts relevant information (e.g. to fill in a form) via LLM calls.
Returns a JSON object compliant to the chosen schema (i.e. PROMPT_ID + PROMPT_VERSION), as defined in `app/prompts`.
Supported LLM providers are OpenAI and Groq.

### Set local environment

    $ nano .env
    OPENAI_API_KEY=<your OpenAI API key>
    GROQ_API_KEY=<your Groq API key>
    LLM_PROVIDER=groq
    PROMPT_ID=groq
    PROMPT_VERSION=v1

### Run with Docker

    $ docker-compose up

### Example request

    $ curl -XPOST localhost:8000/extract/ -F "file=@filename"
