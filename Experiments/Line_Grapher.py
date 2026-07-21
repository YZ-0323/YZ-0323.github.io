import tkinter as tk
from tkinter import messagebox
import math

safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}

def plot_function():
    expr = entry.get()
    canvas.delete("all")
    try:
        width, height = 600, 400
        scale = 20  

        canvas.create_line(0, height//2, width, height//2, fill="black")  # x轴
        canvas.create_line(width//2, 0, width//2, height, fill="black")  # y轴

        prev = None
        for px in range(width):
            x = (px - width / 2) / scale
            try:
                y = eval(expr, {"x": x, **safe_dict})
                py = height / 2 - y * scale
                if prev:
                    canvas.create_line(prev[0], prev[1], px, py, fill="blue")
                prev = (px, py)
            except:
                prev = None  
    except Exception as e:
        messagebox.showerror("错误", f"无法绘制函数图像：\n{e}")

# GUI 设置
root = tk.Tk()
root.title("简单函数图像显示器")

entry = tk.Entry(root, width=40)
entry.insert(0, "x**2")
entry.pack(pady=5)

button = tk.Button(root, text="绘制图像", command=plot_function)
button.pack(pady=5)

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

root.mainloop()
