# Дополнить проект тестами, проверяющими команды вывода списка файлов (l)
# и разархивирования с путями (x).


import subprocess


folder_in = "/home/user/tst"
folder_out = "/home/user/out"
folder_ext = "/home/user/folder1"
folder_ext2 = "/home/user/folder2"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    # test1
    result1 = checkout("cd {}; 7z a {}/arx2".format(folder_in, folder_out), "Everything is Ok")
    result2 = checkout("ls {}".format(folder_out), "arx2.7z")
    assert result1 and result2, "test1 FAIL"


def test_step2():
    # test2
    result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(folder_out, folder_ext), "Everything is Ok")
    result2 = checkout("ls {}".format(folder_ext), "t1")
    result3 = checkout("ls {}".format(folder_ext), "t2")
    assert result1 and result2 and result3, "Test2 FAIL"


def test_step3():
    # test3
    assert checkout(f"cd {folder_out}; 7z t arx2.7z", "Everything is Ok"), "Test3 FAIL"


def test_step4():
    # test4
    assert checkout(f"cd {folder_in}; 7z u {folder_out}/arx2.7z", "Everything is Ok"), "Test4 FAIL"


def test_step5():
    # test5: проверка команды списка вывода файлов
    result2 = checkout("cd {}; 7z l arx2.7z".format(folder_out, folder_ext), "t1.txt")
    result3 = checkout("cd {}; 7z l arx2.7z".format(folder_out, folder_ext), "t2.txt")
    assert result2 and result3, "test5 FAIL"


def test_step6():
    # test6: проверка команды разархивирования с путями
    result1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(folder_out, folder_ext2), "Everything is Ok")
    result2 = checkout("ls {}".format(folder_ext2), "t1")
    result3 = checkout("ls {}".format(folder_ext2), "t2")
    assert result1 and result2 and result3, "test6 FAIL"


def test_step7():
    # test7
    assert checkout(f"cd {folder_out}; 7z d arx2.7z", "Everything is Ok"), "Test7 FAIL"



