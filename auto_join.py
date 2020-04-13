from jiami import get_token
from test import Post, test_token
import os
import datetime
import threading
import time


user = input('请输入账号')
passwd = input('请输入密码')
aids = {}
time_aid = {}


class Opreation:

    def read(self):
        with open('a.ini', 'r', encoding='utf-8') as f:
            self.token = f.readline().rstrip()
            self.name = f.readline().rstrip()
            self.uid = f.readline().rstrip()

    # 登录
    def login(self):

        acc = user
        pwd = passwd
        # 修复bug防止因为token过期
        if os.path.exists('a.ini'):
            if test_token():
                print('token登录成功')
                return True
            elif get_token(acc, pwd):
                print('密码登录成功')
                return True
            else:
                print('token过期请检查账号密码')
                os.remove('a.ini')
                return False
        else:
            if get_token(acc, pwd):
                print('密码登录成功')
                return True
            else:
                print('请检查账号密码')
                return False

    # 获取规划中的列表
    def get_aid(self):
        a = Post()
        a.get_ids(self.token, self.uid)
        # 将规划中的活动加入
        for name, id, status in zip(a.names, a.ids, a.status):
            # 防止重复添加
            if(status == "2")and(id not in aids):
                # print(name+':'+id+status)
                aids[id] = name

    def chiken(self):
        for aid in aids.keys():
            a = Post()
            res = a.get_info(aid, self.token, self.uid)

            if res:
                # 判断是否有存在的键值对,以免重复添加
                # 将时间:aid加入字典中
                # print(aids[aid]+"报名时间:"+res['data']['joindate'])
                time_aid[res['data']['joindate']] = aid

            else:
                print('查询失败')

    def enter(self, id):
        a = Post()
        res = a.join(id, self.token, self.uid)
        if res:
            if res['code'] == '100':
                print(aids[id]+'报名成功')
                return True
            else:
                print('报名失败')
                return False
        else:
            print('查询失败，请检查id')
            return False


opreation = Opreation()


# 增加定时功能
def update():
    if opreation.login():
        opreation.read()
        opreation.get_aid()
        opreation.chiken()
        print("更新成功")
        timer = threading.Timer(3600, update)
        timer.start()


def join():
    # 按时间顺序报名,时间相同则会发生冲突
    for set_time in sorted(time_aid.keys()):

        # 将时间字符串裁剪只取前半部分,并格式化时间
        join_time = set_time.split('-')[0]
        join_time = datetime.datetime.strptime(join_time, '%Y.%m.%d %H:%M')
        print('即将报名的活动:'+aids[time_aid[set_time]])
        print(join_time)
        print('正在等待报名时间.....')
        while True:
            now = datetime.datetime.now()

            # 对比时间，时间到的话就报名
            if now >= join_time:
                # 重复四次报名
                for i in range(4):
                    opreation.login()
                    if opreation.enter(time_aid[set_time]):
                        break
                    time.sleep(0.01)
                # 将已报名信息从字典中删除
                aids.pop(time_aid[set_time])
                time_aid.pop(set_time)
                # 中断内层循环
                break
            time.sleep(0.1)


def main():

    # 首先初始化登录
    if opreation.login():
        # 初始化报名
        opreation.read()
        print('正在初始化')
        print('欢迎您'+opreation.name)

        opreation.get_aid()
        opreation.chiken()
        timer = threading.Timer(3600, update)
        timer.start()
        join()


if __name__ == '__main__':
    main()
