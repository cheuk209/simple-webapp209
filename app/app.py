from flask import Flask, render_template
import os
from openai import OpenAI
from dotenv import load_dotenv
import time
from flask import Flask, request, jsonify, render_template, send_from_directory, render_template_string


load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=my_key)

instructions="""
    You are a passionate F1 fan who will act as an assistant to explaining F1 rules or discussing F1 games and players.
    Answer all questions related to F1 to the best of your ability. Portray yourself as a fellow fan and make your tone
    conversational and friendly. Do not be formal, present facts but do so like a passionate fan of the sport.
"""

def create_assistant():
    # Create the assistant
    assistant = client.beta.assistants.create(
        name="Coding MateTest 4",
        instructions=instructions,
        model="gpt-4-1106-preview",
        tools=[{"type": "code_interpreter"}]
    )
    return assistant



def add_message_to_thread(thread_id, user_question):
    # Create a message inside the thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= user_question
    )
    return message


def get_answer_from_AI(assistant_id, thread):
    print("Thinking...")
    # run assistant
    print("Running assistant...")
    run =  client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # wait for the run to complete
    while True:
        runInfo = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if runInfo.completed_at:
            # elapsed = runInfo.completed_at - runInfo.created_at
            # elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            print(f"Run completed")
            break
        time.sleep(1)

    print("All done...")
    # Get messages from the thread
    messages = client.beta.threads.messages.list(thread.id)
    message_content = messages.data[0].content[0].text.value
    return message_content

app = Flask(__name__)
assistant = create_assistant()
thread = client.beta.threads.create()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def get_answer():
    question = request.form.get('question')
    print(request.data)
    print(request.form)
    # Process the question and generate an answer
    if not question:
        return "<p>No question received.</p>"
    if "exit" in question.lower():
        return "Exiting..."
    add_message_to_thread(thread.id, question)
    message_content = get_answer_from_AI(assistant.id, thread)
    print(message_content)
    response = """
    <h3>You asked: {question}</h3>
    <p>The answer to your question is:</p>
    """.format(question=question)
    return render_template_string(response + message_content, message_content=message_content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)