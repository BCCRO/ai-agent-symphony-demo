from langchain.agents import tool
import wikipedia

@tool
def wikipedia_search(query: str) -> str:
    """
    Performs a search on Wikipedia and returns a summary of the first result found.

    Args:
        query (str): Search term.

    Returns:
        str: Summary of the corresponding Wikipedia article.
    """
    try:
        summary = wikipedia.summary(query, sentences=5, auto_suggest=True, redirect=True)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"The query is ambiguous. Some possible options are: {e.options[:3]}"
    except wikipedia.PageError:
        return "No Wikipedia page was found for this term."
    except Exception as ex:
        return f"An unexpected error occurred: {str(ex)}"