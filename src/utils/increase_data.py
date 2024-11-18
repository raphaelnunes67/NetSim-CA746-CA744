import os


def increase_txt_file(n_lines_begin: int, n_lines_final: int) -> bool:
    if n_lines_final % n_lines_begin != 0:
        return False

    factor = int(n_lines_final / n_lines_begin)

    files = os.listdir()
    print(files)

    for file in files:
        if file != 'increase_data.py':
            with open(file, 'r') as txt_file:
                content = txt_file.readlines()

            with open(file, 'w') as txt_file:
                txt_file.write('')

            content_normalized = []

            for i in range(len(content)):
                aux = content[i].replace('\x00', '').replace('ÿþ', '').strip()
                if aux != '':
                    content_normalized.append(aux)

            print(content_normalized)

            with open(file, 'a') as txt_file:
                for item in content_normalized:
                    for i in range(factor):
                        txt_file.write(item + '\n')

    return True


def increase_csv_file():
    pass


if __name__ == '__main__':
    increase_txt_file(96, 1440)
