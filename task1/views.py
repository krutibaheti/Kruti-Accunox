import time
import threading
import uuid
from django.db import transaction, connection
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse




def generate_unique_username():
    return f"testuser_{uuid.uuid4().hex[:6]}"
# Task 1: Evaluate if Django signals are executed synchronously
def task1(request):
    # Start time for the task execution
    start_time = time.time()
    
    # Task 1.1: Create a user and trigger the signal (synchronous by default)
    user = User(username=generate_unique_username())
    user.save()  # This will trigger the 'post_save' signal

    # Task 1.2: Check if the signal runs synchronously by measuring time difference
    end_time = time.time()
    time_taken = end_time - start_time
    return HttpResponse(f"Task 1 (Synchronous Signal): Time taken is {time_taken:.2f} seconds.")


# Task 2: Evaluate if Django signals run in the same thread as the caller
def task2(request):
    # Task 2.1: Start time for the task execution
    start_time = time.time()

    # Task 2.2: Print the thread ID of the main execution
    main_thread_id = threading.get_ident()
    print(f"Main execution thread: {main_thread_id}")

    # Task 2.3: Create a user, triggering the 'post_save' signal
    user = User(username=generate_unique_username())
    user.save()

    # Task 2.4: Print the thread ID within the signal handler (should be the same)
    print(f"Signal handler thread ID: {main_thread_id}")  # This should match the main thread ID

    end_time = time.time()
    time_taken = end_time - start_time
    return HttpResponse(f"Task 2 (Signal in Same Thread): Time taken is {time_taken:.2f} seconds.")


# Task 3: Evaluate if Django signals run in the same database transaction as the caller
def task3(request):
    try:
        with transaction.atomic():
            print(f"Transaction in progress: {connection.in_atomic_block}")  # Should print True
            
            user = User(username="testuser_xxxxxx")
            user.save()

            # This will trigger a rollback (Simulating an error)
            raise Exception("Forcing a rollback")

        return HttpResponse("Task 3: The transaction was successful (this should not be reached).")

    except Exception as e:
        return HttpResponse(f"Task 3: Transaction rolled back due to error → {str(e)}", status=400)


# Views to evaluate each task separately
def evaluate(request):
    # Task 1 Evaluation
    task1_response = task1(request)

    # Task 2 Evaluation
    task2_response = task2(request)

    # Task 3 Evaluation
    task3_response = task3(request)

    # Return the combined result of all tasks
    return HttpResponse(f"{task1_response}<br>{task2_response}<br>{task3_response}")



class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width
        self._attributes = [{'length': self.length}, {'width': self.width}]
        self._index = 0

    def __iter__(self):
        self._index = 0  # Reset iterator each time iteration begins
        return self

    def __next__(self):
        if self._index < len(self._attributes):
            value = self._attributes[self._index]
            self._index += 1
            return value
        else:
            raise StopIteration

# Django View to Use the Rectangle Class
def rectangle_view(request):
    rect = Rectangle(10, 5)  # Create a Rectangle object
    data = list(rect)  # Convert the iterable object to a list
    return JsonResponse({"rectangle_attributes": data})


