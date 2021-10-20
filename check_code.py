#!/usr/bin/env python
# coding=utf-8
#
# commit msg check
import sys
from os import walk
from os.path import join

import smtplib
from email.mime.text import MIMEText

# if hasattr(sys.stdout, 'buffer'):
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TIPS_INFO = '''
！！！！提交失败！！！！
注释不符合规范，提交失败（当前状态等于没做刚刚的同步操作）！
请确保注释已填写完善！
！！！！提交失败！！！！
'''

def send_email(msg):
    mail_host = 'smtp.qq.com'  
    #用户名
    mail_user = '@qq.com'  
    #密码(部分邮箱为授权码) 
    mail_pass = ''   
    #邮件发送方邮箱地址
    sender = '@qq.com'  
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['@qq.com']  

    #设置email信息
    #邮件内容设置
    message = MIMEText(msg,'plain','utf-8')
    #邮件主题       
    message['Subject'] = '更新的代码存在不合法注释！' 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误

def walk_excels(input_path):
    if(not isinstance(input_path, list)):
        input_path = [input_path]
    java_path = []
    for path in input_path:
        name = path.split('\\')[-1]
        if(name[-4:] in ['java'] and name[:2] != '~$'):
            java_path.append(path)
            continue
        for root, dirs, files in walk(path, topdown=False):
            for name in files:
                if(name[-4:] in ['java'] and name[:2] != '~$'):
                    java_path.append(join(root, name))
    return java_path

def contain_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

class check_commit_line():
    def __init__(self):
        self.note_keyword = None
        self.target_keyword = None
        self.note_flag = False

    def init_mode(self, mode):
        if(mode == 0):
            self.note_keyword = '@ApiModelProperty'
            self.target_keyword = 'private'
        elif(mode == 1):
            self.note_keyword = '@ApiOperation'
            self.target_keyword = 'ResponseEntity'
        elif(mode == 2):
            self.note_keyword = '@ApiModelProperty'
            self.target_keyword = 'private'
        print('注释关键词：{}'.format(self.note_keyword))
        print('定义关键词：{}'.format(self.target_keyword))
    def check_line(self, msg):
        tmp = msg.replace(' ', '')
        if(tmp[:2] == '//' or tmp[0] == '*'):
            return 1
        elif(tmp.find(self.note_keyword) == 0 and contain_chinese(tmp)):
            self.note_flag = True
            print(tmp)
            return 1
        if(tmp.find(self.target_keyword) == 0):
            if(self.note_flag):
                self.note_flag = False
                return 1
            else:
                return 0


if __name__=="__main__":
    print('python start!')
    target_path = sys.argv[1]
    files_path = walk_excels(target_path)
    print('path:{}'.format(files_path))
    start_flag = 0
    first_line_flag = 1
    mode = None
    checker = check_commit_line()
    for file_path in files_path:
        line_num = 0
        with open(file_path, 'r') as f:
            for line in f:
                line_num += 1
                line = line.replace(' ', '')
                if(start_flag == 0 and line[:7] == 'package'):
                    start_flag = 1
                if(start_flag == 0):
                    continue
                if(first_line_flag):
                    first_line_flag = 0
                    if('controller.dto' in line):
                        mode = 0
                    elif('controller.v1' in line):
                        mode = 1
                    elif('entity' in line):
                        mode = 2
                    checker.init_mode(mode)
                    continue

                if(checker.check_line(line) == 0):
                    msg = '所更新的java代码中存在不合法的注释情况！\n文件名：{}\n行数：{}'.format(file_path.split('/')[-1], line_num)
                    print(file_path, line, TIPS_INFO)
                    send_email(msg)
                    sys.exit(1)
    print('finished with no error!')
    sys.exit(0)
