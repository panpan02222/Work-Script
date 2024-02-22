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
from tkinter import messagebox, filedialog


class Quiz:
    def __init__(self):
        self.current_question = 0
        self.mapping = {0:'A', 1:'B', 2:'C', 3:'D'}
        self.mapping_judge = {0:'√', 1:'×'}
        self.xlsx_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")],title="选择你的题库文件")
        self.questions, self.choices, self.solutions, self.types = self.get_questions_and_solutions()


    def get_questions_and_solutions(self):
        # 读取xlsx文件
        df = pd.read_excel(self.xlsx_path, sheet_name=None)

        # 获取问题和选项
        questions = []
        choices = []
        solutions = []
        types = []
        for sheet_name, sheet in df.items():
            questions.extend(sheet['question'].tolist())
            if sheet_name == "选择题":
                choices.extend(sheet[['A', 'B', 'C', 'D']].values.tolist())
                types.extend(["选择题"] * len(sheet))
            elif sheet_name == "判断题":
                choices.extend([['√', '×']] * len(sheet))
                types.extend(["判断题"] * len(sheet))
            else:
                choices.extend([[]]*len(sheet))
                types.extend(["填空题"] * len(sheet))
            solutions.extend(sheet['solution'].tolist())

        return questions, choices, solutions, types

    def check_answer(self):
        if self.types[self.current_question] == "判断题":
            user_choices = ''.join([self.mapping_judge[i.get()] for i in self.vars if i.get() != -1])
        elif self.types[self.current_question] == "填空题":
            user_choices = self.entry.get()
        else:
            user_choices = ''.join([self.mapping[i.get()] for i in self.vars if i.get() != -1])
        # 从solutions列表中获取当前问题的答案
        answer = self.solutions[self.current_question]
        # print(user_choices)
        # print(type(user_choices))
        # print(answer)
        # print(type(answer))
        if user_choices == answer:
            # messagebox.showinfo("结果", "你的答案是正确的！")
            pass
        else:
            messagebox.showinfo("结果", f"你的答案是错误的。正确答案是：{answer}")
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.update_question()
        else:
            self.root.quit()

    def update_question(self):
        for cb in self.check_buttons:
            cb.pack_forget()
        if hasattr(self, 'entry'):
            self.entry.pack_forget()
        if self.types[self.current_question] == "判断题":
            self.vars = [tk.IntVar(value=-1) for _ in range(len(self.choices[self.current_question]))]
            self.check_buttons = [tk.Checkbutton(self.root, text="", variable=var, onvalue=i, offvalue=-1, anchor='w') for i, var in enumerate(self.vars)]
        elif self.types[self.current_question] == "填空题":
            self.entry = tk.Entry(self.root)
            self.entry.pack()
        else:
            self.vars = [tk.IntVar(value=-1) for _ in range(len(self.choices[self.current_question]))]
            self.check_buttons = [tk.Checkbutton(self.root, text="", variable=var, onvalue=i, offvalue=-1, anchor='w') for i, var in enumerate(self.vars)]
        for i, choice in enumerate(self.choices[self.current_question]):
            if pd.isnull(choice):
                continue
            if self.types[self.current_question] == "选择题":
                self.check_buttons[i].config(text=f"{self.mapping[i]}. {choice}")
            else:
                self.check_buttons[i].config(text=choice)
            self.check_buttons[i].pack(anchor='w')
        if self.types[self.current_question] == "选择题" and len(self.solutions[self.current_question]) > 1:
            self.label.config(text="【多选】" + self.questions[self.current_question], wraplength=400)
        else:
            self.label.config(text=self.questions[self.current_question], wraplength=400)

    def run(self):
        self.root = tk.Tk()
        self.root.title("2024年安全学习考试题库")
        self.root.geometry("500x400")
        self.label = tk.Label(self.root)
        self.label.pack()

        self.vars = [tk.IntVar(value=-1) for _ in range(4)]
        self.check_buttons = [tk.Checkbutton(self.root, text="", variable=var, onvalue=i, offvalue=-1, anchor='w') for i, var in enumerate(self.vars)]
        for cb in self.check_buttons:
            cb.pack(anchor='w')

        button = tk.Button(self.root, text="下一题", command=self.check_answer)
        button.pack()

        self.update_question()

        self.root.mainloop()

if __name__ == "__main__":
    quiz = Quiz()
    quiz.run()





















