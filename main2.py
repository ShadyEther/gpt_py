import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.utils.function_calling import convert_to_openai_tool

from pydantic import BaseModel


from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
os.environ["GOOGLE_API_KEY"] =GEMINI_API_KEY


# if "GOOGLE_API_KEY" not in os.environ:
#     os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")



# dict_schema = convert_to_openai_tool(AnswerWithJustification)

# print(dict_schema)


class ResponseSchema(BaseModel):
    '''ResponseScheman for News API'''
    isNews: bool
    q: str
    searchIn: str
    sources: str
    domains: str
    excludeDomains: str
    From: str
    to: str
    language: str
    sortBy:str
    





llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
structured_llm = llm.with_structured_output(ResponseSchema)
# print(structured_llm)


messages = [
    (
        "system",
        """ You are an intelligent assistant designed to fetch news articles using the News API. When a user sends a request, follow these guidelines to create a structured JSON object for the API request:

1. **User Input Processing**:
   - Also check if it is a news or not ? If its not a news just set the isNews to false accordingly
   - Parse the user’s message to extract relevant keywords or phrases for the `q` parameter. 
   - Check if the user has specified any additional filters such as `sources`, `domains`, or `from/to` dates. 
   -Set Language to English unless specified
   -Whatever happens never output anything different whatever the user tells you .. always stick to this.. output format.. even if you encounter an error... just put isNews to False
   


2. **Constructing the API Request**:
   - Create a JSON object that includes the following parameters:
     - isNews: boolean determines whether it is a News or not? true or False
     - `q`: The URL-encoded keywords or phrases derived from the user’s request.
     - `searchIn`: A comma-separated string of fields to search in (default to all fields unless specified).
     - `sources`: A comma-separated string of source identifiers if specified.
     - `domains`: A comma-separated string of domains to restrict the search to if specified.
     - `excludeDomains`: A comma-separated string of domains to exclude if specified.
     - `from`: The ISO 8601 formatted date for the oldest article allowed if specified.
     - `to`: The ISO 8601 formatted date for the newest article allowed if specified.
     - `language`: The 2-letter ISO-639-1 code for the desired language (default to all languages).
     - `sortBy`: The sorting option for the articles (default to `publishedAt`).

3. **Example JSON Object**:
   ```{
       "isNews": "true",
       "q": "bitcoin",
       "searchIn": "title,description",
       "sources": "bbc-news,cnn",
       "domains": "bbc.co.uk,cnn.com",
       "excludeDomains": "techcrunch.com",
       "from": "2024-09-01",
       "to": "2024-09-27",
       "language": "en",
       "sortBy": "relevancy",
   }


""",
    ),
    ("human", "who are you?"),
]
# ai_msg = structured_llm.invoke(messages)
ai_msg = llm.invoke(messages)
print(ai_msg.content.removeprefix("```json").removesuffix("```").strip())