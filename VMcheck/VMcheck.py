# -*- coding: utf-8 -*-
from pyVim import connect
from pyVmomi import vim
import requests
import urllib3
urllib3.disable_warnings()

ip = "10.11.8.39"
VMUser = "root"
VMPass = "P@ssw0rd"

WinUser = "Administrator"
WinPass = 'P"ssw0rd'

LinUser = "root"
LinPass = "toor"


si = connect.SmartConnectNoSSL(host=ip, user=VMUser, pwd=VMPass)
content = si.RetrieveContent()
vms = content.rootFolder.childEntity[0].vmFolder.childEntity
for vm in vms:
    print("=" * 50, "\n", vm.summary.config.name, " - ", vm.summary.runtime.powerState, " - ", vm.summary.guest.toolsStatus)
    guestsname = vm.summary.config.guestFullName
    if "poweredOn" in vm.summary.runtime.powerState:
        if "Windows" in guestsname:
            try:
                creds = vim.vm.guest.NamePasswordAuthentication(username=WinUser, password=WinPass)
                pm = content.guestOperationsManager.processManager
                ps = vim.vm.guest.ProcessManager.ProgramSpec(programPath="C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", arguments='Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\* | Select-Object DisplayName | Out-File C:\\temp.txt')
                pm.StartProgramInGuest(vm, creds, ps)
                r = ""
                while r == "":
                    try:
                        fti = content.guestOperationsManager.fileManager.InitiateFileTransferFromGuest(vm, creds, "C:\\temp.txt").url.replace("*", ip)
                        r = requests.get(fti, verify=False).content.decode("utf-16")
                    except:
                        pass
                print("-" * 50, "\n", "WinSDP = ", "WinSCP" in r, "\n", "Java Update = ", "Java" in r, "\n Curl = True")
            except:
                print("Check connect -", vm.summary.config.name)
        else:
            try:
                creds = vim.vm.guest.NamePasswordAuthentication(username=LinUser, password=LinPass)
                pm = content.guestOperationsManager.processManager
                ps = vim.vm.guest.ProcessManager.ProgramSpec(programPath="/bin/rpm", arguments='-qa | grep "tcpdump\|net-tools\|lynx\|dnsutils\|ftp\|lftp\|sshpass\|curl\|open-vm-tools"> /root/temp.txt')
                pm.StartProgramInGuest(vm, creds, ps)
                r = ""
                while r == "":
                    try:
                        fti = content.guestOperationsManager.fileManager.InitiateFileTransferFromGuest(vm, creds, "/root/temp.txt").url.replace("*", ip)
                        r = requests.get(fti, verify=False).content.decode("utf-8")
                    except:
                        pass
                print("-" * 50, "\n", r)
            except:
                print("Check connect -", vm.summary.config.name)
