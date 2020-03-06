# -*- coding: utf-8 -*-
import time
import re
import os
from threading import Thread

import netmiko
from flask import Flask, render_template, request, redirect, url_for

ip = "127.0.0.1"
# ip = "10.11.14.202"
username = "cisco"
password = "cisco"
secret = "cisco"
tftp = "tftp://192.168.254.199/"
path = r"C:\Program Files\Tftpd64"

pathconf = os.getcwd() + "\\conf\\"
ranges = range(7001, 7049)
settings = {"HQ": [], "BR": [], "ISP": [], "SW3": [], "SW2": [], "SW1": [], "FW1": []}
status = {}
active = {i: True for i in ranges}

app = Flask(__name__, template_folder='templates')

good = sorted(['BR1              Fas 0/12', 'HQ1              Fas 0/1', 'SW2              Fas 0/6', 'SW2              Fas 0/5', 'SW3              Fas 0/4', 'SW3              Fas 0/3'])

def dialog(net_connect, command, word="confirm"):
    output = net_connect.send_command_timing(command, strip_command=False, strip_prompt=False)
    if word in output:  # custom
        output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
    elif "Unexpected answer" in output:  # Unexpected answer
        output += net_connect.send_command_timing("n", strip_command=False, strip_prompt=False)
        output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
    elif "Pre-configure" in output:  # Pre-conf
        output += net_connect.send_command_timing("n", strip_command=False, strip_prompt=False)
    elif "Delete filename" in output:  # Delete file
        for i in range(4):  # Answer to questions
            output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
    elif "Destination filename" in output:  # copy firmware tftp
        for i in range(2):
            output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
    elif "System configuration has been modified. Save?" in output:  # reload asa 
        output += net_connect.send_command_timing("n", strip_command=False, strip_prompt=False)
        output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
    elif "Erasing the nvram filesystem will remove all configuration files!" in output:  # Erase Router
        output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
    elif "Erase configuration in flash memory?" in output:  # Erase FW
        output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
    elif "Address or name of remote host" in output:  # copy firmware tftp
        for i in range(4):
            output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)


def connection(port):
    for i in [secret, "\n"]:
        active[int(port)] = False
        try:
            net_connect = netmiko.Netmiko(
                host=ip,
                username=username,
                password=password,
                secret=i,
                port=str(port),
                device_type="cisco_ios_telnet",
            )
        except netmiko.ssh_exception.NetmikoAuthenticationException or ConnectionResetError:
            status[int(port)] = "Bad Authentication"
            active[int(port)] = True
            return 0
        except EOFError:
            status[int(port)] = "Timeout"
            active[int(port)] = True
            return 0
        except ConnectionRefusedError:
            status[int(port)] = "Bad connect"
            active[int(port)] = True
            return 0
        status[int(port)] = "Good connect"
        try:
            net_connect.enable()
            status[int(port)] = "Good enable"
            break
        except:
            status[int(port)] = "Bad enable try \"\\n\""
            active[int(port)] = True
            continue
    if active[int(port)]:
        return 0
    else:
        return net_connect


def webobr(command):
    if request.form["device"] == "MANUAL":
        for i in list(request.form)[:-3]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)
    elif request.form["device"] == "HQ":
        for i in settings["HQ"]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)
    elif request.form["device"] == "BR":
        for i in settings["BR"]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)
    elif request.form["device"] == "ISP":
        for i in settings["ISP"]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)
    elif request.form["device"] == "SW3":
        for i in settings["SW3"]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)
    elif request.form["device"] == "SW2":
        for i in settings["SW2"]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)
    elif request.form["device"] == "SW1":
        for i in settings["SW1"]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)
    elif request.form["device"] == "FW1":
        for i in settings["FW1"]:
            if active[int(i)]:
                while True:
                    if len([i for i in list(active.values()) if i is False]) < 10:
                        eval(command)
                        break
                    status[int(i)] = "WAIT"
                    time.sleep(2)


