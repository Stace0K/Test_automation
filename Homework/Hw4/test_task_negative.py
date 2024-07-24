import yaml
from sshcheckers import ssh_checkout_negative, ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_step1(self, make_folders, make_bad_arx):
        result = ssh_checkout_negative(data["host"], data["user"], data["passwd"],
                                       "cd {}; 7z e {}.{} -o{} -y".format(data["folder_out"], make_bad_arx,
                                                                          data["type"],
                                                                          data["folder_ext"]), "ERROR:")
        assert result, "test1 FAIL"

    def test_step2(self):
        result = []
        result.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -r"
                                                                               " {}".format(data["passwd"],
                                                                                            data["pack_name"]),
                                   "Удаляется"))
        result.append(ssh_checkout(data["host"], data["user"], data["passwd"], "echo '{}' | "
                                                                               "sudo -S dpkg -s {}".format(
            data["passwd"],
            data["pack_name"]),
                                   "Status: deinstall ok"))
        assert all(result), "test2 FAIL"
