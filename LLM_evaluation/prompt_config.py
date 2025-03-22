def generate_prompt(question):
    """
    Generate a prompt for the given question.
    Args:
        question (str): The question text.
    Returns:
        list: A formatted prompt for the LLM.
    """
    instruction = (
        "Solve the following problem step-by-step. "
        "At the end of the solution, explicitly include the final numerical answer "
        "in a separate tag like this:\n\n"
        '"Answer": "final numerical value"\n\n'  # Ensure this line is properly quoted
        "Here is the question:"
    )
    return [{"role": "user", "content": f"{instruction}\n\n{question}"}]
