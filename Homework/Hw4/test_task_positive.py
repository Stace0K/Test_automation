import yaml
from checkers import getout
from sshcheckers import ssh_checkout, upload_files, ssh_getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def logging(self, starttime, name):
        with open(name, 'w') as f:
            f.write(getout("journalctl --since '{}'".format(starttime)))

    def test_step1(self, start_time):
        res = []
        upload_files(data["host"], data["user"], data["passwd"], data["pack_name"] + ".deb",
                     "/home/{}/{}.deb".format(data["user"], data["pack_name"]))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -i"
                                                                            " /home/{}/{}.deb".format(data["passwd"],
                                                                                                      data["user"],
                                                                                                      data[
                                                                                                          "pack_name"]),
                                "Настраивается пакет"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo '{}' | "
                                                                            "sudo -S dpkg -s {}".format(data["passwd"],
                                                                                                        data[
                                                                                                            "pack_name"]),
                                "Status: install ok installed"))
        self.logging(start_time, "logging.txt")
        assert all(res), "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, start_time):
        res1 = ssh_checkout(data["host"], data["user"], data["passwd"], "cd {};"
                                                                        " 7z a {}/arx2".format(data["folder_in"],
                                                                                               data["folder_out"]),
                            "Everything is Ok")
        res2 = ssh_checkout(data["host"], data["user"], data["passwd"], "ls {}".format(data["folder_out"]), "arx2.7z")
        self.logging(start_time, "logging.txt")
        assert res1 and res2, "test2 FAIL"

    def test_step3(self, clear_folders, make_files, start_time):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z a "
                                                                            "{}/arx2".format(data["folder_in"],
                                                                                             data["folder_out"]),
                                "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z e "
                                                                            "arx2.7z -o{} -y".format(data["folder_out"],
                                                                                                     data[
                                                                                                         "folder_ext"]),
                                "Everything is Ok"))
        for item in make_files:
            res.append(
                ssh_checkout(data["host"], data["user"], data["passwd"], "ls {}".format(data["folder_ext"]), item))
        self.logging(start_time, "logging.txt")
        assert all(res), "test3 FAIL"

    def test_step4(self, start_time):
        self.logging(start_time, "logging.txt")
        assert ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z t"
                                                                        " arx2.7z".format(data["folder_out"]),
                            "Everything is Ok"), "test4 FAIL"

    def test_step5(self, start_time):
        self.logging(start_time, "logging.txt")
        assert ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z u"
                                                                        " arx2.7z".format(data["folder_in"]),
                            "Everything is Ok"), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, start_time):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z a "
                                                                            "{}/arx2".format(data["folder_in"],
                                                                                             data["folder_out"]),
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z l"
                                                                                " arx2.7z".format(data["folder_out"],
                                                                                                  data["folder_ext"]),
                                    item))
        self.logging(start_time, "logging.txt")
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder, start_time):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z a "
                                                                            "{}/arx".format(data["folder_in"],
                                                                                            data["folder_out"]),
                                "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "cd {};"
                                                                            " 7z x arx.7z -o{} -y".format(
            data["folder_out"], data["folder_ext2"]), "Everything is Ok"))

        for item in make_files:
            res.append(
                ssh_checkout(data["host"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]), item))

        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]),
                                make_subfolder[0]))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], "ls {}/{}".format(data["folder_ext2"],
                                                                                              make_subfolder[0]),
                                make_subfolder[1]))
        self.logging(start_time, "logging.txt")
        assert all(res), "test7 FAIL"

    def test_step8(self, start_time):
        self.logging(start_time, "logging.txt")
        assert ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z d arx.7z".format(data["folder_out"]),
                            "Everything is Ok"), "test8 FAIL"

    def test_step9(self, start_time):
        result = []
        result.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -r"
                                                                            " {}".format(data["passwd"],
                                                                                         data["pack_name"]),
                                "Удаляется"))
        result.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo '{}' | "
                                                                            "sudo -S dpkg -s {}".format(data["passwd"],
                                                                                                        data[
                                                                                                            "pack_name"]),
                                "Status: deinstall ok"))
        assert all(result), "test10 FAIL"