class Configuration(Thread):
    def __init__(self, port, conf):
        Thread.__init__(self)
        self.port = port
        self.conf = conf

    def run(self):
        status[int(self.port)] = "Start config upload"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        net_connect.send_config_from_file(self.conf)
        status[int(self.port)] = "Config upload"
        net_connect.disconnect()
        active[int(self.port)] = True
        status[int(self.port)] = "Config upload - disconnect"


class Reset(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        status[int(self.port)] = "Start Reset"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        dialog(net_connect, "wr er")
        dialog(net_connect, "reload")
        status[int(self.port)] = "Reload"

        while True:
            try:
                output = net_connect.find_prompt()
            except:
                output = ""
            print(self.port, output)
            if "rommon" in output:
                status[int(self.port)] = "Rommon"
                dialog(net_connect, "boot")
            elif "IP address" in output:
                status[int(self.port)] = "Firewall mode"
                for i in range(5):
                    net_connect.send_command_timing('\x1A', strip_command=False, strip_prompt=False)
                break
            if "yes/no" in net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False):
                status[int(self.port)] = "Decline autoconfiguration"
                dialog(net_connect, "no", "Would")
                break
            time.sleep(10)
        status[int(self.port)] = "Reload finish"

        net_connect.disconnect()
        active[int(self.port)] = True
        status[int(self.port)] = "Reload finish - Disconnect"


