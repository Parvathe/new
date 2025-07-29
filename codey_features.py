import os
from langchain_google_vertexai import VertexAI
from vertexai.language_models import TextGenerationModel, CodeChatModel

# Set up Google Vertex AI environment
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "prj-adapt-app-dev-001--adapt-services.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"


def code_explanation(input_code):
    """Code Explainer function"""

    python_code_examples = """
    --------------------
    Example 1: Code Snippet
    x = 10
    def foo():
        global x
        x = 5
    foo()
    print(x)

    Correct answer: 5
    Explanation: Inside the foo function, the global keyword is used to modify the global variable x to be 5.
    So, print(x) outside the function prints the modified value, which is 5.
    ---------------------
    Example 2: Code Snippet
    def modify_list(input_list):
        input_list.append(4)
        input_list = [1, 2, 3]
    my_list = [0]
    modify_list(my_list)
    print(my_list)

    Correct answer: [0, 4]
    Explanation: Inside the modify_list function, an element 4 is appended to input_list.
    Then, input_list is reassigned to a new list [1, 2, 3], but this change doesn't affect the original list.
    So, print(my_list outputs [0, 4].)
    ----------------------
    """

    parameters = {
        "temperature": 0,
        "max_output_tokens": 1000
    }

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        f"""
        Your task is to act as a Python code Explainer.
        I'll give a code Snippet. Your job is to explain the code Snippet in two ways:
            1. Simple explanation of the code.
            2. step-by-step explanation of code.
        Break down the code into as many steps as possible.
        Share intermediate checkpoints along with results.
        Few good examples of python code output between #### separator:
        ####
        {python_code_examples}
        ####

        Code snippet is shared below, delimited with triple backticks:
        ```
        {input_code}
        ```

        """,
        **parameters,
    )

    return response.text.strip()



def code_review(input_code):
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"
    model = VertexAI(model_name="code-bison-32k", temperature=0)

    review_code_examples = """
    --------------------
    Example 1: Code Snippet
    
    addition = lambda , y: x + y
    print("Sum:", addition(3, ))
    
    Explanation:
    1 Lambda Function Syntax Error: The lambda function is missing parameter names ('x' and 'y') and the colon ':' between the parameter list and the function body.
    2 Syntax Error in the 'print' Statement: The 'print' statement is missing the second argument ('y') for the lambda function call.
    
    Corrected Version:
    addition = lambda x, y: x + y
    print("Sum:", addition(3, 5))
    
    This corrected version of the code should now execute without syntax errors and correctly print the sum of 3 and 5, which is 8.
    
    ---------------------
    Example 2: Code Snippet
    addition = lambda x, y: x + y
    print("Sum:", addition(3, 5))
    
    Explanation:
    This code defines a lambda function 'addition' that takes two arguments 'x' and 'y' and returns their sum. It then prints the sum of 3 and 5 using this lambda function.
    The code is correct, and it should output the sum as expected.
    If you encounter any errors in this code, it might be due to syntax errors or logical mistakes. However, in this case, the code appears to be error-free.
    If you have any specific requirements or concerns about the code, please let me know, and I can provide further assistance or corrections.
    ----------------------
    """
    
    def code_review_2(temperature: float = 0.0) -> object:
        """Example of using Codey for Code Chat Model to write a function."""
    
        # TODO developer
        parameters = {
            "temperature": temperature,  
            "max_output_tokens": 1024,  
        }
    
        code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
        chat = code_chat_model.start_chat()
    
        response = chat.send_message(
            f"""
            Your task is to act as a Python code Reviewer.
            I'll give a code Snippet. Your job is to review and debug the code Snippet:
                1. Review the code for any syntax errors, such as missing or misplaced characters, unmatched parentheses, or incorrect indentation.
                2. Check for semantic errors, including incorrect variable names, undefined variables, or invalid operations.
                3. Verify the logic of the code, including loop conditions, conditional statements, and function definitions.
                4. Ensure that all necessary libraries or modules are imported and properly used.
                5. Debug the code if any errors/bugs are found, providing comments or annotations to indicate the corrections made.
                6. If the code is error-free, provide feedback indicating that no errors were found.
            Please debug the code provided below and provide the corrected version:
            Give the review for the code, Also Explain the code in simple way.
            Few good examples of python code reviewer is  between #### separator:
            ####
            {review_code_examples}
            ####
    
            Code snippet is shared below, delimited with triple backticks:
            ```
            {input_code}
            ```
            """, **parameters
        )
        return response.text
    
    return code_review_2()


