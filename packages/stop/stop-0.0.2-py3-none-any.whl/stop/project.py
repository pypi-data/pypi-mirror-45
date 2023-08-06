import canvas_object
import queue
import threading
import time



class Project:
    def __init__(self, fps=60):
        self.sprites = {}
        self.canvas_object = canvas_object.CanvasObject()
        self.queue = queue.Queue()
        self.fps = fps
        self.frame_time_ms = int(1000/fps)
        self.frame_time = 1/fps

        # event lists
        self.green_flag_events = []

    def run(self):
        self.canvas_object.root.after(self.frame_time_ms, self.frame)
        self.send_green_flag_event()
        self.canvas_object.root.mainloop()

    def frame(self):
        for _ in range(self.queue.qsize()):
            item = self.queue.get()
            item_function = item['function']
            item_parameters = item['parameters']
            item_function(item_parameters)
            self.queue.task_done()

        self.canvas_object.root.after(self.frame_time_ms, self.frame)

    def wait(self, seconds=False):
        if not seconds:
            seconds = self.frame_time
        time.sleep(seconds)

    # EVENTS

    def send_green_flag_event(self):
        # use threads
        threads = []
        for method in self.green_flag_events:
            temp_thread = threading.Thread(target=method, daemon=True)
            threads.append(temp_thread)

        for thread in threads:
            thread.start()


    def green_flag(self, function):
        self.green_flag_events.append(function)






