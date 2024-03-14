import argparse
import glob
import multiprocessing as mp
import numpy as np
import tempfile
import time
import warnings
import cv2
import tqdm
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM,TextIteratorStreamer
from threading import Thread
import torch,sys,os
import json
import pandas

sys.path.insert(0, "./")  # noqa
from demo.predictors import VisualizationDemo
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import LazyConfig, instantiate
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

def setup(args):
    cfg = LazyConfig.load(args.config_file)
    cfg = LazyConfig.apply_overrides(cfg, args.opts)
    return cfg
def get_parser():
    parser = argparse.ArgumentParser(description="detrex demo for visualizing customized inputs")
    parser.add_argument(
        "--config-file",
        default="projects/dino/configs/dino_r50_4scale_12ep.py",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")

    parser.add_argument("--gradio", nargs="+", help="A Gradio",)

    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )
    parser.add_argument(
        "--min_size_test",
        type=int,
        default=800,
        help="Size of the smallest side of the image during testing. Set to zero to disable resize in testing.",
    )
    parser.add_argument(
        "--max_size_test",
        type=float,
        default=1333,
        help="Maximum size of the side of the image during testing.",
    )
    parser.add_argument(
        "--img_format",
        type=str,
        default="RGB",
        help="The format of the loading images.",
    )
    parser.add_argument(
        "--metadata_dataset",
        type=str,
        default="coco_2017_val",
        help="The metadata infomation to be used. Default to COCO val metadata.",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    parser.add_argument("--model_name_or_path", type=str, help='mode name or path')

    parser.add_argument("--is_4bit", action='store_true', help='use 4bit model')

    return parser

# 标签映射字典
class_mapping = {
    0 : "bengbian",
    1 : 'unjoined_weld',
    2 : 'zangpian',
    3 : 'loujiang',
    4 : 'crack',
    5 : 'scratch',
    6 : 'black_spot',
    7 : 'broken_gate',
    8 : 'thick_line',
    9 : 'duanshan',
    10 : 'linear_crack',
    11 : 'black_core',
    12 : 'finger'
}

with gr.Blocks() as interface:
    gr.Markdown("""<h1><center>王朝阳多模态缺陷检测大模型前端Demo</center></h1>""")
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(label='输入图片进行推理')
            img_submit_button = gr.Button(value="提交推理", variant='primary')
            conf = gr.Slider(0, 1, value=0, step=0.0001, label="置信度")
        with gr.Column():
            output_img = gr.Image(label='检测后图片输出')
            predictions = gr.Textbox(label='推理结果调试窗口', lines=4)
    with gr.Row():
        with gr.Column():
            gr.CheckboxGroup(choices=['大语言模型接入', '大语言模型辅助推理', '多轮对话学习'], label='多模态接入')
            llm_type = gr.Dropdown(choices=['llama_7B', 'llama2_13B', 'Atom_7B'], label='选择语言模型')
            msg = gr.Textbox(lines=6, label="对话输入")
            state = gr.State()
            with gr.Row():
                clear = gr.Button("新话题")
                re_generate = gr.Button("重新回答")
                sent_bt = gr.Button("发送", variant='primary')
            with gr.Accordion("生成参数", open=False):
                slider_temp = gr.Slider(minimum=0, maximum=1, label="temperature", value=0.3)
                slider_top_p = gr.Slider(minimum=0.5, maximum=1, label="top_p", value=0.95)
                slider_context_times = gr.Slider(minimum=0, maximum=5, label="上文轮次", value=2, step=2.0)
        chatbot = gr.Chatbot()

    def user(user_message, history):
        return "", history + [[user_message, None]]
    def bot(history,temperature,top_p, slider_context_times):
        if pandas.isnull(history[-1][1]) == False:
            history[-1][1] = None
            yield history
        slider_context_times = int(slider_context_times)
        history_true = history[1:-1]
        prompt = ''
        if slider_context_times>0:
            prompt += '\n'.join([("<s>Human: "+one_chat[0].replace('<br>','\n')+'\n</s>' if one_chat[0] else '')  +"<s>Assistant: "+one_chat[1].replace('<br>','\n')+'\n</s>'    for one_chat in history_true[-slider_context_times:] ])
        prompt +=  "<s>Human: "+history[-1][0].replace('<br>','\n')+"\n</s><s>Assistant:"
        input_ids = tokenizer([prompt], return_tensors="pt",add_special_tokens=False).input_ids[:,-512:].to('cuda')        
        generate_input = {
            "input_ids":input_ids,
            "max_new_tokens":512,
            "do_sample":True,
            "top_k":50,
            "top_p":top_p,
            "temperature":temperature,
            "repetition_penalty":1.3,
            "streamer":streamer,
            "eos_token_id":tokenizer.eos_token_id,
            "bos_token_id":tokenizer.bos_token_id,
            "pad_token_id":tokenizer.pad_token_id
        }
        thread = Thread(target=llm_model.generate, kwargs=generate_input)
        thread.start()
        start_time = time.time()
        bot_message =''
        print('Human:',history[-1][0])
        print('Assistant: ',end='',flush=True)
        for new_text in streamer:
            print(new_text,end='',flush=True)
            if len(new_text)==0:
                continue
            if new_text!='</s>':
                bot_message+=new_text
            if 'Human:' in bot_message:
                bot_message = bot_message.split('Human:')[0]
            history[-1][1] = bot_message
            yield history
        end_time =time.time()
        print()
        print('生成耗时：',end_time-start_time,'文字长度：',len(bot_message),'字耗时：',(end_time-start_time)/len(bot_message))

    # 推理单张图片函数
    def infer_img(input_image, confidence_threshold, llm_type):
        predictions, visualized_output = demo.run_on_image(input_image, confidence_threshold)  # Key!!
        print(predictions)
        print('aaaaaaaaaaaaa')
        print(predictions['instances'].num_instances)
        img_out = visualized_output.get_image()
        img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
        return img_out, predictions

    # 输出内容参考
    # {
    #     'instances': Instances(
    #         num_instances=1, 
    #         image_height=1024, 
    #         image_width=1024, 
    #         fields=[
    #             pred_boxes: Boxes(tensor([[ 27.0954, 331.9492, 333.3728, 608.2092]], device='cuda:0')), 
    #             scores: tensor([0.5853], device='cuda:0'), 
    #             pred_classes: tensor([10], device='cuda:0')]
    #         )
    #     }
    
    def perdiction_convert_text(predictions):

        # 提取检测数量
        num_instances = predictions['instances'].get('num_instances')

        # 提取box位置
        xyxy = predictions['instances'].pred_boxes.tensor.cpu().numpy().tolist()

        # 提取类别index, convert chinese classes
        pred_classes_ = predictions['instances'].pred_classes.tensor.cpu().numpy().tolist()
        classess_list = []
        for i in pred_classes_:
            classess_list.append(
                class_mapping[i]
            )

        # 提取置信度
        conf = predictions['instances'].scores.tensor.cpu().numpy()

        prompt = f"这是一张太阳能光伏板图片, 属于__数据集。在图片内的__{xyxy}位置, 存在__{num_instances}个__{classess_list}缺陷,置信度为:__{conf}。"
        return prompt

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot,slider_temp,slider_top_p,slider_context_times], chatbot
    )
    sent_bt.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot,slider_temp,slider_top_p,slider_context_times], chatbot
    )
    re_generate.click(bot, [chatbot,slider_temp,slider_top_p,slider_context_times], chatbot )

    img_submit_button.click(infer_img, [input_img, conf,llm_type], [output_img, predictions])

    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    cfg = setup(args)
    model = instantiate(cfg.model)
    model.to(cfg.train.device)
    checkpointer = DetectionCheckpointer(model)
    checkpointer.load(cfg.train.init_checkpoint)

    model.eval()

    demo = VisualizationDemo(
        model=model,
        min_size_test=args.min_size_test,
        max_size_test=args.max_size_test,
        img_format=args.img_format,
        metadata_dataset=args.metadata_dataset,)

