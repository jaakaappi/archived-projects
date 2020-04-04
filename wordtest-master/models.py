class Answer:
    def __init__(self, correct, word, meaning, answer):
        self.correct = correct
        self.word = word
        self.meaning = meaning
        self.answer = answer
    def __repr__(self):
        return "Word: {}, correct answer: {}, your answer: {}. {}".format(self.word, self.meaning, self.answer,"Correct!" if self.correct else "Wrong...")