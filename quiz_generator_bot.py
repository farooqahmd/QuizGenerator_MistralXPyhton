import ollama
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def get_quiz_from_llm(topic, num_questions=5):
    # Generate quiz questions and answers using Mistral
    prompt = f"Generate a quiz with {num_questions} multiple-choice questions on the topic '{topic}'. For each question, provide 4 options and indicate the correct answer. Format each question as: 'Q: [question] Options: [option1], [option2], [option3], [option4] Correct Answer: [correct answer]'."
    response = ollama.generate(model='mistral', prompt=prompt)
    return response['response'].split('\n')

def create_pdf(quiz_lines, topic, filename="quiz_output.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Quiz on {topic}")
    c.drawString(100, 730, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    y = 700
    for line in quiz_lines:
        if line.strip():  # Skip empty lines
            y -= 20
            if y < 50:  # Move to new page if needed
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 750
            c.drawString(100, y, line[:80])  # Truncate long lines for PDF
    
    c.save()
    print(f"PDF saved as {filename}")

def main():
    topic = input("Enter quiz topic (e.g., Python Programming, General Knowledge): ")
    try:
        num_questions = int(input("Enter number of questions (default 5): ") or 5)
    except ValueError:
        num_questions = 5
    
    # Generate quiz using Mistral
    quiz_lines = get_quiz_from_llm(topic, num_questions)
    
    # Create PDF with quiz
    create_pdf(quiz_lines, topic)

if __name__ == "__main__":
    main()