import os
import logging


"""
Настройка логирования:
В файл bot.log и в стандартный вывод
"""


logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'bot.log')
    
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)