# LLM部分
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path,use_fast=False)
    tokenizer.pad_token = tokenizer.eos_token
    if args.is_4bit==False:
        llm_model = AutoModelForCausalLM.from_pretrained(args.model_name_or_path,
                                                     device_map='cuda:0' if torch.cuda.is_available() else "auto",
                                                     torch_dtype=torch.float16,
                                                     load_in_8bit=True,
                                                     trust_remote_code=True,
                                                     use_flash_attention_2=True)
        llm_model.eval()
    else:
        from auto_gptq import AutoGPTQForCausalLM
        llm_model = AutoGPTQForCausalLM.from_quantized(args.model_name_or_path,low_cpu_mem_usage=True, device="cuda:0", use_triton=False,inject_fused_attention=False,inject_fused_mlp=False)
    streamer = TextIteratorStreamer(tokenizer,skip_prompt=True)
    if torch.__version__ >= "2" and sys.platform != "win32":
        llm_model = torch.compile(llm_model)
    interface.queue().launch(share=True, debug=True,server_name="0.0.0.0")

# -----------------------
'''
python demo/chat_gradio.py \
--config-file projects/dab_detr/configs/dab_detr_r50_50ep.py \
--model_name_or_path /home/wangzhaoyang/wzytest/Llama2_Chinese_7b_Chat/ \
--opts train.init_checkpoint="./dab_detr_r50_50ep.pth"
'''
