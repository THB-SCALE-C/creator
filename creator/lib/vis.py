from IPython.display import HTML

def render_learning_content(data):
    html = []

    # Basic CSS for readability in Jupyter
    html.append("""
    <style>
        .course { font-family: Arial, sans-serif; line-height: 1.6; }
        .slide { border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 20px; }
        .slide h2 { margin-top: 0; }
        .quiz-question { margin-bottom: 12px; }
        .quiz-answers li { margin-left: 20px; }
        .tip { background: #f5f7fa; padding: 10px; border-left: 4px solid #4a90e2; margin-top: 12px; }
        .correct { color: #22ae35; }
        .instruct {}
        .cloze {}
    </style>
    """)

    html.append(f"<div class='course'><h1>{data.get('title','')}</h1>")

    for slide in data.get("slides", []):
        html.append("<div class='slide'>")
        html.append(f"<h2>{slide.get('title','')}</h2>")

        if slide.get("type") == "text":
            html.append(slide.get("text", ""))

        elif slide.get("type") == "single_choice":
            for i, q in enumerate(slide.get("questions", []), 1):
                html.append(f"<div class='quiz-question'><strong>{i}. {q['question']}</strong>")
                html.append("<ul class='quiz-answers'>")

                answers = [q["correct_answer"]] + q.get("wrong_answers", [])
                for i,ans in enumerate(answers):
                    html.append(f"<li class='{i==0 and "correct"}'>{ans}</li>")

                html.append("</ul></div>")

            if slide.get("tip"):
                html.append(f"<div class='tip'><strong>Tipp:</strong> {slide['tip']}</div>")

        elif slide.get("type") == "drag_text":
            html.append(f"<p class='instruct'><strong>{slide["user_instruction"]}</strong></p>")
            html.append(f"<p class='cloze'>{slide["cloze_text"]}</p>")
            
        html.append("</div>")

    html.append("</div>")
    return HTML("".join(html))
