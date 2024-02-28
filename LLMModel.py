import openai as OpenAI

class LLMModel:
    def __init__(self):
        # Initialize recommendation model and related resources
        pass    

    def get_llm_items(self,query):
        # Make a request to the OpenAI API
        completion = OpenAI.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",                    
                    "content": "Respond in a list of 10 items that matches the context of toys and stationery retail stores, without numbers. If no items found return an empty list."
                },
                {"role": "user", "content": query}
            ],
            n=1  # Get 1 possible response
        )

        # Process the response to extract the items
        item_list = []
        if completion:
            for choice in completion.choices:
                # Assuming each choice.message.content contains one item
                item_list.append(choice.message.content)
        # Split each item by newline character and remove the numbering
        print(item_list)        
        item_list = item_list[0].split('\n')
        if('.' in item_list[0]):
        # Extracting each item, removing the numbering, and enclosing in double inverted commas
            llm_items = ['"' + item.split('. ')[1] + '"' for item in item_list if item.strip()]
        else:
            llm_items = ['"' + item + '"' for item in item_list if item.strip()]
        #llm_items = ['"' + item + '"' for item in item_list if item.strip()]
        return llm_items


#get_llm_items("Suggest items for a 10 year old birthday party")
