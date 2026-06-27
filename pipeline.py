from agents import build_search_agent , build_reader_agent , writer_chain , critic_chain

def run_research_pipeline(topic : str) -> dict: 

    state = {}

    #search agent working
    print("\n" + "="*50)
    print("STEP 1 : Search agent is working......") 
    print("\n" + "="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user" , f"Find recent, reliable and detailed information about : {topic}")]
    })

    state['search_results'] = search_result["messages"][-1].content
    print("\nSearch result :", state["search_results"])


    #step 2: reader agent
    print("\n" + "="*50)
    print("STEP 1 : Reader agent is Scraping top resources......") 
    print("\n" + "="*50)

    reader_agent = build_reader_agent()

    read_result = reader_agent.invoke({
        "messages" : [("user" , 
            f"Based on the following search results about {topic}"
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"      
        )] 
    })

    state["scraped_content"] = read_result['messages'][-1].content

    print("\nScraped Content : \n\n" , state['scraped_content'])

    #step 3 writer chain

    print("\n" + "="*50)
    print("STEP 3 : Writer is drafting a report......") 
    print("\n" + "="*50)


    combine_research = (
        f"Search results : \n {state['search_results']}"
        f"Detailed scraped content : \n{state['scraped_content']}"
    ) 

    state["report"] = writer_chain.invoke({
        "topic" : topic ,
        "research" : combine_research
    })

    print("\nFinal Report\n" , state["report"])

    #critic report

    print("\n" + "="*50)
    print("STEP 4 : Critic is reviewing the report......") 
    print("\n" + "="*50)

    state['feedback'] = critic_chain.invoke({
        
        "report" :  state["report"]
    })

    print("\nCritic Report\n", state['feedback'])

    return state

if __name__ == "__main__" : 
    topic = input("Please enter a topic : ")
    run_research_pipeline(topic)



    