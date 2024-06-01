import os
import pymorphy2

class Presets:
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    directory = parent_dir + '\presets'
    extension = '.modalpreset'

    @staticmethod
    def get_preset(preset):
        for root, dirs, files in os.walk(Presets.directory):
            for file in files:
                if file.endswith(Presets.extension) and file.startswith(preset):
                    return read_file(os.path.join(root, file))

    @staticmethod
    def get_banwords():
        script_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(script_dir)
        path = parent_dir + '/presets/banwords'

        print(path)
        with open(path, 'r', encoding='utf-8') as file:
            result = [line.strip() for line in file.readlines()]

        return result

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None