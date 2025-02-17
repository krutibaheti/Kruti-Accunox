import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Task 1: Signal Handler (Proving the signal runs in the same thread)
@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    # Task 1.1: Signal handler runs in the same thread as the caller
    print(f"Signal running in thread: {threading.get_ident()}")  # Same thread ID as the main view

    print("Signal started...")
    time.sleep(5)  # Introduce a delay to simulate work in the signal
    print("Signal finished.")