class Firmware(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        status[int(self.port)] = "Start Firmware"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        status[int(self.port)] = " | ".join(re.findall(".+\.bin", net_connect.send_command('dir')))
        net_connect.disconnect()
        active[int(self.port)] = True


class Register(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        status[int(self.port)] = "Start Check Register"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        status[int(self.port)] = net_connect.send_command('show version | include register')
        net_connect.disconnect()
        active[int(self.port)] = True


class Ports(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        status[int(self.port)] = "Start Check Ports"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        status[int(self.port)] = net_connect.send_command('show cdp nei | b /').replace("\n", " | ")
        net_connect.disconnect()
        active[int(self.port)] = True


class Clear(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        status[int(self.port)] = "Start Clear"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        status[int(self.port)] = "Start clear flash"
        for i in net_connect.send_command('dir flash:').split("\n"):
            b = re.findall("  ([A-z0-9-\.]+$)", i)
            if b != [] and ".bin" not in b[0]:
                dialog(net_connect, "delete /recursive " + b[0])
        status[int(self.port)] = "Good clear flash"
        net_connect.disconnect()
        status[int(self.port)] = "Clear flash - disconnect"
        active[int(self.port)] = True


class Flashing(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        status[int(self.port)] = "Start Flashing"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        status[int(self.port)] = "Save name \.bin"
        bins = []
        for i in net_connect.send_command('dir flash:').split("\n"):
            b = re.findall("  ([A-z0-9-\.]+$)", i)
            if b != [] and ".bin" in b[0]:
                bins.append(re.findall("(^[A-z0-9]+)-", b[0])[0])
            if b != []:
                dialog(net_connect, "delete /recursive " + b[0])
        status[int(self.port)] = "Start flashing"
        for j in bins:
            dialog(net_connect, "copy " + tftp + [i for i in os.listdir(path) if j in i][0] + " flash:")
            time.sleep(10)
            while True:
                if "#" in net_connect.find_prompt():
                    break
        status[int(self.port)] = "Upload finish"
        net_connect.disconnect()
        status[int(self.port)] = "Upload finish - disconnect"
        active[int(self.port)] = True


class Check(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        status[int(self.port)] = "Start topology"
        net_connect = connection(self.port)
        if net_connect == 0:
            return
        status[int(self.port)] = "Check topology"
        allint = re.findall(".+?\d+\/\d+", net_connect.send_command('show cdp nei'))
        sortir = sorted([allint[i] for i in range(0, len(allint), 2)])
        st = ""
        if sortir == good:
            st = "Topology OK"
        else:
            st = " | ".join(sortir)
        status[int(self.port)] = st
        net_connect.disconnect()
        active[int(self.port)] = True


@app.route("/", methods=['POST', 'GET'])
def start():
    return render_template('main.html', ports=ranges)


@app.route("/obr", methods=['POST', 'GET'])
def obr():
    if request.method == 'POST':
        if request.form["mode"] == "Setings":
            if request.form["device"] == "HQ":
                for i in list(request.form)[:-3]:
                    if i not in str(settings):
                        settings["HQ"].append(i)
            elif request.form["device"] == "BR":
                for i in list(request.form)[:-3]:
                    if i not in str(settings):
                        settings["BR"].append(i)
            elif request.form["device"] == "ISP":
                for i in list(request.form)[:-3]:
                    if i not in str(settings):
                        settings["ISP"].append(i)
            elif request.form["device"] == "SW3":
                for i in list(request.form)[:-3]:
                    if i not in str(settings):
                        settings["SW3"].append(i)
            elif request.form["device"] == "SW2":
                for i in list(request.form)[:-3]:
                    if i not in str(settings):
                        settings["SW2"].append(i)
            elif request.form["device"] == "SW1":
                for i in list(request.form)[:-3]:
                    if i not in str(settings):
                        settings["SW1"].append(i)
            elif request.form["device"] == "FW1":
                for i in list(request.form)[:-3]:
                    if i not in str(settings):
                        settings["FW1"].append(i)
            elif request.form["device"] == "RESET":
                for i in settings.keys():
                    [settings[i].pop(j) for j, k in enumerate(settings[i]) if k in list(request.form)[:-3]]
        elif request.form["mode"] == "Reset":
            webobr("Reset(int(i)).start()")
        elif request.form["mode"] == "Config":
            if request.form["device"] == "MANUAL":
                for i in list(request.form)[:-3]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), os.getcwd() + "\\conf\\" + request.form["MANUAL"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
            elif request.form["device"] == "HQ":
                for i in settings["HQ"]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), os.getcwd() + "\\conf\\" + request.form["HQ"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
            elif request.form["device"] == "BR":
                for i in settings["BR"]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), pathconf + request.form["BR"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
            elif request.form["device"] == "ISP":
                for i in settings["ISP"]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), pathconf + request.form["ISP"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
            elif request.form["device"] == "SW3":
                for i in settings["SW3"]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), pathconf + request.form["SW3"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
            elif request.form["device"] == "SW2":
                for i in settings["SW2"]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), pathconf + request.form["SW2"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
            elif request.form["device"] == "SW1":
                for i in settings["SW1"]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), pathconf + request.form["SW1"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
            elif request.form["device"] == "FW1":
                for i in settings["FW1"]:
                    if active[int(i)]:
                        while True:
                            if len([i for i in list(active.values()) if i is False]) < 9:
                                Configuration(int(i), pathconf + request.form["FW1"]).start()
                                break
                            status[int(i)] = "WAIT"
                            time.sleep(2)
        elif request.form["mode"] == "Firmware":
            webobr("Firmware(int(i)).start()")
        elif request.form["mode"] == "Register":
            webobr("Register(int(i)).start()")
        elif request.form["mode"] == "Ports":
            webobr("Ports(int(i)).start()")
        elif request.form["mode"] == "Clear":
            webobr("Clear(int(i)).start()")
        elif request.form["mode"] == "Flashing":
            webobr("Flashing(int(i)).start()")
        elif request.form["mode"] == "Check":
            webobr("Check(int(i)).start()")
        else:
            print(str(list(request.form)))
    return redirect(url_for("start"))


@app.route("/logs", methods=['POST', 'GET'])
def logs():
    if request.method == 'GET':
        return render_template('logs.html',
                               settings=settings,
                               status=status,
                               active=active,
                               device=sorted(list(set(ranges) - set(map(int, sum(list(settings.values()), [])))))
                               )


if __name__ == "__main__":
    app.run(debug=True)
