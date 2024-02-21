#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/02/21 11:16:13
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''

import pandas as pd
import tkinter as tk
from tkinter import messagebox
from utils.module import get_questions_and_solutions

# 读取xlsx文件
# 获取单选题的问题和答案
def get_questions_and_solutions(xlsx_path):
    # 读取xlsx文件
    df = pd.read_excel(xlsx_path)

    # 获取问题和选项
    questions = df['question'].tolist()
    choices = df[['A', 'B', 'C', 'D']].values.tolist()
    solutions = df['solution'].tolist()

    return questions,choices,solutions
questions, choices, solutions = get_questions_and_solutions(r'Question-and-answer tool\Put_excel_here\test.xlsx')

# 当前问题的索引
current_question = 0
mapping = {'0':'A', '1':'B', '2':'C', '3':'D'}

def check_answer():
    global current_question
    user_choices = [mapping[str(i.get())] for i in vars if i.get() != -1]
    # 从solutions列表中获取当前问题的答案
    answer = solutions[current_question]
    if set(user_choices) == set(answer):
        # messagebox.showinfo("结果", "你的答案是正确的！")
        pass
    else:
        messagebox.showinfo("结果", f"你的答案是错误的。正确答案是：{answer}")
    current_question += 1
    if current_question < len(questions):
        update_question()
    else:
        root.quit()

def update_question():
    label.config(text=questions[current_question])
    for i, choice in enumerate(choices[current_question]):
        check_buttons[i].config(text=choice)
        vars[i].set(-1)

root = tk.Tk()
root.title("2024年安全学习考试题库")
root.geometry("500x400")
label = tk.Label(root)
label.pack()

vars = [tk.IntVar(value=-1) for _ in range(4)]
check_buttons = [tk.Checkbutton(root, text="", variable=var, onvalue=i, offvalue=-1, anchor='w') for i, var in enumerate(vars)]
for cb in check_buttons:
    cb.pack(anchor='w')

button = tk.Button(root, text="下一题", command=check_answer)
button.pack()

update_question()

root.mainloop()

