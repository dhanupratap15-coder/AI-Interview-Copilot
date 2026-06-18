def generate_questions():
    import os
    import sys
    import re
    # import pyttsx3
    from langchain_core.output_parsers import StrOutputParser
    parser = StrOutputParser()
    from langchain_core.prompts import ChatPromptTemplate
    # First path
    parent_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(
                r"C:\Users\ASUS\OneDrive\data science\project\INTERVIEW COPILOT PROJECT\Generate_Question\genrate_question.py"
            ),
            ".."
        )
    )
    sys.path.append(parent_dir)

    # Second path
    second_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(
                r"C:\Users\ASUS\OneDrive\data science\project\INTERVIEW COPILOT PROJECT\ChatModel\mistral_chat_modle.py"
            ),
            ".."
        )
    )

    sys.path.append(second_dir)
    # third path
    third_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(
                r"C:\Users\ASUS\OneDrive\data science\project\INTERVIEW COPILOT PROJECT\SelectRollBasicOfResume\resumeroll.py"
            ),
            ".."
        )
    )

    sys.path.append(third_dir)
    from SelectRollBasicOfResume.resumeroll import resume
    from ChatModel.mistral_chat_modle import llm
    from generate_roll import response_roll


    # engine = pyttsx3.init()
    # engine.setProperty('rate', 129)
    # engine.setProperty('volume', 1.0)
    # text = f"Are You {response_roll} yes or no   :  "
    # clean_text = re.sub(r'[^a-zA-Z ]', '', text)
    # engine.say(clean_text)
    # engine.runAndWait()
    roll = input(f"Are You {response_roll} Yes Or No  :  ")
    if roll.lower().strip() == "no" :
        print("Plese Chek Your Resume")
    elif roll.lower().strip() == "yes" :        
        from langchain_core.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an expert technical interviewer.

            Your task is to generate exactly 5 interview questions based on:

            1. The candidate's detected job role.
            2. The candidate's resume keywords and skills.

            Instructions:

    * Analyze the provided job role and resume keywords.
    * Generate exactly 5 interview questions.
    * Ask only one concept or topic per question.
    * Keep each question short and direct.
    * Each question must be a single sentence.
    * Maximum length: 15 words per question.
    * Do not combine multiple topics in one question.
    * Focus on the most important skills from the resume.
    * Difficulty level: Internship / Entry-Level.
    * Return only numbered questions.
    * Do not provide answers.
    * Do not provide explanations.
    * Do not provide introductions or conclusions.

            """
        ),
        (
            "human",
            """
            Job Role:
            {role}

            Resume Keywords:
            {keywords}
            """
        )
    ])
        try:
            chain = prompt | llm | parser

            questions = chain.invoke({
                "role": response_roll,
                "keywords": resume
            })
        except KeyError as e:
            print(f"Missing input variable: {e}")

        except AttributeError as e:
            print(f"Attribute Error: {e}")
            print("Check if 'resumeroll.resume' exists.")

        except Exception as e:
            print(f"An error occurred: {e}")
    return questions            