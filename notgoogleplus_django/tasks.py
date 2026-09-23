import logging
import time

from celery import Task, shared_task

logger = logging.getLogger(__name__)

class TimingTask(Task):
    """Custom base class to log execution time for all tasks."""
    
    def __call__(self, *args, **kwargs):
        start_time = time.perf_counter()
        
        # Execute the actual task
        result = super().__call__(*args, **kwargs)
        
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Task {self.name}[{self.request.id}] took {duration:.4f} seconds")
        
        return result

# Apply it to your tasks by passing the base parameter
@shared_task(base=TimingTask)
def process_data_task(data):
    # Do work here; timing is handled automatically
    pass
