import argparse, json, models, random
import options
from os import listdir, getcwd, path
from sys import exit

argparser = argparse.ArgumentParser()
argparser.add_argument('file', help="Dictionary filename")


def parse_args(args):
    return argparser.parse_args()


def load_dictionary():
    directory = path.dirname(path.abspath(__file__)) + '\dictionaries'
    files = [f for f in listdir(directory) if path.isfile(directory + '\\' + f) and f.endswith('.json')]

    if len(files) is 0:
        print('No .json files in dictionaries folder')
        return ''

    while True:
        i = 0
        for file in files:
            i += 1
            print('{}: {}'.format(i, file))
        selected_file_number = input('Select a file from the list above: ')
        try:
            selected_file_number = int(selected_file_number)
            if selected_file_number > len(files) or selected_file_number == 0:
                print('Please select a number from the list')
            else:
                try:
                    with open(path.join(directory, str(files[int(selected_file_number) - 1])), 'r+',
                              encoding="utf-8") as file:
                        words = file.read()
                        return json.loads(words, encoding="utf-8")
                except Exception as e:
                    print('Error opening file {}: {}'.format(files[int(selected_file_number - 1)], str(e)))
        except Exception as e:
            print('Please input a number')


def from_foreign(option):
    words_list = load_dictionary()
    if len(words_list) is 0:
        return
    do_shuffle = option.shuffle()
    if do_shuffle:
        random.shuffle(words_list)
    pronunciation_enabled = option.pronunciation()

    while (True):
        answers = []
        correct_count = 0

        print("Translate the words.")
        for word in words_list:
            if pronunciation_enabled:
                answer = input("{} ({}): ".format(word['word'], word['pronunciation']))
            else:
                answer = input("{}: ".format(word['word']))
            answer_correct = True if answer in word['translations'] else False
            if answer_correct:
                print("Correct!")
            else:
                print("Wrong, the correct translation is", ", ".join(word['translations']))

            answers.append(models.Answer(answer_correct, word['word'],
                                         " ".join(word['translations']), answer))
        for answer in answers:
            if answer.correct:
                correct_count = correct_count + 1
            print(answer)

        print("{} correct out of {}".format(correct_count, len(answers)))
        if correct_count != len(answers) and option.retry_failed():
            new_list = []
            for word in words_list:
                for answer in answers:
                    if answer.word == word['word']:
                        if not answer.correct:
                            new_list.append(word)
                        break
            words_list = new_list
            if do_shuffle:
                random.shuffle(words_list)
        elif not option.retry():
            return


def to_foreign():
    pass


def add_word():
    pass


commands = {}


def print_help(options):
    for command in commands:
        print("{}:  {}".format(command['name'], command['description']))


def parse_commands(filename):
    try:
        with open(filename) as file:
            global commands
            commands = json.loads(file.read())
            for command in commands:
                if command['command'] not in globals():
                    return 'Invalid command "{}", check {}'.format(command, filename), {}
            return '', commands
    except Exception as e:
        return 'Could not parse command file {}: {}'.format(filename, str(e)), {}


def main():
    option = options.Options()
    message, commands = parse_commands('commands.json')

    if message != '':
        print(message)
        exit()

    print("Input command: 'help' for list of commands")
    while (True):
        input_command = input(">")
        for command in commands:
            if command['name'] == input_command:
                globals()[command['command']](option)
                break
        else:
            print('Unknown command')


if __name__ == "__main__":
    main()
