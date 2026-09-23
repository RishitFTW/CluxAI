from CluxAI.config import config
from CluxAI.observability.logger import get_logger

logger = get_logger(__name__)


def get_llm():
    """Return the right LangChain LLM based on config."""
    provider = config["llm"]["provider"]
    model = config["llm"]["model"]
    logger.info(f"Using LLM provider: {provider}, model: {model}")

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=model)
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model)
    elif provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=model)

    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=model)


def get_embedder():
    """Return the right LangChain embedder based on config."""
    provider = config["embeddings"]["provider"]
    model = config["embeddings"]["model"]
    logger.info(f"Using embeddings provider: {provider}, model: {model}")

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=model)
    elif provider == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(model=model)

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model=model)