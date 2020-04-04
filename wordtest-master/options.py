class Options():
    YES = 1
    NO = 2
    NONE = 3

    def option(self, question, default_answer):
        while True:
            selection = input("{} {}: ".format(question,
                                               '(y/n)' if default_answer is self.NONE else '(Y/n)' if default_answer is self.YES else '(y/N)'))
            if selection.lower() in ["n", "no"]:
                return False
            elif selection.lower() not in ["y", "yes"] and selection is not '':
                print("Please select y or n")
            elif selection.lower() in ['y', 'yes']:
                return True
            elif selection.lower() in ['\n', '']:
                if default_answer is self.YES:
                    return True
                elif default_answer is self.NO:
                    return False

    def retry(self):
        return self.option('Would you like to try the whole set again?', self.NO)

    def pronunciation(self):
        return self.option('Show pronunciation?', self.YES)

    def retry_failed(self):
        return self.option('Would you like to try the failed words again?', self.YES)

    def shuffle(self):
        return self.option('Shuffle the words?', self.NO)
