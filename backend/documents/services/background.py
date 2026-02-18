import threading


def run_in_background(target_function, *args):
    """
    Runs the given function in a separate background thread.
    This is a lightweight placeholder for a real task queue.
    """

    thread = threading.Thread(
        target=target_function,
        args=args,
        daemon=True  # Dies when main process exits
    )
    thread.start()
