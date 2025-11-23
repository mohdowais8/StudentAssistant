import tkinter as tk
from tkinter import messagebox, scrolledtext
import wikipedia
import random

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

# ---------------- GUI Functions ----------------
def make_notes():
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showerror("Error", "Topic cannot be empty!")
        return
    output_box.delete(1.0, tk.END)
    summary = fetch_wiki_summary(topic)
    notes = generate_notes(summary)
    output_box.insert(tk.END, notes)

def make_summary():
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showerror("Error", "Topic cannot be empty!")
        return
    output_box.delete(1.0, tk.END)
    summary = fetch_wiki_summary(topic)
    output_box.insert(tk.END, f"📝 Summary of {topic}\n\n{summary}")

def make_quiz():
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showerror("Error", "Topic cannot be empty!")
        return
    output_box.delete(1.0, tk.END)
    quiz = generate_quiz(topic)
    output_box.insert(tk.END, quiz)

def make_pro_tips():
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showerror("Error", "Topic cannot be empty!")
        return
    output_box.delete(1.0, tk.END)
    tips = generate_pro_tips(topic)
    output_box.insert(tk.END, tips)

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("BharatGPT - Wikipedia Student Assistant")
root.geometry("700x700")

title_label = tk.Label(root, text="BharatGPT - Wikipedia Notes Generator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

topic_label = tk.Label(root, text="Enter Topic:", font=("Arial", 12))
topic_label.pack()

topic_entry = tk.Entry(root, width=50, font=("Arial", 12))
topic_entry.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=80, height=30, font=("Arial", 10))
output_box.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

btn_notes = tk.Button(button_frame, text="Make Notes", width=15, command=make_notes)
btn_notes.grid(row=0, column=0, padx=5)

btn_summary = tk.Button(button_frame, text="Summary", width=15, command=make_summary)
btn_summary.grid(row=0, column=1, padx=5)

btn_quiz = tk.Button(button_frame, text="Quiz", width=15, command=make_quiz)
btn_quiz.grid(row=0, column=2, padx=5)

btn_tips = tk.Button(button_frame, text="Pro Tips", width=15, command=make_pro_tips)
btn_tips.grid(row=0, column=3, padx=5)

root.mainloop()
