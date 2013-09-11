from celery import task


@task()
def test():
    return "test"
