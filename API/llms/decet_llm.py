


    if args.gradio:
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
            # print('+++', input_image)
            return input_image, confidence_threshold

        interface = gr.Interface(fn=input_and_output,
                                 inputs=input_list,
                                 outputs=output_list,
                                 title='王朝阳的实验demo',
                                 description='多模态缺陷检测GUI',
                                 live=False
                                 )
        interface.launch()

if args.gradio:
    print('6666666666666666666666666666')
    input_list = [
        gr.Image(label='输入图像', type='numpy'),
        gr.Slider(minimum=0, maximum=1, step=0.0001, label="置信度"),
        gr.Checkbox(label='大语言模型辅助推理')
    ]

    def input_and_output(input_image, confidence_threshold, llm, output_list):
        # print('+++', input_image)
        output_list = [
            gr.Image(label='检测结果输出', type='numpy', value=input_image),
            gr.Textbox(label='文字输出', value=str(confidence_threshold))
        ]
        return output_list

    interface = gr.Interface(fn=input_and_output,
                             inputs=input_list,
                             outputs='auto',
                             title='王朝阳的实验demo',
                             description='多模态缺陷检测GUI',
                             live=False
                             )
    interface.launch()
    
if args.gradio:
    print('6666666666666666666666666666')
    input_list = [
        gr.Image(label='输入图像', type='numpy'),
        gr.Slider(minimum=0, maximum=1, step=0.0001, label="置信度"),
        gr.Checkbox(label='大语言模型辅助推理')
    ]

    def input_and_output(input_image, confidence_threshold, llm):
        # print('+++', input_image)
        return input_image, str(confidence_threshold)

    output_list = [
        gr.Image(label='检测结果输出', type='numpy'),
        gr.Textbox(label='文字输出')
    ]

    interface = gr.Interface(fn=input_and_output,
                             inputs=input_list,
                             outputs=output_list,
                             title='王朝阳的实验demo',
                             description='多模态缺陷检测GUI',
                             live=False
                             )
    interface.launch()

