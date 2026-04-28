import customtkinter as ctk
import csv

grid_size = 5
W = [0] * (grid_size * grid_size)
b = 0
training_file = "XO_training_data.txt"

def change_color(row, col):
    if buttons[row][col].cget("fg_color") == "white":
        buttons[row][col].configure(fg_color="black")
    else:
        buttons[row][col].configure(fg_color="white")

def save_pattern():
    ans = []
    for row in range(grid_size):
        for col in range(grid_size):
            if buttons[row][col].cget("fg_color") == "black":
                ans.append(1)
            else:
                ans.append(-1)
    
    label = input_label.get().strip().lower()
    if label == 'x':
        ans.insert(0, 1)
    elif label == 'o':
        ans.insert(0, -1)
    else:
        result_label.configure(text="Invalid label. Enter 'x' or 'o'.")
        return

    with open(training_file, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(ans)
    
    result_label.configure(text="Pattern saved successfully.")

def train_hebb_network():
    global W, b
    W = [0] * (grid_size * grid_size)
    b = 0
    try:
        with open(training_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < (grid_size * grid_size + 1):
                    continue
                
                label = int(row[0])
                inputs = [int(x) for x in row[1:]]
                
                for i in range(len(inputs)):
                    W[i] += inputs[i] * label
                b += label
        
        result_label.configure(text="Training complete.")
    except FileNotFoundError:
        result_label.configure(text="Training file not found. Save patterns first.")

def classify_pattern():
    global W, b
    ans = []
    for row in range(grid_size):
        for col in range(grid_size):
            if buttons[row][col].cget("fg_color") == "black":
                ans.append(1)
            else:
                ans.append(-1)

    y = b
    for i in range(len(ans)):
        y += W[i] * ans[i]
    
    if y >= 0:
        result_label.configure(text="The input pattern is classified as an 'X'.")
    else:
        result_label.configure(text="The input pattern is classified as an 'O'.")

def clear_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            buttons[row][col].configure(fg_color="white")

app = ctk.CTk()
app.title("5x5 XO Pattern Recognition")
app.geometry("350x600")

buttons = []
for row in range(grid_size):
    button_row = []
    for col in range(grid_size):
        button = ctk.CTkButton(app, text="", width=60, height=60, fg_color="white",
                               command=lambda r=row, c=col: change_color(r, c))
        button.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(button)
    buttons.append(button_row)

input_label = ctk.CTkEntry(app, placeholder_text="Enter 'x' or 'o'")
input_label.grid(row=grid_size, column=0, columnspan=grid_size, pady=10)

save_button = ctk.CTkButton(app, text="Save Pattern", command=save_pattern)
save_button.grid(row=grid_size + 1, column=0, columnspan=grid_size // 2, pady=10)

train_button = ctk.CTkButton(app, text="Train Network", command=train_hebb_network)
train_button.grid(row=grid_size + 1, column=grid_size // 2, columnspan=grid_size // 2, pady=10)

classify_button = ctk.CTkButton(app, text="Classify Pattern", command=classify_pattern)
classify_button.grid(row=grid_size + 2, column=0, columnspan=grid_size, pady=10)

clear_button = ctk.CTkButton(app, text="Clear Grid", command=clear_grid)
clear_button.grid(row=grid_size + 3, column=0, columnspan=grid_size, pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.grid(row=grid_size + 4, column=0, columnspan=grid_size, pady=10)

app.mainloop()