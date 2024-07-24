from sshcheckers import ssh_checkout, upload_files

def deploy():
    res = []
    upload_files("0.0.0.0", "ak", "4444", "p7zip-full.deb", "/home/ak/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "ak", "4444", "echo '4444' | sudo -S dpkg -i /home/ak/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "ak", "4444", "echo '4444' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)

if deploy():
    print("Деплой успешен")
else:
    print("Ошибка деплоя")