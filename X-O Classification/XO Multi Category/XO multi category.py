import customtkinter as ctk
import csv

grid_size = 5
categories = ["x", "o"]
W = {i: [0] * (grid_size * grid_size) for i in categories}
b = {i: 0 for i in categories}
alpha = 1
Theta = 0.2
training_file = "XO_training_data_multi.txt"

def f(Y_NI, theta):
    if Y_NI > theta:
        return 1
    elif Y_NI < theta * (-1):
        return -1
    else:
        return 0

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
    if label not in categories:
        result_label.configure(text=f"Invalid label. Enter one of: {', '.join(categories)}.")
        return

    ans.insert(0, label)
    with open(training_file, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(ans)
    
    result_label.configure(text="Pattern saved successfully.")

def train_multi_perceptron():
    global W, b
    try:
        with open(training_file, "r") as file:
            reader = csv.reader(file)
            dataset = []

            for row in reader:
                if len(row) < (grid_size * grid_size + 1):
                    continue
                label = row[0]
                inputs = [int(x) for x in row[1:]]
                dataset.append((label, inputs))

        epochs = 500
        for epoch in range(1, epochs):
            errors = 0
            for label, inputs in dataset:
                outputs = {}
                for cat in categories:
                    Y_NI = b[cat] + sum(W[cat][i] * inputs[i] for i in range(len(inputs)))
                    outputs[cat] = Y_NI

                predicted_label = max(outputs, key=outputs.get)

                if predicted_label != label:
                    errors += 1
                    for i in range(len(inputs)):
                        W[label][i] += alpha * inputs[i]
                    b[label] += alpha

            if errors == 0:
                result_label.configure(text=f"Training complete in {epoch} epochs.")
                break
        else:
            result_label.configure(text="Training complete with errors (max epochs reached).")

    except FileNotFoundError:
        result_label.configure(text="Training file not found. Save patterns first.")

def classify_pattern():
    ans = []
    for row in range(grid_size):
        for col in range(grid_size):
            if buttons[row][col].cget("fg_color") == "black":
                ans.append(1)
            else:
                ans.append(-1)

    outputs = {}
    for cat in categories:
        outputs[cat] = b[cat] + sum(W[cat][i] * ans[i] for i in range(len(ans)))

    predicted_label = max(outputs, key=outputs.get)
    result_label.configure(text=f"The input pattern is classified as '{predicted_label.upper()}'.")

def clear_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            buttons[row][col].configure(fg_color="white")

app = ctk.CTk()
app.title("5x5 XO Multi-Category Pattern Recognition")
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

input_label = ctk.CTkEntry(app, placeholder_text=f"Enter one of: {', '.join(categories)}")
input_label.grid(row=grid_size, column=0, columnspan=grid_size, pady=10)

save_button = ctk.CTkButton(app, text="Save Pattern", command=save_pattern)
save_button.grid(row=grid_size + 1, column=0, columnspan=grid_size // 2, pady=10)

train_button = ctk.CTkButton(app, text="Train Network", command=train_multi_perceptron)
train_button.grid(row=grid_size + 1, column=grid_size // 2, columnspan=grid_size // 2, pady=10)

classify_button = ctk.CTkButton(app, text="Classify Pattern", command=classify_pattern)
classify_button.grid(row=grid_size + 2, column=0, columnspan=grid_size, pady=10)

clear_button = ctk.CTkButton(app, text="Clear Grid", command=clear_grid)
clear_button.grid(row=grid_size + 3, column=0, columnspan=grid_size, pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.grid(row=grid_size + 4, column=0, columnspan=grid_size, pady=10)

app.mainloop()