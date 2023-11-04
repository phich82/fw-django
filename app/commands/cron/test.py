import logging

logger = logging.getLogger("project")

def job():
    logger.info("crontab is running...")
    print('crontab is running...')
    with open('/usr/src/app/logs/testcron.txt', 'w') as f:
        f.write('Hello World')
    logger.info("crontab => end")
