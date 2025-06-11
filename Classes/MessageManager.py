# contents of the MessageManager class in python

from queue import Queue


class MessageQueue():
    """
    Class for the MessageManager

    Contains a queue which is responsible for outputting information to the user
    """

    def __init__(self):
        self.queue = Queue()
        self.previous_message = "" #keeps track of previous messages in case they must be repeated

    def add_to_queue(self, string):
        """
        Function for adding string values to the queue
        """

        self.queue.put(string)

    def output_queue(self):
        """
        Function for outputting the next item from the queue
        """
        return self.queue.get()

    def empty_queue(self):
        """
        Function for emptying the queue
        """
        self.queue = Queue()