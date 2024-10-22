
from logics import ai_assistant as bs, validator

def business_assistant() :  
    init_query = input("Hi! I am expert in business setup in Singapore. How may I help you today. ")

    while True:
        # validate the user input to ensure the necessary input are provided
        validation_response = validator.validate_user_input(init_query, "uc1")
        
        # check if further information is still needed to capture
        status = validation_response["valid_query"]

        user_input = {}
        
        if(status):
            user_input["init_query"] = init_query
            user_input["industry"] = validation_response["industry"]
            user_input["company_capital"] = validation_response["company_capital"]
            user_input["business_type"] = validation_response["business_type"]
            print(f"Input : {user_input}")

            ### this execution will take a few minutes to run
            crew = bs.business_assistant_crew()
            result = crew.kickoff(inputs=user_input)

            print(f"Consultation : {result}")

            status_check = input("Do you want to try again or exit?")
        
            if "exit" in status_check:
                break
            else:
                init_query = input("Hi! I am expert in business setup in Singapore. How may I help you today. ")
        else:
            init_query = init_query + " " + input(f"I don't understand your requirment. Please elaborate more.")



def tax_assistant() :  
    init_query = input("Hi! I am expert in finding the business grant in Singapore. How may I help you today. ")

    while True:
        # validate the user input to ensure the necessary input are provided
        validation_response = validator.validate_user_input(init_query, "uc2")
        
        # check if further information is still needed to capture
        status = validation_response["valid_query"]

        user_input = {}
        
        if(status):
            user_input["init_query"] = init_query
            user_input["industry"] = validation_response["industry"]
            user_input["company_revenue"] = validation_response["company_revenue"]
            user_input["business_type"] = validation_response["business_type"]
            user_input["additional_info"] = validation_response["additional_info"]
            print(f"Input : {user_input}")

            ### this execution will take a few minutes to run
            crew = bs.tool_test_crew()
            result = crew.kickoff(inputs=user_input)

            print(f"Consultation : {result}")

            status_check = input("Do you want to try again or exit?")
        
            if "exit" in status_check:
                break
            else:
                init_query = input("Hi! I am expert in business setup in Singapore. How may I help you today. ")
        else:
            init_query = init_query + " " + input(f"I don't understand your requirment. Please elaborate more.")


if __name__ == "__main__":
    #business_assistant()
    tax_assistant()