def comment_generation(input_code: str, temperature: float = 0.0) -> str:
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 1024,
    }
    
    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat = code_chat_model.start_chat()

    response = chat.send_message(
        f"""
        you are tasked to Adding Comments to Code:
                
            1. Review the code and identify key functionalities, algorithms, or important sections that require comments to enhance readability, maintainability, and understanding.
            2. Add comments to describe the purpose of each function, method, or block of code.
            3. Explain the logic, algorithms, or strategies used in the code to guide the reader through the implementation.
            4. Clarify any complex or non-obvious parts of the code to make it easier for users to understand and review.
            5. Ensure that comments are concise, informative, and follow consistent formatting and style guidelines.
            6. Place comments strategically throughout the code to provide context and explanation where needed.

        Please add comments to the code provided below to improve its readability and maintainability:
        ```
        {input_code}
        ```
        """, **parameters
    )

    return response.text

def test_case_generation(input_code: str, temperature: float = 0.0) -> str:
    """Generates unit test cases for provided code using a language model."""
    
    # Define parameters for code chat model
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 1024,
    }
    
    # Initialize Code Chat model
    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat = code_chat_model.start_chat()

    # Send input code to the model and get response
    response = chat.send_message(
        f"""
        Your task is to Generating Unit Test Cases.
            1. Review the code and identify key functionalities, functions, or methods that require unit tests to ensure their correctness.
            2. Create test cases to cover different scenarios, inputs, and edge cases for each function or method.
            3. Ensure that each test case is designed to validate a specific behavior or aspect of the code.
            4. Use assertions to check the expected outcomes or outputs of the functions or methods being tested.
            5. Consider boundary cases, error conditions, and corner cases to provide comprehensive test coverage.
            6. Organize test cases into logical groups and provide descriptive names to improve readability and maintainability.

        Please generate unit test cases for the code provided below delimited with triple backticks:
        ```
        {input_code}
        ```
        """, **parameters
    )

    return response.text
def code_optimization(input_code: str, temperature: float = 0.0) -> str:
    """Example of using Codey for Code Chat Model to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    }

    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat = code_chat_model.start_chat()

    response = chat.send_message(
        f"""
        You are my optimizing agent. Your task is to take the unoptimized code provided by the user and optimize it. 
        Please ensure that the optimized code maintains correct indentation and syntax to ensure it can be directly executed in the editor.
        Consider optimizing the code for efficiency and readability, and feel free to refactor or rewrite sections and algorithms as needed.
        Once you're satisfied with the optimization, please provide the optimized code below,
        remove all the unneccary comments only the code should be given as output in executable format
        Please generate optimized code for the provided below delimited with triple backticks:
        ```
        {input_code}
        ```
        """, **parameters
    )

    return response.text


def code_translation(input_code: str, temperature: float = 0.0) -> str:
    """Example of using Codey for Code Chat Model to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    }

    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat = code_chat_model.start_chat()

    response = chat.send_message(
        f"""
        You are my code translating agent.
        Your task is to:
            - Analyze the provided prompt to determine the desired programming language for code translation.
            - Identify the specific language keywords, syntax, and conventions required for the target programming language.
            - Translate the provided code snippet into the identified programming language, ensuring correctness and adherence to language-specific rules.
            - Pay attention to details such as variable names, function/method definitions, and control structures to maintain consistency with the target language.
            - Verify the translated code to ensure it accurately represents the functionality and behavior of the original code.
            - Provide comments or annotations to explain the translated language name.

        Please translate the provided code snippet into the appropriate programming language based on the analysis of the prompt provided below delimited with triple backticks:
        ```
        {input_code}
        ```

        """, **parameters
    )

    return response.text


def code_completion(input_code: str, temperature: float = 0.0) -> str:
    """Example of using Codey for Code Chat Model to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    }

    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat = code_chat_model.start_chat()

    response = chat.send_message(
        f"""
        Completing Partially Implemented Code:

            1. Review the provided code and identify sections or functionalities that are incomplete or missing.
            2. Analyze the context and requirements to understand the intended behavior of the code.
            3. Implement the missing or incomplete sections of the code to ensure it achieves the desired functionality.
            4. Follow best practices and coding conventions to maintain consistency and readability.
            5. Test the completed code to verify its correctness and ensure it meets the specified requirements.
            6. Provide comments or documentation as needed to explain the purpose and logic of the implemented code.

        Please complete the partially implemented code provided below in delimited with triple backticks:
        ```
        {input_code}
        ```
        """, **parameters
    )

    return response.text

def code_generation(input_code: str, temperature: float = 0.0) -> str:
    """Example of using Codey for Code Chat Model to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    }

    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat = code_chat_model.start_chat()

    response = chat.send_message(
        f"""
        You are my code generator. Your task is to generate code for {input_code}.
        Please ensure that the generated code maintains correct syntax and semantics to ensure it can be directly executed in the selected programming language.

        Scenarios to consider:
        - Generate efficient and readable code for the specified task.
        - Handle input/output appropriately as needed for the task.
        - Ensure that the generated code covers edge cases and handles errors gracefully.

        """, **parameters
    )

    return response.text
