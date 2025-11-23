import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import wikipedia
import random
from fpdf import FPDF

# ---------------- Helper Functions ----------------
def fetch_wiki_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=5, auto_suggest=True, redirect=True)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple options found for '{topic}'. Try more specific.\nOptions: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{topic}'."
    except Exception as e:
        return f"Error fetching summary: {e}"

def generate_notes(summary):
    lines = summary.split('. ')
    notes = ["📌 Notes (Auto-generated from Wikipedia)", "-"*50]
    for line in lines:
        if line.strip():
            notes.append("• " + line.strip())
    return "\n".join(notes)

def generate_quiz(topic):
    words = topic.split()
    if not words:
        words = ["topic"]
    quiz = ["❓ Quiz Questions", "-"*40]
    for i in range(1, 11):
        word = random.choice(words)
        quiz.append(f"{i}. Explain the term '{word}' in detail.")
    return "\n".join(quiz)

def generate_pro_tips(topic):
    tips = [
        f"• Break down {topic} into subtopics for easier understanding.",
        f"• Make diagrams or charts to visualize {topic}.",
        f"• Connect {topic} with real-life examples.",
        f"• Revise {topic} regularly for exams.",
        f"• Try answering previous questions on {topic}."
    ]
    return "💡 Pro Tips:\n" + "-"*40 + "\n" + "\n".join(tips)

# ---------------- PDF Export ----------------
def save_as_pdf(content, filename="BharatGPT_Notes.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 6, line)
    pdf.output(filename)
    messagebox.showinfo("Saved", f"Content saved as {filename}")

# ---------------- GUI Functions ----------------
def process_single_topic(topic, action):
    summary = fetch_wiki_summary(topic)
    if action == "notes":
        return generate_notes(summary)
    elif action == "summary":
        return f"📝 Summary of {topic}\n\n{summary}"
    elif action == "quiz":
        return generate_quiz(topic)
    elif action == "tips":
        return generate_pro_tips(topic)
    else:
        return summary

def run_action(action):
    topics = topic_entry.get().strip()
    if not topics:
        messagebox.showerror("Error", "Topic cannot be empty!")
        return
    output_box.delete(1.0, tk.END)
    all_topics = [t.strip() for t in topics.split(',') if t.strip()]
    final_output = ""
    for t in all_topics:
        final_output += process_single_topic(t, action) + "\n\n"
    output_box.insert(tk.END, final_output)

def save_output_pdf():
    content = output_box.get(1.0, tk.END).strip()
    if not content:
        messagebox.showerror("Error", "Nothing to save!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
    if file_path:
        save_as_pdf(content, file_path)

def toggle_dark_mode():
    if root["bg"] == "white":
        root.config(bg="#2e2e2e")
        output_box.config(bg="#3b3b3b", fg="white", insertbackground="white")
        labels = [title_label, topic_label]
        for l in labels:
            l.config(bg="#2e2e2e", fg="white")
    else:
        root.config(bg="white")
        output_box.config(bg="white", fg="black", insertbackground="black")
        labels = [title_label, topic_label]
        for l in labels:
            l.config(bg="white", fg="black")

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("BharatGPT - Pro Student Assistant")
root.geometry("750x750")
root.config(bg="white")

title_label = tk.Label(root, text="BharatGPT - Pro Wikipedia Notes Generator", font=("Arial", 16, "bold"), bg="white")
title_label.pack(pady=10)

topic_label = tk.Label(root, text="Enter Topic(s) (comma-separated):", font=("Arial", 12), bg="white")
topic_label.pack()

topic_entry = tk.Entry(root, width=55, font=("Arial", 12))
topic_entry.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=90, height=30, font=("Arial", 10))
output_box.pack(pady=10)

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=5)

btn_notes = tk.Button(button_frame, text="Make Notes", width=15, command=lambda: run_action("notes"))
btn_notes.grid(row=0, column=0, padx=5)

btn_summary = tk.Button(button_frame, text="Summary", width=15, command=lambda: run_action("summary"))
btn_summary.grid(row=0, column=1, padx=5)

btn_quiz = tk.Button(button_frame, text="Quiz", width=15, command=lambda: run_action("quiz"))
btn_quiz.grid(row=0, column=2, padx=5)

btn_tips = tk.Button(button_frame, text="Pro Tips", width=15, command=lambda: run_action("tips"))
btn_tips.grid(row=0, column=3, padx=5)

btn_save = tk.Button(button_frame, text="Save as PDF", width=15, command=save_output_pdf)
btn_save.grid(row=1, column=1, pady=5)

btn_dark = tk.Button(button_frame, text="Toggle Dark Mode", width=15, command=toggle_dark_mode)
btn_dark.grid(row=1, column=2, pady=5)

root.mainloop()
