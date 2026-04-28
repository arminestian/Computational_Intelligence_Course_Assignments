import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

TrainingSet = [
    [1, 1, 1, 1],
    [1, -1, 1, -1],
    [-1, 1, 1, -1],
    [-1, -1, 1, -1]
]

w1, w2, b = 0, 0, 0

def train_hebb():
    global w1, w2, b
    for i in range(len(TrainingSet)):
        Delta_w1 = TrainingSet[i][0] * TrainingSet[i][3]
        Delta_w2 = TrainingSet[i][1] * TrainingSet[i][3]
        Delta_b = TrainingSet[i][2] * TrainingSet[i][3]

        w1 += Delta_w1
        w2 += Delta_w2
        b += Delta_b

        plot_decision_boundary(i + 1)

        root.update()
        plt.pause(1.5)

def plot_decision_boundary(iteration):
    ax.clear()

    for point in TrainingSet:
        x, y, _, label = point
        if label == 1:
            ax.scatter(x, y, color="blue", label="+1" if iteration == 1 else "", s=100)
        else:
            ax.scatter(x, y, color="red", label="-1" if iteration == 1 else "", s=100)

    if w2 != 0:
        x_vals = [-2, 2]
        y_vals = [-(w1 * x + b) / w2 for x in x_vals]
        ax.plot(x_vals, y_vals, color="black", label="Decision Boundary")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
    ax.set_title(f"Iteration {iteration}: w1={w1}, w2={w2}, b={b}")
    ax.legend(loc="upper left")

    canvas.draw()

root = tk.Tk()
root.title("Perceptron Training Visualization")

fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

train_button = tk.Button(root, text="Train Hebb", command=train_hebb)
train_button.pack()

root.mainloop()

x1, x2 = map(int, input().split())
y = b + (w1 * x1) + (w2 * x2)
if y >= 0:
    print(1)
else:
    print(-1)