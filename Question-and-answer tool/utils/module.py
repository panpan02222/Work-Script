#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   module.py
@Time    :   2024/02/21 15:09:26
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   :   
'''
import pandas as pd
import tkinter as tk
from tkinter import messagebox

class Question:
    def __init__(self, question, choices, solution, current_question = 0, mappping = {'0':'A', '1':'B', '2':'C', '3':'D'}):
        self.question = question
        self.choices = choices
        self.solution = solution
        self.current_question = current_question
        self.mapping = mappping
    # 获取单选题的问题和答案
    @staticmethod
    def get_questions_and_solutions(xlsx_path):
        # 读取xlsx文件
        df = pd.read_excel(xlsx_path)

        # 获取问题和选项
        question = df['question'].tolist()
        choices = df[['A', 'B', 'C', 'D']].values.tolist()
        solutions = df['solution'].tolist()

        return question,choices,solutions


    def check_answer():
        global current_question
        user_choices = [self.mapping[str(i.get())] for i in vars if i.get() != -1]
        # 从solutions列表中获取当前问题的答案
        answer = self.solutions[current_question]
        if set(user_choices) == set(answer):
            # messagebox.showinfo("结果", "你的答案是正确的！")
            pass
        else:
            messagebox.showinfo("结果", f"你的答案是错误的。正确答案是：{answer}")
        current_question += 1
        if current_question < len(self.questions):
            update_question()
        else:
            root.quit()

    def update_question(self):
        pass







class ChoiceQuestion(Question):
    def __init__(self, question, choices, solution):
        super().__init__(question, choices, solution)

    def check_answer(self, user_answer):
        # 检查用户的答案是否正确
        pass

    def update_question(self):
        # 更新问题
        pass

class TrueFalseQuestion(Question):
    def __init__(self, question, solution):
        super().__init__(question, None, solution)

    def check_answer(self, user_answer):
        # 检查用户的答案是否正确
        pass

    def update_question(self):
        # 更新问题
        pass

class FillInBlankQuestion(Question):
    def __init__(self, question, solution):
        super().__init__(question, None, solution)

    def check_answer(self, user_answer):
        # 检查用户的答案是否正确
        pass

    def update_question(self):
        # 更新问题
        pass




# 获取单选题的问题和答案
def get_questions_and_solutions(xlsx_path):
    # 读取xlsx文件
    df = pd.read_excel(xlsx_path)

    # 获取问题和选项
    questions = df['question'].tolist()
    choices = df[['A', 'B', 'C', 'D']].values.tolist()
    solutions = df['solution'].tolist()

    return questions,choices,solutions
    # 输出问题和选项
    for i in range(len(questions)):
        print(f"问题{i+1}: {questions[i]}")
        print(f"选项: {choices[i]}")
        print(f'答案: {solutions[i]}')

# 获取多选题的问题和答案

# 获取填空题的问题和答案
        
# 获取判断题的问题和答案

# 获取简答题的问题和答案




# if __name__ == '__main__':
#     q,c,s = get_questions_and_solutions('Put_excel_here/test.xlsx')
#     # 输出问题和选项
#     for i in range(len(q)):
#         print(f"问题{i+1}: {q[i]}")
#         print(f"选项: {c[i]}")
#         print(f'答案: {s[i]}')

