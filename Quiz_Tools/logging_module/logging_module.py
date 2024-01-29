import logging  
import datetime  
  
class LoggingManager:  
    def __init__(self, log_file):  
        self.log_file = log_file  
        self.logger = logging.getLogger(__name__)  
        self.logger.setLevel(logging.INFO)  
        self.handler = None  
  
    def setup_handler(self):  
        self.handler = logging.FileHandler(self.log_file)  
        self.handler.setLevel(logging.INFO)  
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
        self.handler.setFormatter(formatter)  
        self.logger.addHandler(self.handler)  

    def log_input(self, input_message):    
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
        self.logger.info(f"{current_time} - 输入信息：{input_message}")

    def log_answer(self, answer):  
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        self.logger.info(f"{current_time} - {answer}")  

# 使用示例：  
# logging_manager = LoggingManager('classify_and_chat.log')  
# logging_manager.setup_handler()  
# logging_manager.log_answer('Hello, world!')