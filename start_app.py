import subprocess
import time

from logger import logger

 
while True:
    logger.debug('Start application ...')
    
    logger.debug('Start chunks.py ...')
    subprocess.call(['python', 'chunks.py'])
    
    logger.debug('Start create_db.py ...')
    subprocess.call(['python', 'create_db.py'])
    
    logger.debug('Start tg_bot.py ...')
    subprocess.call(['python', 'tg_bot.py'])
    
    time.sleep(0.1)
    
    logger.debug('Application is running.')
