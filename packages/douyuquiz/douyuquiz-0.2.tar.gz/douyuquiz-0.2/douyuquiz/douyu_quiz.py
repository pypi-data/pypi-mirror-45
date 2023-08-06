import urllib.request
from urllib.parse import unquote
import ssl
import re
import json
import time
import hashlib
import socket
import threading
import logging
import sqlite3


def room_is_offline_func(url, headers):
    global room_is_offline
    request=urllib.request.Request(url=url, headers=headers)
    while True:
        try:
            room_is_offline_response=urllib.request.urlopen(request).read()
        except:
            print('获取房间内容失败，60秒后重试')
            time.sleep(60)
            continue
        room_is_offline_json=json.loads(room_is_offline_response)
        room_is_offline=room_is_offline_json['room']['show_status']
        time.sleep(60)

def convert_byte(content):
    length_1=bytearray([len(content) + 9, 0x00, 0x00, 0x00])
    length_2=length_1
    content_type=bytearray([0xb1, 0x02, 0x00, 0x00])
    content=bytes(content.encode("utf-8"))
    end=bytearray([0x00])
    return bytes(length_1+length_2+content_type+content+end)

def send_msg(content, s):
    msg=convert_byte(content)
    s.send(msg)
    response=bytearray()
    number=0
    while number<=5:
        buffer=s.recv(1024)
        if buffer==[]:
            break
        else:
            response.extend(buffer)
            number=number+1
    return response

def receive_danmu_quiz(room_id, danmu_s):
    time_last_keeplive=time.time()
    while True:
        if room_is_offline==2:
            break
        if time.time()-time_last_keeplive >= 45:
            content_auth_keeplive='type@=mrkl/'
            msg_auth_keeplive=convert_byte(content_auth_keeplive)
            danmu_s.send(msg_auth_keeplive)
            time_last_keeplive=time.time()
        danmu_response=danmu_s.recv(20480)
        danmu_response=danmu_response.split(b'/\\x00')
        for massage in danmu_response:
            if re.match(b'^.+type@=(erquizisn|rquizisn)/.+/qst@=2', massage)!= None:
                massage=massage.decode('utf8',errors='ignore')
                msg_to_sql(massage,room_id)

def msg_to_sql(msg,room_id):
    conn=sqlite3.connect('quizdata.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Quiz (
    time text, room_id test, quiz_id text, title text,
    left_title text, left_total integer, left_odd real,
    right_title text, right_total integer, right_odd real,
    result text
    )''')
    conn.commit()
    msg=msg.replace('\n', '')
    msg=msg.split('@AS@S')
    for quiz in msg:
        if quiz == '':
            continue
        quiz_title=re.findall(r'@ASqt@AA=(.+?)@', quiz)
        if quiz_title == []:
            continue
        quiz_title=quiz_title[0]
        quiz_qid=re.findall(r'qid@AA=(.+?)@', quiz)[0]
        quiz_left_title=re.findall(r'@ASfon@AA=(.+?)@', quiz)[0]
        quiz_right_title=re.findall(r'@ASson@AA=(.+?)@', quiz)[0]
        quiz_left_total=int(re.findall(r'@AS(?:fobc|op1to)@AA=(.+?)@', quiz)[0])
        quiz_right_total=int(re.findall(r'@AS(?:sobc|op2to)@AA=(.+?)@', quiz)[0])
        quiz_left_odd=float(re.findall(r'AS(?:folpc|op1pr)@AA=(.+?)@', quiz)[0])*0.01
        quiz_right_odd=float(re.findall(r'@AS(?:solpc|op2pr)@AA=(.+?)@', quiz)[0])*0.01
        quiz_result=re.findall(r'@ASwo@AA=(.+?)@', quiz)[0]
        date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        row=(date, room_id, quiz_qid, quiz_title, quiz_left_title, quiz_left_total, quiz_left_odd, quiz_right_title, quiz_right_total, quiz_right_odd, quiz_result,)
        c.execute('''INSERT INTO Quiz(time, room_id, quiz_id, title, left_title, left_total, left_odd, right_title, right_total, right_odd, result) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',row)
        conn.commit()
        logging.info('获取一条竞猜结果，写入quizdata.db')
        print('获取一条竞猜结果，写入quizdata.db')
    conn.close()

