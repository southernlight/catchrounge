from app.common.scheduler import TableExpireScheduler

def init_scheduler(table_repository):
    scheduler = TableExpireScheduler(table_repository)
    scheduler.start()
    return scheduler
