import random
import customtkinter as ctk

grid_size = 5
input_size = grid_size * grid_size
hidden_size = 10
output_size = 1
alpha = 0.1
epochs = 1000

input_weights = [[random.uniform(-0.5, 0.5) for _ in range(hidden_size)] for _ in range(input_size)]
hidden_weights = [random.uniform(-0.5, 0.5) for _ in range(hidden_size)]
input_bias = [random.uniform(-0.5, 0.5) for _ in range(hidden_size)]
hidden_bias = random.uniform(-0.5, 0.5)

def sigmoid(x):
    return 1 / (1 + (2.71 ** -x))

def sigmoid_derivative(x):
    return x * (1 - x)

def dot_product(v1, v2):
    return sum(v1[i] * v2[i] for i in range(len(v1)))

def feed_forward(inputs, input_weights, hidden_weights, input_bias, hidden_bias):
    hidden_layer_input = [dot_product(inputs, [input_weights[j][k] for j in range(len(inputs))]) + input_bias[k] for k in range(len(hidden_weights))]
    hidden_layer_output = [sigmoid(x) for x in hidden_layer_input]

    output_input = dot_product(hidden_layer_output, hidden_weights) + hidden_bias
    output = sigmoid(output_input)

    return hidden_layer_output, output

def feed_backward(inputs, hidden_output, output, target, input_weights, hidden_weights, input_bias, hidden_bias, alpha):
    output_error = target - output
    output_delta = output_error * sigmoid_derivative(output)

    hidden_errors = [output_delta * hidden_weights[k] for k in range(len(hidden_weights))]
    hidden_deltas = [hidden_errors[k] * sigmoid_derivative(hidden_output[k]) for k in range(len(hidden_weights))]

    for k in range(len(hidden_weights)):
        hidden_weights[k] += alpha * hidden_output[k] * output_delta
    hidden_bias += alpha * output_delta

    for k in range(len(input_weights[0])):
        for j in range(len(inputs)):
            input_weights[j][k] += alpha * inputs[j] * hidden_deltas[k]
        input_bias[k] += alpha * hidden_deltas[k]

    return input_weights, hidden_weights, input_bias, hidden_bias

def train_mlp(data, labels):
    global input_weights, hidden_weights, input_bias, hidden_bias

    for epoch in range(epochs):
        total_loss = 0
        for i in range(len(data)):
            hidden_output, output = feed_forward(data[i], input_weights, hidden_weights, input_bias, hidden_bias)
            loss = (labels[i] - output) ** 2
            total_loss += loss
            input_weights, hidden_weights, input_bias, hidden_bias = feed_backward(
                data[i], hidden_output, output, labels[i],
                input_weights, hidden_weights, input_bias, hidden_bias, alpha
            )
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {total_loss / len(data)}")

def predict(inputs):
    _, output = feed_forward(inputs, input_weights, hidden_weights, input_bias, hidden_bias)
    return 1 if output >= 0.5 else -1

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

    with open(training_file, "a") as file:
        file.write(",".join(map(str, ans)) + "\n")
    result_label.configure(text="Pattern saved successfully.")

def train_network():
    try:
        with open(training_file, "r") as file:
            data = []
            labels = []
            for line in file:
                row = list(map(int, line.strip().split(",")))
                labels.append(row[0])
                data.append(row[1:])
        train_mlp(data, labels)
        result_label.configure(text="Training complete.")
    except FileNotFoundError:
        result_label.configure(text="Training file not found.")

def classify_pattern():
    ans = []
    for row in range(grid_size):
        for col in range(grid_size):
            if buttons[row][col].cget("fg_color") == "black":
                ans.append(1)
            else:
                ans.append(-1)

    prediction = predict(ans)
    if prediction == 1:
        result_label.configure(text="The pattern is classified as an 'X'.")
    else:
        result_label.configure(text="The pattern is classified as an 'O'.")

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

train_button = ctk.CTkButton(app, text="Train Network", command=train_network)
train_button.grid(row=grid_size + 1, column=grid_size // 2, columnspan=grid_size // 2, pady=10)

classify_button = ctk.CTkButton(app, text="Classify Pattern", command=classify_pattern)
classify_button.grid(row=grid_size + 2, column=0, columnspan=grid_size, pady=10)

clear_button = ctk.CTkButton(app, text="Clear Grid", command=clear_grid)
clear_button.grid(row=grid_size + 3, column=0, columnspan=grid_size, pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.grid(row=grid_size + 4, column=0, columnspan=grid_size, pady=10)

training_file = "XO_training_data2.txt"

app.mainloop()