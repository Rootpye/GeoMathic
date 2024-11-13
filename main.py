import tkinter as tk
from tkinter import messagebox
import sympy as sp
from sympy import symbols
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class FunctionGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoMathic")

        # Input field for function expression and add button
        self.expression_label = tk.Label(root, text="Enter Function (e.g., y = 2*x + 3, y = sin(x), y = exp(x)):")
        self.expression_label.pack()
        
        self.expression_entry = tk.Entry(root, width=30)
        self.expression_entry.pack()
        
        self.add_button = tk.Button(root, text="Add Function", command=self.add_expression)
        self.add_button.pack()

        # Input field to set x range
        self.range_label = tk.Label(root, text="Enter x range (e.g., -10, 10):")
        self.range_label.pack()
        
        self.range_entry = tk.Entry(root, width=30)
        self.range_entry.insert(0, "-10, 10")  # Default x range setting
        self.range_entry.pack()

        # Function list and plot button
        self.expressions = []
        self.plot_button = tk.Button(root, text="Plot Graphs", command=self.plot_graphs)
        self.plot_button.pack()

        # Initialize Matplotlib graph canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack()

        # Enable basic navigation tools for moving and zooming in Matplotlib
        self.ax.set_navigate(True)

    def add_expression(self):
        """Add the user-entered expression to the list"""
        expression = self.expression_entry.get().strip()
        if expression:
            try:
                # Split by `=` to check if it is an equation in terms of `y`
                if '=' not in expression:
                    raise ValueError("Function must be in the form 'y = ...'")
                
                lhs, rhs = expression.split('=')
                lhs, rhs = lhs.strip(), rhs.strip()
                
                if lhs != 'y':
                    raise ValueError("Function must start with 'y ='")

                # Parse the expression to check if it is valid
                parsed_expr = sp.sympify(rhs)  # Raises SympifyError if invalid
                self.expressions.append(parsed_expr)  # Add the function of y
                self.expression_entry.delete(0, tk.END)
                messagebox.showinfo("Added", f"Function '{expression}' added.")
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except sp.SympifyError:
                messagebox.showerror("Error", "Invalid function. Please enter a valid mathematical function.")
        else:
            messagebox.showerror("Error", "Please enter a valid function.")

    def parse_range(self):
        """Parse and return the x range entered by the user"""
        try:
            range_text = self.range_entry.get().strip()
            x_min, x_max = map(int, range_text.split(','))
            if x_min >= x_max:
                raise ValueError("Invalid range: minimum x should be less than maximum x.")
            return x_min, x_max
        except ValueError:
            messagebox.showerror("Error", "Invalid range format. Please enter range as two integers, e.g., '-10, 10'.")
            return None

    def plot_graphs(self):
        """Plot all the functions as graphs"""
        if not self.expressions:
            messagebox.showerror("Error", "No functions to plot. Please add functions first.")
            return

        # Parse the x-coordinate range
        x_range = self.parse_range()
        if not x_range:
            return  # Stop plotting if the x range is invalid

        x_min, x_max = x_range
        x_vals = np.linspace(x_min, x_max, 400)  # Generate continuous x values (400 points)
        x = symbols('x')

        # Clear the graph
        self.ax.clear()

        # Show the x and y axes to divide into four quadrants
        self.ax.axhline(0, color='black', linewidth=2)  # x-axis (horizontal line)
        self.ax.axvline(0, color='black', linewidth=2)  # y-axis (vertical line)

        for expr in self.expressions:
            try:
                # Convert to a lambda function compatible with numpy
                func = sp.lambdify(x, expr, modules=['numpy'])
                y_vals = func(x_vals)
                
                # Add function to the graph
                self.ax.plot(x_vals, y_vals, label=f"y = {sp.pretty(expr)}")
                
            except Exception as e:
                # Show message if an error occurs while plotting the function
                messagebox.showerror("Error", f"Could not plot function 'y = {sp.pretty(expr)}': {e}")
                continue  # Continue plotting the rest of the functions even if an error occurs

        # Automatically adjust the y-axis to include negative values
        self.ax.relim()
        self.ax.autoscale_view()

        # Graph settings
        self.ax.set_title("Function Graphs with 4 Quadrants")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        self.ax.grid(True)  # Add grid

        # Update the graph canvas
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionGraphApp(root)
    root.mainloop()