# main function
def douyuquiz(room_id):
    room_id=str(room_id)
    ssl._create_default_https_context = ssl._create_unverified_context
    url='https://www.douyu.com/betard/{}'.format(room_id)
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    logging.basicConfig(level=logging.INFO, filename='douyuquiz.log', filemode='a', format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    is_offline=threading.Thread(target=room_is_offline_func, args=(url, headers))
    is_offline.start()
    time.sleep(5)
    # 主循环
    while True:
        print('正在连接直播间服务器')
        while True:
            if room_is_offline==1:
                request=urllib.request.Request(url=url, headers=headers)
                response=urllib.request.urlopen(request).read()
                room_info_json=json.loads(response)
                room_name=room_info_json['room']['room_name']
                logging.info('主播已经开播，房间号:{}, 房间名:{}'.format(room_id, room_name))
                print('主播已经开播，房间号:{}, 房间名:{}'.format(room_id, room_name))
                break
            elif room_is_offline==2:
                print('主播未开播，10分钟后刷新')
                time.sleep(600)
                continue
            else:
                print('网络错误或room_id输入有误，请重试')
                break
        room_auth_list=json.loads(unquote(room_info_json['room_args']['server_config']))
        rt=str(int(time.time()))
        vk_string=rt+"7oE9nPEG9xXV69phU31FYCLUagKeYtsF"+'c31d74819620530ffb3c624f70705111'
        hl=hashlib.md5()
        hl.update(vk_string.encode(encoding='utf-8'))
        vk=hl.hexdigest()
        content_auth='type@=loginreq/username@=/ct@=0/password@=/roomid@={}/devid@=c31d74819620530ffb3c624f70705111/rt@={}/vk@={}/ver@=20180809/'.format(room_id, rt, vk)
        msg_auth=convert_byte(content_auth)
        for address_port in room_auth_list:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((address_port['ip'], int(address_port['port'])))
                logging.info('认证服务器失败，换下一组服务器')
            except:
                continue
            s.send(msg_auth)
            response_auth=bytearray()
            number=0
            while number<=5:
                buffer=s.recv(1024)
                if buffer==[]:
                    break
                else:
                    response_auth.extend(buffer)
                    number=number+1
            if response_auth!=[]:
                break
            else:
                s.close()
                logging.info('认证服务器失败，换下一组服务器')
                print('认证服务器失败，换下一组服务器')
        response_auth=str(response_auth)
        username=re.findall(r'^.*username@=(\w+)/', response_auth)
        danmu_server=[('danmu.douyu.com', '8601'), ('danmu.douyu.com', '8602'), ('danmu.douyu.com', '12601'), ('danmu.douyu.com', '12602'), ('danmu.douyu.com', '12603'), ('danmu.douyu.com', '12604')]
        if username and danmu_server:
            logging.info('成功获取用户名，弹幕服务器')
            print('成功获取用户名，弹幕服务器')
        content_auth_2="type@=qrl/rid@={}/".format(room_id)
        response_auth_2=send_msg(content_auth_2,s)
        if response_auth_2:
            logging.info('第二步认证成功')
            print('第二步认证成功')
        content_auth_3="type@=keeplive/tick@={}/vbw@=0/k@=19beba41da8ac2b4c7895a66cab81e23/".format(str(int(time.time())))
        response_auth_3=send_msg(content_auth_3,s)
        if response_auth_3:
            logging.info('keeplive认证成功')
            print('keeplive认证成功')
        content_danmu_auth_1="type@=loginreq/username@={}/password@=1234567890123456/roomid@={}/".format(username[0],room_id)
        msg_danmu_auth_1=convert_byte(content_danmu_auth_1)
        for danmu_ip_port in danmu_server:
            logging.info('正在连接弹幕服务器{}:{}'.format(danmu_ip_port[0], danmu_ip_port[1]))
            print('正在连接弹幕服务器{}:{}'.format(danmu_ip_port[0], danmu_ip_port[1]))
            danmu_s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                danmu_s.connect((danmu_ip_port[0],int(danmu_ip_port[1])))
                logging.info('弹幕服务器认证失败，换下一组服务器')
            except:
                continue
            danmu_s.send(msg_danmu_auth_1)
            response_danmu_auth=danmu_s.recv(1024)
            if response_danmu_auth!=[]:
                logging.info('弹幕服务器认证成功')
                print('弹幕服务器认证成功')
                break
            else:
                danmu_s.close()
                print('danmu_s关闭')
                logging.info('认证弹幕服务器失败，换下一组服务器')
                print('认证弹幕服务器失败，换下一组服务器')
        content_danmu_join="type@=joingroup/rid@={}/gid@=-9999/".format(room_id)
        msg_danmu_join=convert_byte(content_danmu_join)
        logging.info('发送弹幕服务器join请求')
        print('发送弹幕服务器join请求')
        danmu_s.send(msg_danmu_join)
        response_danmu_join=danmu_s.recv(1024)
        if response_danmu_join:
            logging.info('发送弹幕服务器join请求成功')
            print('发送弹幕服务器join请求成功')
        logging.info('获取竞猜消息')
        print('获取竞猜消息')
        while True:
            receive_danmu_quiz(room_id, danmu_s)
            logging.info('主播已下播')
            print('主播已下播')
            time.sleep(5)
            break
        s.close()
        danmu_s.close()
