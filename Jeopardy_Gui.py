import tkinter as tk
from tkinter import simpledialog, messagebox
import csv

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
        self.team_one_name = team_one_name
        self.team_two_name = team_two_name
        self.category_bg = category_bg
        self.setup_root()
        self.create_category_frame()
        self.create_button_frame()
        self.create_team_frame()
        
    def setup_root(self):
        self.root.geometry("1500x800")
        self.root.title("SDEV 265 - Jeopardy")
        self.root.configure(background=(main_bg))
        
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

        category_frame = tk.Frame(self.root, background=(main_bg))

        for category_heading in range(6):
            category_frame.columnconfigure(category_heading, weight = 1)
            
        categories = self.read_categories_from_csv('categories.csv')

        for category_title, category in enumerate(categories):
            category_label = tk.Label(category_frame, text=category, font=('monospace', 25), background=(category_bg), foreground=(fg))
            category_label.grid(row=0, column=category_title, sticky=tk.W+tk.E, padx="5", pady="5")
            
        category_frame.pack(fill="x")
        
    def read_categories_from_csv(self, filename):
        categories = []
        try:
            with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                for row in reader:
                    categories.extend(row)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        return categories          
         
    def create_button_frame(self):
        button_frame = tk.Frame(self.root, background=(category_bg))
        for button_value in range(6):
            button_frame.columnconfigure(button_value, weight=1)

        for button_value in range(6):
            button = tk.Button(button_frame, text="$200",font=('monospace', 40), background=(button_bg), foreground=(fg))
            button.grid(row=1, column=button_value, sticky=tk.W+tk.E, padx="5", pady="5" )
            button = tk.Button(button_frame, text="$400",font=('monospace', 40), background=(button_bg), foreground=(fg))
            button.grid(row=2, column=button_value, sticky=tk.W+tk.E, padx="5", pady="5"  )
            button = tk.Button(button_frame, text="$600",font=('monospace', 40), background=(button_bg), foreground=(fg))
            button.grid(row=3, column=button_value, sticky=tk.W+tk.E, padx="5", pady="5"  )
            button = tk.Button(button_frame, text="$800",font=('monospace', 40), background=(button_bg), foreground=(fg))
            button.grid(row=4, column=button_value, sticky=tk.W+tk.E, padx="5", pady="5"  )
            button = tk.Button(button_frame, text="$1000",font=('monospace', 40), background=(button_bg), foreground=(fg))
            button.grid(row=5, column=button_value, sticky=tk.W+tk.E, padx="5", pady="5"  )
            
        button_frame.pack(fill="x")

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Question", command=self.add_question)
    
    def get_questions(self):
        category = simpledialog.askstring("Input", "Enter category: ")
        if not category:
            messagebox.showwarning("Input error", "You must enter a category.")
            return
    
        value = simpledialog.askinteger("Input", "Enter value ($200, $400, etc.): ")
        if not value or value not in [200, 400, 600, 800, 1000]:
            messagebox.showwarning("Input error", "Invalid value.")
            return
        
        question = simpledialog.askstring("Input", "Enter your question: ")
        if not question:
            messagebox.showwarning("Input error", "Question cannot be empty.")
            return
        
        answer = simpledialog.askstring("Input", "Enter your answer: ")
        if not answer:
            messagebox.showwarning("Input error", "Answer cannot be empty.")
            return
        
        messagebox.showinfo("Done", "Question added.")
        
def start_game(team_one_name, team_two_name):
    root = tk.Tk()
    game_gui = GUI(root, main_bg, fg, category_bg, button_bg, team_one_name, team_two_name)
    root.mainloop()
        
if __name__ == "__main__":
    team_one_name = "Team One"
    team_two_name = "Team Two"
    start_game(team_one_name, team_two_name)