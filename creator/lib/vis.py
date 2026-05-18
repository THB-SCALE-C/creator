from IPython.display import HTML
import re

def render_learning_content(data):
    blank_pattern = re.compile(r"\*([^*]+)\*")

    html = []
    append = html.append

    # Basic CSS for readability in Jupyter
    append("""
    <style>
        .course { font-family: Arial, sans-serif; line-height: 1.6;}
        .slide { border: 1px solid #333; border-radius: 8px; padding: 16px; margin-bottom: 20px; }
        .slide h2 { margin-top: 0; }
        .quiz-question { margin-bottom: 12px; }
        .quiz-answers li { margin-left: 20px; }
        .tip { background: #f5f7fa; padding: 10px; border-left: 4px solid #4a90e2; margin-top: 12px; color: #000000;}
        .correct { color: #22ae35; }
        .feedback-positive { background: #eef9f0; padding: 10px; border-left: 4px solid #22ae35; margin-top: 12px; color: #000000; }
        .feedback-negative { background: #fff1f1; padding: 10px; border-left: 4px solid #d64545; margin-top: 12px; color: #000000;}
        .instruct {}
        .cloze {}
        .blank-box {
            display: inline-block;
            min-width: 80px;
            padding: 0 8px;
            margin: 0 2px;
            border: 1px solid #333;
            border-radius: 4px;
            text-align: center;
            vertical-align: baseline;
        }
    </style>
    """)

    append(f"<div class='course'><h1>{data.get('title','')}</h1>")

    for slide in data.get("slides", []):
        append("<div class='slide'>")
        append(f"<h2>{slide.get('title','')}</h2>")

        slide_type = slide.get("slide_type") or slide.get("type")

        if slide_type == "text":
            append(slide.get("text", ""))

        elif slide_type == "single_choice":
            items = slide.get("question_items") or slide.get("questions") or []
            for q_idx, q in enumerate(items, 1):
                question = q.get("question", "")
                append(f"<div class='quiz-question'><strong>{q_idx}. {question}</strong>")
                append("<ul class='quiz-answers'>")

                answers = [q.get("correct_answer", "")] + (q.get("wrong_answers") or [])
                for a_idx, ans in enumerate(answers):
                    css = "correct" if a_idx == 0 else ""
                    append(f"<li class='{css}'>{ans}</li>")

                append("</ul></div>")

            if slide.get("tip"):
                append(f"<div class='tip'><strong>Tipp:</strong> {slide['tip']}</div>")
            if slide.get("positive_feedback"):
                append(
                    f"<div class='feedback-positive'><strong>Positive Feedback:</strong> {slide['positive_feedback']}</div>"
                )
            if slide.get("negative_feedback"):
                append(
                    f"<div class='feedback-negative'><strong>Negative Feedback:</strong> {slide['negative_feedback']}</div>"
                )

        elif slide_type == "drag_text":
            append(f"<p class='instruct'><strong>{slide.get('user_instruction', '')}</strong></p>")
            cloze_text = slide.get("cloze_text", "")
            cloze_text = blank_pattern.sub(
                lambda m: f"<span class='blank-box' data-answer='{m.group(1)}'>{m.group(1)}</span>",
                cloze_text,
            )
            append(f"<p class='cloze'>{cloze_text}</p>")
            distractors = slide.get("distractors") or []
            if distractors:
                append("<div><strong>Distractors:</strong> " + ", ".join(distractors) + "</div>")

        evidences = slide.get("evidences") or []
        if evidences:
            append("<div class='tip'><strong>Evidence:</strong> " + ", ".join(map(str, evidences)) + "</div>")

        append("</div>")

    append("</div>")
    return HTML("".join(html))
