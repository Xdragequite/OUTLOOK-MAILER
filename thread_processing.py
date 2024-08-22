class ThreadType():
    def __init__(self):
        self.container = []
    def append_params(self,email, content, subject, file_path):
        dictionary = {'email':email, 'content_path':content, 'subject':subject, 'file_path':file_path}
        self.container.append(dictionary)