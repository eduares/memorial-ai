import ollama


def generate_answer(question, context):

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]