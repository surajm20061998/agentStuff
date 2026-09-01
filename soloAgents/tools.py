from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_FILE = PROJECT_DIR / "research_output.txt"


def save_to_txt(data: str, filename: str | None = None):
    output_path = Path(filename).expanduser() if filename else DEFAULT_OUTPUT_FILE
    if not output_path.is_absolute():
        output_path = PROJECT_DIR / output_path

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with output_path.open("a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {output_path}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name = "search_web",
    func = search.run,
    description="Search the web for information",    
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
