class QuestionProcessor:
    def __init__(self):
        self.answer = "брут"

    def my_function(self, message):
        print(f"Вопрос: {message}\nОтвет: {self.answer}")

    def other_method(self, message):
        self.my_function(message)


message = "кто убил цезаря"
my_class = QuestionProcessor()
my_class.other_method(message)
