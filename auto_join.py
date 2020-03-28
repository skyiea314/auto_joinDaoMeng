from jiami import *
from test import Post, test_token
import os
import datetime

user = input('请输入账号')
passwd = input('请输入密码')
aids=[]
time_aid={}

class Main:
 

    def read(self):
        with open('a.ini', 'r', encoding='utf-8') as f:
            self.token = f.readline().rstrip()
            self.name = f.readline().rstrip()
            self.uid = f.readline().rstrip()
    
    # 登录
    def login(self):
        
        acc = user
        pwd = passwd
    
        if os.path.exists('a.ini'):
            if test_token():
                return True
            else:
                print('登录失效，请重新登录')
                os.remove('a.ini')
                return False
        else:
            if get_token(acc, pwd):
                return True
            else:
                print('请检查账号密码')
                return False
    # 获取规划中的列表
    def get_aid(self):
        a = Post()
        a.get_ids(self.token, self.uid)
        print('欢迎您'+self.name)
        # 将规划中的活动加入
        for name, id, status in zip(a.names, a.ids, a.status):

            if(status == "2"):
                print(id)
                aids.append(id)

    def chiken(self):
        for aid in aids:
            a = Post()
            res = a.get_info(aid, self.token, self.uid)
            
            if res:
                # 将时间:aid加入字典中
                print(res['data']['joindate'])
                time_aid[res['data']['joindate']] = aid

            else:
                print('查询失败')

    def enter(self, id):
        a = Post()
        res = a.join(id, self.token, self.uid)
        if res:
            if res['code'] == '100':
                print('报名成功')
            else:
                print(res['msg'])
        else:
            print('查询失败，请检查id')


main = Main()
# 首先初始化登录
if main.login():
    # 每一小时更新一次map
    main.read()
    main.get_aid()
    main.chiken()

    # 按时间顺序报名,时间相同则会发生冲突
    for set_time in sorted(time_aid.keys()):

        # 将时间字符串裁剪只取前半部分,并格式化时间
        join_time = set_time.split('-')[0]
        join_time = datetime.datetime.strptime(join_time, '%Y.%m.%d %H:%M')
        print('即将报名的活动时间:')
        print(join_time)
        print('正在等待报名时间.....')
        while True:
            now = datetime.datetime.now()
            # 对比时间，时间到的话就报名
            if now >= join_time:
                if main.login():
                    main.enter(time_aid[set_time])
                    print('当前报名时间:')
                    print(now)
                    # 将已报名信息从字典与列表中删除
                    aids.remove(time_aid[set_time])
                    time_aid.pop(set_time)
                    # 中断内层循环
                break
