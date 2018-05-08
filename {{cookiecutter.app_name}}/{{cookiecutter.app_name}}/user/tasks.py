from ..extensions import celery


@celery.task()
def dummy_task():
    print "Hello World from task"
    return "OK"
