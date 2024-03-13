import gradio as gr
# import cv2

# def process_image_and_text(image, text):
#     # 将图片转换为灰度图像
#     gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
#     # 获取文本的前五个字符
#     first_five_chars = text[:5]
#     return gray, first_five_chars

# # 创建Gradio接口
# interface = gr.Interface(fn=process_image_and_text, inputs=[gr.Image(), gr.Textbox()], outputs=['image', 'text'])

# # 启动接口
# interface.launch(debug=True)



print('6666666666666666666666666666')
input_list = [
    gr.Image(label='输入图像', type='numpy'),
    gr.Slider(minimum=0, maximum=1, step=0.0001, label="置信度"),
    gr.Checkbox(label='大语言模型辅助推理')
]

output_list = [
    gr.Image(label='检测结果输出', type='numpy'),
    gr.Textbox(label='文字输出')
]


def input_and_output(input_image, confidence_threshold, llm):
    print('+++', input_image)
    return input_image, confidence_threshold

interface = gr.Interface(fn=input_and_output,
                            inputs=input_list,
                            outputs=output_list,
                            title='王朝阳的实验demo',
                            description='多模态缺陷检测GUI',
                            live=False
                            )
interface.launch()