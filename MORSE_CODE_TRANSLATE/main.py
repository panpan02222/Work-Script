#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/01/31 09:48:27
@Author  :   pan binghong 
@Email   :   19909442097@163.com
@description   莫斯密码翻译器,最终可打包成exe文件:   
'''

# 定义摩斯密码字典
MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}



# 测试
# def main():
#     message = "你是谁"
#     result = encrypt(message.upper())
#     print (result)

#     message = ".... . .-.. .-.. ---  .-- --- .-. .-.. -.."
#     result = decrypt(message)
#     print (result)

# if __name__ == '__main__':
#     main()


import tkinter as tk
from tkinter import messagebox

# 你的摩斯密码字典和函数在这里
# 函数来加密/解密
def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            cipher += ' '
    return cipher

def decrypt(message):
    message += ' '
    decipher = ''
    citext = ''
    for letter in message:
        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2 :
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''
    return decipher

def encrypt_message():
    message = input_text.get("1.0", 'end-1c')
    result = encrypt(message.upper())
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def decrypt_message():
    message = input_text.get("1.0", 'end-1c')
    result = decrypt(message)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

root = tk.Tk()
root.title("摩斯密码转换器")

input_label = tk.Label(root, text="输入:")
input_label.pack()

input_text = tk.Text(root, height=10, width=30)
input_text.pack()

encrypt_button = tk.Button(root, text="加密", command=encrypt_message)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="解密", command=decrypt_message)
decrypt_button.pack()

output_label = tk.Label(root, text="输出:")
output_label.pack()

output_text = tk.Text(root, height=10, width=30)
output_text.pack()

root.mainloop()
