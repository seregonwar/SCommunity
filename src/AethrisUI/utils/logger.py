import logging
import sys
from typing import Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LogConfig:
    level: int = logging.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[Path] = None
    console: bool = True

class Logger:
    @staticmethod
    def setup(config: LogConfig):
        logger = logging.getLogger("aethris")
        logger.setLevel(config.level)
        
        if config.console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(config.format))
            logger.addHandler(console_handler)
            
        if config.file:
            file_handler = logging.FileHandler(str(config.file))
            file_handler.setFormatter(logging.Formatter(config.format))
            logger.addHandler(file_handler) 