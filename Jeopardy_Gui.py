import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
import Jeopardy_menu  # Importing the menu module where team names are entered

main_bg = '#333652'
fg = '#E9EAEC'
category_bg = '#333652'
button_bg = '#90ADC6'

class GUI:
    def __init__(self, root, main_bg, fg, category_bg, button_bg, team_one_name, team_two_name):
        self.root = root
        self.button_bg = button_bg
        self.main_bg = main_bg
        self.fg = fg
        self.category_bg = category_bg
        self.questions = []
        self.team_one_name = team_one_name  # Initialize team names from the parameter
        self.team_two_name = team_two_name
        self.setup_root()
        self.create_category_frame()
        self.create_button_frame()
        self.create_team_frame()

    def setup_root(self):
        self.root.geometry("1500x800")
        self.root.title("SDEV 265 - Jeopardy")
        self.root.configure(background=main_bg)

    def create_team_frame(self):
        label_frame = tk.Frame(self.root, background=(category_bg))
        
        team_label = tk.Label(label_frame, text=("Team Names"),font=('monospace', 30), background=(main_bg), foreground=(fg))
        team_label.grid(row=1, column=0, sticky="n", padx="5", pady="5"  )
        
        team_one_label = tk.Label(label_frame, text=f"Team One: {self.team_one_name}",font=('monospace', 20), background=(button_bg), foreground=(fg))
        team_one_label.grid(row=2, column=0, sticky='n', padx="5", pady="5"  )
        team_two_label = tk.Label(label_frame, text=f"Team Two: {self.team_two_name}",font=('monospace', 20), background=(button_bg), foreground=(fg))
        team_two_label.grid(row=3, column=0, sticky="n", padx="5", pady="5"  )
        
        label_frame.pack(fill="x")

    def create_category_frame(self):
        category_frame = tk.Frame(self.root, background=main_bg)
        
        for category_heading in range(6):
            category_frame.columnconfigure(category_heading, weight = 1)

        # Read categories from CSV
        categories = self.read_categories_from_csv('questions.csv')

        for category_title, category in enumerate(categories):
            category_label = tk.Label(category_frame, text=category, font=('monospace', 35), background=category_bg, foreground=fg)
            category_label.grid(row=0, column=category_title, sticky=tk.W+tk.E, padx="5", pady="5")

        category_frame.pack(fill="both")

    def read_categories_from_csv(self, filename):
        categories = []
        try:
            with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row['Category']
                    if category not in categories:
                        categories.append(category)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        return categories

    def create_button_frame(self):
        button_frame = tk.Frame(self.root, background=self.category_bg)

        # Read questions from CSV
        self.questions = self.read_questions_from_csv('questions.csv')

        # Configure columns to expand proportionally
        num_categories = len(self.questions)
        for column_index in range(num_categories):
            button_frame.grid_columnconfigure(column_index, weight=1)

        # Create buttons dynamically based on categories and values
        for category_index, category in enumerate(self.questions):
            for value_index, question in enumerate(category):
                button_text = f"${(value_index + 1) * 200}"
                button = tk.Button(button_frame, text=button_text, font=('monospace', 40), background=self.button_bg, foreground=self.fg)
                button.grid(row=value_index + 1, column=category_index, sticky=tk.W+tk.E, padx="5", pady="5")
                button.config(command=lambda q=question: self.show_question(q))

        """ # Add "Add Question" button
        add_question_button = tk.Button(button_frame, text="Add Question", font=('monospace', 20), background=self.button_bg, foreground=self.fg, command=self.add_question)
        add_question_button.grid(row=value_index + 2, column=num_categories // 2, columnspan=num_categories // 2, sticky=tk.W+tk.E, padx="5", pady="10") """

        button_frame.pack(fill="x")


    def read_questions_from_csv(self, filename):
        questions = [[] for _ in range(5)]  # 5 rows (values) per category
        try:
            with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row['Category']
                    value = row['Value']
                    question = {'Question': row['Question'], 'Answer': row['Answer']}
                    index = (int(value[1:]) // 200) - 1  # Calculate index based on value ($200, $400, etc.)
                    if index < 5:  # Ensure index is within range of 0-4 (for rows 0 to 4)
                        questions[index].append(question)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        return questions

    def show_question(self, question_data):
        question_text = question_data['Question']
        answer_text = question_data['Answer']

        # Display question in a messagebox
        messagebox.showinfo("Question", question_text)

        # Ask if user wants to see the answer
        show_answer = messagebox.askyesno("Show Answer", "Do you want to see the answer?")

        if show_answer:
            # Display answer in a messagebox
            messagebox.showinfo("Answer", answer_text)

    """ def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Question", command=self.add_question)

    def add_question(self):
        question = simpledialog.askstring("Input", "Enter question:")
        if not question:
            messagebox.showwarning("Input Error", "Question cannot be empty")
            return

        answer = simpledialog.askstring("Input", "Enter answer:")
        if not answer:
            messagebox.showwarning("Input Error", "Answer cannot be empty")
            return

        category = simpledialog.askstring("Input", "Enter category:")
        if not category:
            messagebox.showwarning("Input Error", "Category cannot be empty")
            return

        value = simpledialog.askstring("Input", "Enter value (e.g., $200, $400):")
        if not value:
            messagebox.showwarning("Input Error", "Value cannot be empty")
            return

        with open('questions.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([category, value, question, answer])

        messagebox.showinfo("Success", "Question added successfully!")
        print(question, answer) """

def start_game(team_one_name, team_two_name):
    root = tk.Tk()
    game_gui = GUI(root, main_bg, fg, category_bg, button_bg, team_one_name, team_two_name)
    root.mainloop()

if __name__ == "__main__":
    # Retrieve team names from Jeopardy_menu module
    team_one_name, team_two_name = Jeopardy_menu.get_team_names()

    # Start the game with retrieved team names
    start_game(team_one_name, team_two_name)
