# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
# в котором вывод разбивается на слова с удалением всех знаков пунктуации
# (их можно взять из списка string.punctuation модуля string).
# В этом режиме должно проверяться наличие слова в выводе.

import string
import subprocess


def task_func_upd(cmd: str, text: str) -> bool:
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    res = result.stdout
    without_punc = res.translate(str.maketrans('', '', string.punctuation))
    lst = without_punc.split()
    if text in lst and result.returncode == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    print(task_func_upd('cat /etc/os-release', 'Jammy'))


