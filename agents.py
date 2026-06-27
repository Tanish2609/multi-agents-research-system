from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
from tools import web_search , scrape_url
#model
llm = ChatMistralAI(model = "mistral-small-2506")

#agent 1
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )


#agent 2
def build_reader_agent():
    return create_agent(
        model = llm ,
        tools = [scrape_url]
    )

#writer chain

writer_prompt = ChatPromptTemplate.from_messages([
    ('system' , 'You are an expert research writer. Write clear , structured and insightful reports.') ,
    ('human' , """Write a detailed research on topic below.
     
    Topic : {topic}
    
     Research Gathered : {research}
     
     Structure the report as :
     -Introduction
     -Key Findings (minimum 3 well explained points)
     -Conclusion
     -Sources (list all the URLs found in research)

     Be detailed , factual and professional""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic chain

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior research editor and critic.

Your job is to rigorously review research reports and identify weaknesses.

Evaluate the report on the following criteria:

1. Accuracy
   - Are there any unsupported claims?
   - Are facts properly backed by the provided research?

2. Completeness
   - Are important aspects of the topic missing?
   - Is the coverage sufficiently detailed?

3. Structure & Organization
   - Is the report logically organized?
   - Are sections clear and coherent?

4. Clarity
   - Is the writing easy to understand?
   - Are explanations sufficiently detailed?

5. Source Usage
   - Are sources properly referenced?
   - Are any claims lacking evidence?

6. Improvements
   - Suggest specific improvements to make the report stronger.

Be critical, objective, and constructive.

Do NOT rewrite the report.

Return your review in the following format:

Overall Score: X/10

Strengths:
- ...

Weaknesses:
- ...

Missing Information:
- ...

Recommended Improvements:
- ...

Final Verdict:
(Accept / Needs Revision / Major Revision Required)
"""
    ),
    (
        "human",
        """

Generated Report:
{report}
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()

