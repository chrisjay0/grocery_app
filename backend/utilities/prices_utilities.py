class Queue(object):
    def __init__(self):
        self.in_stack = []
        self.out_stack = []
    
    def enqueue(self, data):
        self.in_stack.append(data)
    
    def peek(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack[-1]
        
    def dequeue(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack.pop()
    
    def size(self):
        return len(self.in_stack) + len(self.out_stack)
    
    def is_empty(self):
        return self.size() == 0
    