import datetime
import os
import random
import re
import shutil
import time
import win32gui
import imagehash
import pytesseract
import win32com.client
import win32con

from PIL import Image, ImageGrab, ImageDraw
from aip import AipOcr
# import speech
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from pymouse import PyMouse

# auther:大豆
# version:1.0
# date:2018.09.01


speaker = win32com.client.Dispatch('SAPI.SpVoice')
mouse = PyMouse()
base_dir = r'./'
imgs_dir = r'./images/'
conf_dir = r'./conf/'
log_dir = r'./logs/'

# 设置执行锁
execute_lock = 'common'
# pattern = re.compile(r'\d+|Q')
city_pattern = re.compile('[比奇]')
queue_jobs_list = []
amount_fight = 0
amount_rush = 0
amount_tower = 0
amount_secret_boss = 0
amount_fight_failed = 0
action_name = ''
action_name2 = ''
action_lock = [False, action_name, datetime.datetime.strptime('2018-10-01 08:00:00', '%Y-%m-%d %H:%M:%S')]
action_lock2 = [False, action_name, datetime.datetime.strptime('2018-10-01 08:00:00', '%Y-%m-%d %H:%M:%S')]
normal_log = 'message.log'
boss_log = 'boss.log'
prisoner_log = 'prisoner.log'


def find_window(target_title='CefWebViewWnd'):
    """
    查找传奇来了客户端
    :param target_title: '传奇来了'窗体名称
    :return: 返回窗体handle
    """
    handle = win32gui.FindWindow(target_title, None)
    return handle


def reset_window():
    """
    重新设置客户端大小
    x,y,宽，高
    :return:
    """
    handle = find_window()
    win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 1312, 0, 608, 1080, win32con.SWP_SHOWWINDOW)


def get_force(handle):
    """
    获取窗口焦点
    :param handle: 参数接收一个窗体handle
    :return: 返回元组，窗口左上角和右下角的坐标 lx,ly,rx,ry
    """
    lx, ly, rx, ry = win32gui.GetWindowRect(handle)
    # print('Lx：%s\nLy：%s\nRx：%s\nRy：%s' % (lx, ly, rx, ry))
    # 指定句柄设置为前台，也就是激活
    win32gui.SetForegroundWindow(handle)
    return lx, ly, rx, ry


def cost_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        print('\n%s' % start.strftime('%Y-%m-%d %H:%M:%S'))
        res = func(*args, **kwargs)
        end = datetime.datetime.now()
        result = end - start
        if result.total_seconds() > 60:
            expentiture_time = result.total_seconds() / 60
            ext = '分'
        else:
            expentiture_time = result.total_seconds()
            ext = '秒'
        print('%s %s:花费时间:%.3f%s\n' % (end, func.__name__, expentiture_time, ext))
        return res

    return wrapper


def set_lock(func):
    """
    装饰器，锁定每个动作，防止并发执行
    :param func: 接收动作函数
    :return: 返回加锁后的动作
    """

    def wrapper(*args, **kwargs):
        global action_name, action_lock
        now = datetime.datetime.now()
        time_consuming = (now - action_lock[2]).seconds
        if time_consuming < 300:
            for n in range(4):
                if action_lock[0]:
                    print('正在执行:%s，5秒后再次尝试%d:%s' % (action_lock[1], n + 1, func.__name__))
                    if n == 3:
                        print('%s正在执行，放弃执行:%s' % (action_lock[1], func.__name__))
                        return False
                    time.sleep(5)
                else:
                    break

        action_lock[0] = True
        action_lock[1] = func.__name__
        action_lock[2] = now
        try:
            inner = func(*args, **kwargs)
        except:
            pass
        action_lock[0] = False
        wrapper.__name__ = func.__name__
        return inner

    return wrapper


def set_single(func):
    """
    装饰器，锁定每个动作，防止并发执行
    :param func: 接收动作函数
    :return: 返回加锁后的动作
    """

    def wrapper(*args, **kwargs):
        global action_name2, action_lock2
        now = datetime.datetime.now()
        time_consuming = (now - action_lock2[2]).seconds
        if time_consuming < 300:
            for n in range(3):
                if action_lock2[0]:
                    print('正在执行:%s，1秒后再次尝试%d:%s' % (action_lock2[1], n + 1, func.__name__))
                    if n == 2:
                        print('%s正在执行，放弃执行:%s' % (action_lock2[1], func.__name__))
                        return None
                    time.sleep(1)
                else:
                    break

        action_lock2[0] = True
        action_lock2[1] = func.__name__
        action_lock2[2] = now
        inner = func(*args, **kwargs)
        action_lock2[0] = False
        wrapper.__name__ = func.__name__
        return inner

    return wrapper


def baidu_ocr():
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client


def copy_image(filename, new_dir='rob_name'):
    """
    复制图片
    :param filename:str 文件名
    :param new_dir: str 目标文件目录
    :return:
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    new_filename = now + '_' + filename
    if os.path.exists(imgs_dir + filename):
        if not os.path.exists(imgs_dir + new_filename):
            shutil.copyfile(imgs_dir + filename, imgs_dir + new_dir + '/' + new_filename)


def get_file(filename, directory=imgs_dir):
    """
    根据给定图片文件名，打开文件对象
    :param filename: 文件名，字符串
    :param directory: 目录名，默认为./images/
    :return: 返回图片二进制内容
    """
    with open(directory + filename, 'rb') as fp:
        return fp.read()


def get_content(filename, accurate=False):
    """
    根据给定图片文件名，获取文件图片中的文字内容
    :param filename:图片文件名,字符串
    :param accurate:是否精确识别，精确时间花费时间较长，默认普通识别，bool
    :return:返回文字内容
    """
    time.sleep(1)
    image = get_file(filename)
    client = baidu_ocr()
    if accurate:
        # result = client.basicAccurate(image)
        result = client.basicGeneral(image)
    else:

        result = client.basicGeneral(image)

    if 'error_msg' in result:
        print(result)
        result = client.basicGeneral(image)
    if result['words_result_num'] == 1:
        words = result['words_result'][0]['words']
        print(words)
        return words
    return None


def get_content_local(filename, lang='chi_sim', psm=7):
    """
    获取图片中的文字内容
    :param filename: str 图片文件
    :param lang: str 识别的文字库
    :param psm: int default:7 识别模式6为多行模式，7为单行模式
    :return:
    """
    fp = open(imgs_dir + filename, 'rb')
    text = pytesseract.image_to_string(Image.open(fp), lang=lang, config='--psm ' + str(psm))
    fp.close()
    return text


def record_log(filename, content):
    """
    记录日志
    :param filename: str 日志文件名
    :param content: str 日志内容
    :return:
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_dir + filename, 'a+', encoding='utf-8') as f:
        f.write('%-25s%s\n' % (now, content))


def file_operation(filename, operation='read', content=""):
    """
    操作配置文件，进行读写操作
    :param filename: str 需要操作的文件名
    :param operation: str ['read','write'] 读文件rdad 写文件write
    :param content: str 写文件是对应写入的内容
    :return:
    """
    if operation == 'read':
        with open(conf_dir + filename, 'r', encoding='utf-8') as f:
            words = f.readline()
            return words
    if operation == 'write':
        with open(conf_dir + filename, 'w+', encoding='utf-8') as f:
            f.write(content)


def snapshot(position, filename):
    """
    据给定坐标，截取截图，并返回截图中心点坐标
    :param position: 截取图片左上右下角的坐标,元组(lx,ly,rx,ry)
    :param filename: filename: 截图文件名
    :return: 返回截图中心点坐标，元组(x,y)
    """
    ImageGrab.grab(position).save(imgs_dir + filename)
    # 根据给定坐标设置位置中心点坐标
    lx, ly, rx, ry = position
    width = rx - lx
    height = ry - ly
    x = int(lx + width / 2)
    y = int(ly + height / 2)
    mouse_position = x, y
    return mouse_position


# def save_rgb_pic(filename, rgb_index=0, threshold=80, less=True):
#     """
#     将传入的图片颜色过滤后处理为黑白文字图
#     :param filename: str 文件名
#     :param rgb_index: int [0-2] default:0 RGB的索引
#     :param threshold: int [0-255] default:17 RGB某个颜色的阈值
#     :return:返回新的文件名，原文件名前加rgb_
#     """
#     new_filename = 'rgb_' + filename
#     # 定义二值数组
#     t2val = {}
#     fp = open(imgs_dir + filename, 'rb')
#     image = Image.open(fp)
#
#     # 遍历图像中的每个像素
#     for y in range(0, image.size[1]):
#         for x in range(0, image.size[0]):
#             # 获取每个像素的RGB值
#             pixel_rgb = image.getpixel((x, y))
#             # 将像素rgb中的r 的值与临界值进行比较
#             if less:
#                 if pixel_rgb[rgb_index] < threshold:
#                     # 小于临界值设置为白色
#                     t2val[(x, y)] = (255, 255, 255)
#                 else:
#                     # 大于临界值设置为黑色
#                     t2val[(x, y)] = (0, 0, 0)
#             else:
#                 if pixel_rgb[rgb_index] > threshold:
#                     # 小于临界值设置为白色
#                     t2val[(x, y)] = (255, 255, 255)
#                 else:
#                     # 大于临界值设置为黑色
#                     t2val[(x, y)] = (0, 0, 0)
#
#     # 新建RGB对象
#     new_image = Image.new("RGB", image.size)
#     draw = ImageDraw.Draw(new_image)
#     # 重绘RGB新图像
#     for x in range(0, image.size[0]):
#         for y in range(0, image.size[1]):
#             draw.point((x, y), t2val[(x, y)])
#     new_image.save(imgs_dir + new_filename)
#     fp.close()
#     return new_filename


def rgb_filter(filename, r_threshold=0, g_threshold=0, b_threshold=0, r_compare='>', g_compare='>', b_compare='>',
               x_start=0, x_end=0, y_start=0, y_end=0):
    """
    将传入的图片文件，通过RGB颜色过滤后转换为黑白图，并保存为新图片
    :param filename:str 传入的文件名
    :param r_threshold:int R的阈值
    :param g_threshold:int G的阈值
    :param b_threshold:int B的阈值
    :param r_compare:str ['<','==','>'] R比较操作符
    :param g_compare:str ['<','==','>'] G比较操作符
    :param b_compare:str ['<','==','>'] B比较操作符
    :param x_start: int 开始x坐标
    :param x_end: int 结束x坐标
    :param y_start: int 开始y坐标
    :param y_end: int 结束y坐标
    :return:str 返回新文件，在源文件前加'rgb_'
    """
    new_filename = 'rgb_' + filename
    # 定义二值数组
    t2val = {}
    fp = open(imgs_dir + filename, 'r+b')
    image = Image.open(fp)

    # 遍历图像中的每个像素
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            # 获取每个像素的RGB值
            pixel_rgb = image.getpixel((x, y))
            # 坐标x_start开始,到坐标x_end结束 与 y_start < y < y_end填充白色遮盖
            if x_start <= x <= x_end and y_start <= y <= y_end:
                t2val[(x, y)] = (255, 255, 255)
                continue
            if eval(str(pixel_rgb[0]) + r_compare + str(r_threshold) + ' and ' + str(pixel_rgb[1]) + g_compare + str(
                    g_threshold) + ' and ' + str(pixel_rgb[2]) + b_compare + str(
                b_threshold)):
                # 符合条件设置为黑色
                t2val[(x, y)] = (0, 0, 0)
            else:
                # 不符合设置为白色
                t2val[(x, y)] = (255, 255, 255)

    # 新建RGB对象
    new_image = Image.new("RGB", image.size)
    draw = ImageDraw.Draw(new_image)
    # 重绘RGB新图像
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            draw.point((x, y), t2val[(x, y)])
    new_image.save(imgs_dir + new_filename)
    fp.close()
    return new_filename


def gray_binary(filename, threshold=120):
    fp = open(imgs_dir + filename, 'rb')
    img = Image.open(fp)

    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    Img = img.convert('L')
    gray_filename = imgs_dir + 'gray_' + filename
    Img.save(gray_filename)
    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = threshold
    table = []
    for i in range(256):
        if i > threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化
    photo = Img.point(table, '1')
    binary_filename = imgs_dir + 'binary_' + filename
    photo.save(binary_filename)
    fp.close()
    return binary_filename


def compare_content(position, filename, my_words, accurate=True, click=True, move=False):
    """
    根据给坐标立即截取图片，并提取图片中的文字信息
    :param position:截取图片左上和右下角坐标的元组(lx,ly,rx,ry)
    :param filename:图片文件名，字符串
    :param my_words:匹配字符串，字符串
    :param accurate: 是否精确比较，bool
    :param click:如果匹配是否需要点击，bool
    :param move: click为False时，此选项为True时则把鼠标移动到图片中心，用于调试，bool
    :return:成功返回True,否则返回False,bool
    """

    mouse_position = snapshot(position, filename)
    words = get_content(filename, accurate=accurate)
    print(words)
    if my_words == words:
        if click:
            mouse.click(*mouse_position)
        elif move:
            mouse.move(*mouse_position)
        return True
    return False


def compare_image(original_image, temp_image, directory=imgs_dir, arg=0.9):
    """
    比对原始图片和临时图片，判断是否一致
    :param original_image:原始图片
    :param temp_image:临时图片
    :param directory:文件目录默认为./images/
    :param arg:相似值参数，1为图片完全匹配，小于1为图片相似
    :return:返回元组(是否匹配，匹配度)
    """
    hash_size = 8
    fp1 = open(directory + original_image, 'rb')
    fp2 = open(directory + temp_image, 'rb')
    hash1 = imagehash.average_hash(Image.open(fp1), hash_size=hash_size)
    hash2 = imagehash.average_hash(Image.open(fp2), hash_size=hash_size)

    similarity = (1 - (hash1 - hash2) / len(hash1.hash) ** 2)
    # print(similarity)
    fp1.close()
    fp2.close()
    if similarity > arg:
        return True, similarity
    else:
        return False, similarity


def print_time():
    now_time = datetime.datetime.now()
    print('\n', now_time)


def rob_list(one=True, two=True, three=True):
    """
    循环监测镖车列表，符合条件进行抢夺
    :return:
    """
    # 当前时间点日期
    now = datetime.datetime.now()
    key_date = now.strftime('%Y-%m-%d')

    periods = []
    # 跨服押镖 第一场、第二场
    key_time1 = ['11:00:00', '13:00:00']
    key_time2 = ['18:00:00', '20:00:00']
    key_time3 = ['21:00:00', '23:00:00']

    periods.append(key_time1)
    periods.append(key_time2)
    periods.append(key_time3)
    # periods.append(key_time3)


    out = True
    second = 0
    delay_time = 0.3

    position_title = (1360, 192, 1458, 216)
    title_file = 'rob_union_title.bmp'
    snapshot(position_title, title_file)
    union_title_file = rgb_filter(title_file, g_threshold=80)
    title = get_content_local(union_title_file)
    if '本公会' not in title:
        print('不在抢夺列表界面')
        return False

    # [镖车等级,当前护送人数，可击破数]
    last_num = [[9, 99, 99], [9, 99, 99], [9, 99, 99], [9, 99, 99], [9, 99, 99], [9, 99, 99], [9, 99, 99], [9, 99, 99]]
    rank_patten = re.compile('.*: ?(\d)$')
    num_patten = re.compile('^\d{1,2}$')

    while out:
        for period in periods:
            key_start_str = key_date + ' ' + period[0]
            key_end_str = key_date + ' ' + period[1]
            key_start = datetime.datetime.strptime(key_start_str, '%Y-%m-%d %H:%M:%S')
            key_end = datetime.datetime.strptime(key_end_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()
            if key_start <= now <= key_end:
                in_periods = True
                break
            else:
                # 不在抢夺时间点内，设置标记
                in_periods = False
        if not in_periods:
            print('超出掠夺时间')
            out = False
            # 关闭抢夺列表
            mouse.click(1858, 156)
            time.sleep(1)
            # 关闭跨服押镖
            mouse.click(1858, 176)

        second += 1
        print("次数：%2d" % second)
        # if second == 3600:
        #     break
        lx, ly, rx, ry = 1449, 260, 1686, 315
        x = 1821
        y = 286

        for num in range(0, 8):
            position = lx, ly, rx, ry
            if last_num[num][2] != 0:
                filename = 'rob_p' + str(num + 1) + '.bmp'
                snapshot(position, filename)

                new_filename = rgb_filter(filename, r_threshold=80, g_threshold=80, b_threshold=150, b_compare='<',
                                          x_start=50,
                                          x_end=208, y_end=60)
                # 原始字符串
                words = get_content_local(new_filename, lang='legend_figure', psm=6)
                # print(words)
                row_split = re.split('\n', words, re.M)
                # print(row_split)
                mark = ''
                # 如果抢夺信息有两行
                if len(row_split) == 2:
                    # 获取镖车等级
                    # print(row_split[0])
                    rank_result = rank_patten.match(row_split[0].strip())
                    # print(rank_result)
                    if rank_result is not None:
                        # 第一行为数字，并且只有一位，则从row_split[0]获取镖车等级
                        rank = rank_result.groups()[0]
                        # print(rank)
                        carriage_rank = int(rank)
                        # 设置上次飙车等级
                        last_num[num][0] = carriage_rank
                    else:
                        # 第一行不为数字或有多位，则从上次镖车等级获取
                        carriage_rank = last_num[num][0]
                    # 获取护送人数、击破数
                    floor_info = row_split[1]
                # 如果抢夺信息有一行
                if len(row_split) == 1:
                    # 获取护送人数、击破数
                    floor_info = row_split[0]
                    # 镖车等级
                    carriage_rank = last_num[num][0]
                    mark = 'rank!'
                # print(floor_info)

                # 分割取护送人数、击破数字符串，['当前护送人数','护送总人数','可击破数'] e.g. ['8', '8', '1']
                floor_split = re.split('[ /]+', floor_info)
                floor_list = list(filter(None, floor_split))
                if len(floor_list) == 0:
                    continue
                # print(floor_list)

                if len(floor_list) == 3:
                    # 当前护送人数
                    if num_patten.match(floor_list[0]):
                        protect_amount = int(floor_list[0])
                    else:
                        protect_amount = last_num[num][1]
                        mark = 'protect!'
                    # 可击破数
                    if num_patten.match(floor_list[2]):
                        broken = int(floor_list[2])
                    else:
                        broken = last_num[num][2]
                        mark = 'broken!'
                else:
                    # 当前护送人数
                    protect_amount = last_num[num][1]
                    # 可击破数
                    broken = last_num[num][2]
                    mark = 'x'

                if protect_amount != last_num[num][1]:
                    mark = '-'
                # 设置上次护送人数、可击破数
                last_num[num][1] = protect_amount
                last_num[num][2] = broken
                print('镖车等级:%d 可击破数:%d 护送人数:%2d %s' % (carriage_rank, broken, protect_amount, mark))

                # 所有等级镖车护送人数为1,马上抢夺
                if protect_amount == 1:
                    out = False
                    mouse.click(x, y)
                    time.sleep(delay_time)
                    mouse.click(1602, 745)
                    print('发现可抢夺对象，护送人数：%d' % protect_amount)
                    break
                # 三级以上镖车，护送人数为2攻击
                if three and carriage_rank >= 3:
                    # 可击破等于4，护送人数小于等于3才攻击
                    if broken == 4 and 0 < protect_amount <= 6:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                    if broken == 3 and 0 < protect_amount <= 5:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                    if broken <= 2 and 0 < protect_amount <= 5:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                # 二级镖车
                if two and carriage_rank == 2:
                    # 可击破等于4，护送人数小于等于3才攻击
                    if broken == 4 and 0 < protect_amount <= 6:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                    # 可击破数等于2/3，则护送人数需小于等于2
                    if broken == 3 and 0 < protect_amount <= 6:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                    if broken == 2 and 0 < protect_amount <= 5:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                # 一级镖车
                if one and carriage_rank == 1:
                    # 可击破等于4，护送人数小于等于3才攻击
                    if broken == 4 and 0 < protect_amount <= 6:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                    # 可击破数等于3，则护送人数需小于等于3
                    if broken == 3 and 0 < protect_amount <= 6:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break
                    # 可击破数小于等于2，则护送人数需小于等于2
                    if broken <= 2 and 0 < protect_amount <= 6:
                        out = False
                        mouse.click(x, y)
                        time.sleep(delay_time)
                        mouse.click(1602, 745)
                        print('发现可抢夺对象，护送人数：%d' % protect_amount)
                        break

            ly += 78
            ry += 78
            y += 78

    content = '发现劫镖对象,镖车等级:%d,可击破数:%d,护送人数:%d' % (carriage_rank, broken, protect_amount)
    print(content)
    try:
        speaker.Speak(content)
    except:
        pass


def get_rob_token():
    """
    获取跨服镖车当前可用劫镖令数量
    :return: int
    """
    position = (1846, 434, 1878, 462)
    filename = 'token_num.bmp'
    snapshot(position, filename)
    token_file = rgb_filter(filename, r_threshold=0, g_threshold=100, b_threshold=0, r_compare='==', g_compare='>',
                            b_compare='==')
    time.sleep(1)
    words = get_content_local(token_file, lang='legend_figure')
    if words:
        if int(words) >= 0:
            print('劫镖领数量:%s' % words)
            return int(words)
    return None


def get_rob_cd():
    """
    检查抢夺冷却时间是否已过
    :return: bool 可抢夺返回True,否则返回False
    """
    position = (1768, 825, 1832, 848)
    filename = 'can_rob.bmp'
    snapshot(position, filename)
    can_rob_file = rgb_filter(filename, r_threshold=140)
    time.sleep(1)
    words = get_content_local(can_rob_file, lang='chi_sim')
    if words == '可抢夺':
        print('跨服镖车目前没有CD，进入抢夺列表')
        return True
    return False


def rob_list_icon():
    """
    跨服镖车中，检查是否在抢夺列表界面
    :return:
    """
    position = (1349, 496, 1431, 527)
    filename = 'rob_list_icon.bmp'
    x, y = snapshot(position, filename)
    rob_icon = rgb_filter(filename, r_threshold=150, g_threshold=240, b_threshold=170, g_compare='<', b_compare='<')
    words = get_content_local(rob_icon)
    print(words)
    if words and '列表' in words:
        return True
    return False


def rob_message_confirm():
    """
    公会镖车信息报告确认
    :return:
    """
    position = (1585, 654, 1640, 680)
    filename = 'rob_message_confirm.bmp'
    x, y = snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=170)
    words = get_content_local(rgb_file)
    print('识别文字:%s' % words)
    if '确认' in words:
        print('确认镖车抢夺信息')
        mouse.click(x, y)
        return True
    return False


def global_rob():
    """
    跨服镖车功能
    :return:
    """

    # 点击'跨服''
    mouse.click(1616, 888)
    time.sleep(0.5)
    # 点击跨服押镖
    mouse.click(1735, 513)
    time.sleep(0.5)
    # 点击抢夺镖车
    mouse.click(1413, 943)
    time.sleep(0.5)
    # 确认抢夺镖车信息
    rob_message_confirm()
    time.sleep(0.5)
    # 检查夺标令数量
    rob_token = get_rob_token()
    while rob_token is not None and rob_token > 0:
        # 检查抢夺冷却时间
        while not get_rob_cd():
            # 冷却时间如果没过，则5秒后再次检查
            print('目前处于抢夺冷却期，10秒后再次检查')
            time.sleep(10)
        # 抢夺期已过，点击抢夺列表
        mouse.click(1394, 506)
        time.sleep(1)
        # 抢夺列表内监测可抢夺对象
        rob_list()
        # 进入战斗界面等待30秒
        time.sleep(30)
        print('进入抢夺CD期，160秒后再次尝试')
        # 再次检查夺标令数量
        rob_token = get_rob_token()
        time.sleep(1)
        rob_message_confirm()
    else:
        # 确认抢夺镖车信息
        rob_message_confirm()
        time.sleep(3)
        content = '夺标令数量不足，关闭跨服押镖界面'
        print(content)
        # 关闭跨服押镖
        mouse.click(1861, 177)
        try:
            speaker.Speak(content)
        except:
            pass


def pk_icon():
    """
    立即截取主界面'野战'位置坐标的图标，并判断是否是'野战'，如果是则点击进入
    :return: 返回是否是'野战'图标,bool
    """

    position = (1846, 585, 1877, 617)
    filename = 'temp_pk.bmp'
    x, y = snapshot(position, filename)
    result, similarity = compare_image('pk.bmp', filename, arg=0.7)
    print('野战图标相似度:%s' % similarity)
    if result:
        print('打开野战菜单')
        mouse.click(x, y)
        time.sleep(1)
        return True
    return False


def slide(number=7):
    """
    '野战界面'向上滑动鼠标
    :param number: 滑动次数
    :return:
    """
    x, y = 1600, 590

    for num in range(number):
        mouse.press(x, y)
        time.sleep(0.8)
        mouse.release(x, y - 150)
    time.sleep(3)


def get_pkname(ly, ry):
    """
    根据'野战'菜单第一行人员位置，获取'野战'姓名
    :return: str [姓名 等级]
    """
    position = (1487, ly - 74, 1740, ry - 74)
    filename = 'pkname.bmp'
    snapshot(position, filename)
    # time.sleep(2)
    rgb_file = rgb_filter(filename, r_threshold=100, g_threshold=0, b_threshold=0)
    # time.sleep(2)
    words = get_content_local(rgb_file)
    print(words)
    del_symbol = re.compile('[ ?”]+')
    words = del_symbol.sub('', words)
    # print(words)
    pk_pattern = re.compile('(.*?)(\d{1,2}转\d+.)')
    info = pk_pattern.match(words).groups()
    if len(info) == 2:
        return info
    return None


def competitor_inspection_time():
    """
    野战寻找对手剩余时间
    :return:
    """
    pattern = re.compile('.*?(\d{1,2}).*?分(\d{1,2}).*')
    position = (1403, 810, 1483, 829)
    filename = 'competitor_inspection_time.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=80, g_threshold=30, g_compare='<')
    words = get_content_local(rgb_file)
    result = pattern.findall(words)
    print('捕获字符串：%s' % words)

    now = datetime.datetime.now()
    if len(result) == 1:
        minute, second = int(result[0][0]), int(result[0][1])
        add_time = datetime.timedelta(minutes=minute, seconds=second)
        next_time = (now + add_time).strftime("%Y-%m-%d %H:%M:%S")
        print('%2d分%02d秒后出现新敌人，任务下次运行时间:%s' % (minute, second, next_time))
        return next_time
    return None


@cost_time
def auto_pk(opeart='down'):
    """
    自动野战功能
    :return:
    """
    white_list = ['庞', '妙', '细', '雨梅', '蒋', '黎昕', '马', '叶', '卫文', '诗蕾']
    # 确认是否有押解囚犯奖励，有则领取，防止挡界面
    confirm_prisoner_award()
    if in_city(click=False):
        return False
    if pk_icon():
        if opeart == 'up':
            position = (1799, 469, 1868, 497)
        else:
            time.sleep(1)
            position = (1799, 665, 1868, 693)
            slide()

        # 获取下次出现敌人的时间
        next_time = competitor_inspection_time()
        job = scheduler.get_job(job_id='auto_pk')
        if job:
            job.modify(next_run_time=next_time)
        time.sleep(2)
        filename = 'challenge.bmp'
        x, y = snapshot(position, filename)
        # time.sleep(2)
        challenge_file = rgb_filter(filename, r_threshold=160, g_threshold=130, b_threshold=70)
        # time.sleep(1)
        words = get_content_local(challenge_file)
        print('挑战按钮文字识别:%s' % words)
        if '挑' in words or '战' in words:
            name_info = get_pkname(position[1], position[3])
            if name_info:
                name = name_info[0].strip()
                rank = name_info[1].strip()
                content = '野战:%s\t%s' % (name, rank)
            else:
                name = None
                content = '野战，未获取到姓名'

            if name is not None:
                in_while_list = False
                for white_name in white_list:
                    if white_name in name:
                        in_while_list = True
                        break
                if in_while_list:
                    print('白名单：%s，跳过' % name)
                    # 关闭菜单
                    mouse.click(1860, 165)
                else:
                    # 点击挑战对手
                    mouse.click(x, y)
                    print(content)
                    record_log(filename=normal_log, content=content)
                    time.sleep(5)
                    num = 0
                    while fight_result() is None:
                        if num % 10 == 0:
                            print('战斗中...')
                        time.sleep(1)
                        if num >= 45:
                            content = 'pk卡住，添加任务重试'
                            print(content)
                            # 超时45秒，插入1次auto_pk任务,并直接返回程序
                            queue_jobs_list.insert(0, 'auto_pk')
                            record_log(filename=normal_log, content=content)
                            return True
                        num += 1
                return True
            else:
                # 关闭菜单
                mouse.click(1860, 165)
                return True
        else:
            # 关闭菜单
            mouse.click(1860, 165)
            return True

    return False


def in_city(click=True, out=False, report=False):
    """
    立即截取主界面'主城'位置坐标的图标，如果匹配说明不在主城，并点击进入
    :param click:bool 不在主城时是否点击进入
    :param out:bool 在主城时,是否点击出城
    :param report:bool 是否打印信息
    :return:在主城返回是，不在则否，bool
    """
    # if not game_method(click=False):
    #     print('非空闲状态，跳过城市检测')
    #     return None

    position = (1776, 132, 1819, 156)
    filename = 'temp_city.bmp'

    snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=135, g_threshold=90)
    words = get_content_local(rgb_file)
    # print(words)
    # match_word = city_pattern.findall(words)
    if '蓝' in words or '月' in words:
        if out:
            if report:
                print('在主城，点击出城')
            mouse.click(1865, 1030)
            return True
        else:
            if report:
                print('在主城')
            return True
    else:
        if click:
            if report:
                print('不在主城，点击进入')
            # click选项为真，点击进入主城
            mouse.click(1865, 1030)
            return False
        else:
            if report:
                print('不在主城')
            return False


def in_fight_scene():
    """
    检查是否在战斗画面
    :param handle:
    :return:
    """
    position = (1318, 128, 1408, 168)
    filename = 'temp_fight_scene.bmp'
    snapshot(position, filename)
    check, similarity = compare_image('fight_scene.bmp', filename, arg=0.81)
    print('战斗界面中检测: ', check, similarity)
    if check:
        # print('战斗界面中')
        return True
    return False


def soldier_icon(click=False):
    """
    立即截取主界面'大刀侍卫'攻击位置坐标的图标
    :return: 返回是否是大刀侍卫图标,bool
    """

    position = (1843, 491, 1883, 552)
    filename = 'temp_soldier_ico.jpg'
    x, y = snapshot(position, filename)
    result, similarity = compare_image('soldier_ico.jpg', filename, arg=0.8)
    if result:
        if click:
            mouse.click(x, y)
            time.sleep(1)
        return True
    return False


def soldier_lived():
    """
    判断大刀侍卫是否存活
    :return:存活返回True,不存活返回False,bool
    """
    # 确认是否有押解囚犯奖励，有则领取，防止挡界面
    confirm_prisoner_award()

    resurgence_time = soldier_resurgence_time()
    # print(resurgence_time)
    if not resurgence_time:
        # 如果没有获取到时间，说明大刀侍卫已经复活
        return True
    now = datetime.datetime.now()
    if now >= resurgence_time:
        # 当前时间大于记录的时间，说明已经复活
        return True
    else:
        # 当前时间小于获取的时间，说明大刀侍卫尚未复活
        return False


@set_single
def soldier_resurgence_time_from_message():
    """
    从游戏中获取大刀侍卫复活时间
    :return:
    """

    position = (1668, 961, 1742, 978)
    filename = 'soldier_resurgence_time.bmp'
    snapshot(position, filename)
    new_filename = rgb_filter(filename, r_threshold=70, g_threshold=45, b_threshold=45, r_compare='>', g_compare='<',
                              b_compare='<')
    words = get_content_local(new_filename, lang='legend_figure')
    print('复活时间字符串:', words)
    time_pattern = re.compile('(\d{2}).?(\d{2}).?(\d{2})')
    if 6 <= len(words) <= 8:
        result = time_pattern.match(words)
        # print(result)
        if result:
            # 获取复活倒计时，时、分、秒
            h, m, s = int(result[1]), int(result[2]), int(result[3])
            # print('复活时间 split:', h, m, s)
            # 复活倒计时转换为datetime对象
            add_time = datetime.timedelta(hours=h, minutes=m, seconds=s)
            # 当前时间加上倒计时时间
            now = datetime.datetime.now()
            resurgence_time = now + add_time
            return resurgence_time
    print('未获取到大刀侍卫复活时间，当前已经复活')
    return None


def soldier_resurgence_time():
    """
    获取大刀侍卫复活时间
    :return:返回大刀侍卫复活时间的datetime的实例
    """
    time_recordfile = 'resurgence_time.conf'
    now = datetime.datetime.now()
    resurgence_time_record = now
    weekend = False
    if now.strftime('%w') in '06':
        weekend = True
    hours = 10
    seconds = 36000
    if weekend:
        hours = 5
        seconds = 18000
    # 从文件读取时间
    time_str = file_operation(time_recordfile, operation='read')
    if time_str:
        # print('文件记录内容：', time_str)
        # 将字符串时间转为datetime对象
        resurgence_time_record = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        # 比较当前时间与文件中记录的时间
        if now < resurgence_time_record < (now + datetime.timedelta(hours=hours)):
            # 如果当前时间小于文件中记录的时间,但不超过5小时,则返回文件中的记录时间
            return resurgence_time_record
    # 如果文件里的时间小于当前时间，则尝试从游戏中的复活时间信息里截取时间
    update_time = soldier_resurgence_time_from_message()
    # record_log('soldier_time.log', update_time)
    if update_time is None:
        # 如果没有获取到游戏中的复活时间信息，说明大刀侍卫活着
        # 如果当前是周日(0)或周六(6) 当前时间-文件中的时间超过5小时(18000秒) 则文件太旧返回当前时间
        if (now - resurgence_time_record).total_seconds() > seconds:
            return now
        # 差值小于5小时就是最新的，返回文件时间
        return resurgence_time_record
    else:
        # 如果游戏里拿到时间，则格式化复活时间
        update_time_format = update_time.strftime("%Y-%m-%d %H:%M:%S")
        # 将游戏中拿到的时间字符串格式存入文件
        file_operation(time_recordfile, operation='write', content=update_time_format)
        print('大刀侍卫复活时间:%s,已更新写入文件:%s' % (update_time_format, time_recordfile))
        # 将datetime格式的时间返回
        return update_time


def pass_soldier_lead_time(lead_time):
    """
    检查当前是否超过大刀侍卫复活前n分钟
    :param lead_time: int 复活前n分钟
    :return:bool 已过复活时间前n分钟返回True,否则为False
    """
    resurgence_time = soldier_resurgence_time()
    skip_time = resurgence_time - datetime.timedelta(minutes=lead_time)
    now = datetime.datetime.now()
    if now > skip_time:
        return True
    return False


def get_red_name_values():
    # position = (1890, 617, 1920, 630)
    position = (1888, 625, 1920, 640)
    filename = 'red_name_values.bmp'
    snapshot(position, filename)
    new_filename = rgb_filter(filename, r_threshold=163, g_threshold=100, b_threshold=100, g_compare='<', b_compare='<')
    words = get_content_local(new_filename, lang='legend_figure')
    try:
        red_name_value = int(words)
    except:
        return None
    # print(red_name_value)
    if 0 <= red_name_value <= 100:
        return red_name_value
    return None


def blood_status():
    position = (1376, 1017, 1382, 1020)
    filename = 'temp_blood_status.bmp'
    snapshot(position, filename)
    result, similarity = compare_image('blood_status.bmp', filename, arg=0.8)
    # print(similarity)
    if result:
        return True
    return False


@cost_time
def kill_soldier():
    """
    攻击大刀侍卫功能
    :return:
    """
    # 为了防止复活时间不刷新，点击两次主城
    # 点击主城
    mouse.click(1855, 1030)
    time.sleep(0.6)
    # 再次点击主城
    mouse.click(1855, 1030)
    time.sleep(0.6)

    # 防止押解囚徒奖励挡画面
    confirm_prisoner_award()
    time.sleep(1)
    if game_method(click=False):
        # 检测'玩法'图标，如果'玩法'存在，说明在空闲状态
        if soldier_lived():
            log_file = 'soldier.log'
            resurgence_time = soldier_resurgence_time()
            # 检查大刀侍卫是否存活
            content = '大刀侍卫已经复活，尝试攻击'
            print(content)
            record_log(log_file, content)
            # 检查是否在主城，不在则点击进入
            in_city(click=True, report=True)
            # 点击次数
            click_times = 0
            # 攻击次数
            try_times = 0
            # 上一轮攻击次数
            last_try_times = -1
            # 上次红名值
            last_red_name_values = 0
            while True:
                click_times += 1
                # 每点击20次，如果上次攻击次数等于当前攻击次数，则说明上次攻击周期没有掉血，可能大刀侍卫已经死亡
                if click_times % 20 == 0 and last_try_times == try_times:
                    now = datetime.datetime.now()
                    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                    expenditure_minutes = (now - resurgence_time).seconds / 60
                    print('%s\t耗时:%0.2f分,攻击次数:%d,点击次数:%s' % (now_str, expenditure_minutes, try_times, click_times))
                    if not soldier_lived():
                        now = datetime.datetime.now()
                        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                        expenditure_minutes = (now - resurgence_time).seconds / 60
                        content = '大刀侍卫已经死亡,耗时:%0.2f分,攻击次数:%d,点击次数:%d' % (expenditure_minutes, try_times, click_times)
                        print('%s  %s' % (now_str, content))
                        record_log(log_file, content)
                        queue_jobs_list.insert(0, 'auto_pk')
                        queue_jobs_list.insert(0, 'auto_pk')
                        queue_jobs_list.insert(0, 'clean_bag')
                        break
                    # 如果大刀侍卫没有死亡，点击2次主城，防止血量卡住，刷新血量
                    mouse.click(1855, 1030)
                    time.sleep(0.6)
                    mouse.click(1855, 1030)
                    time.sleep(0.3)
                    # 如果大刀侍卫没有死亡，检查是否离线
                    check_offline()
                    in_city(click=True, report=True)
                # 点击大刀侍卫头像
                mouse.click(1865, 551)
                # 每点击20次，将当前攻击次数赋值给上次攻击次数
                if click_times % 20 == 0:
                    last_try_times = try_times
                if blood_status() is False:
                    # 血量减少，攻击次数+1
                    try_times += 1
                    if last_red_name_values < 100:
                        # 上次红名值如果小于100，不延时
                        delay_time = 0
                        # 获取当前红名值
                        red_name_values = get_red_name_values()
                        if red_name_values is not None:
                            # 当前红名值不为空时，第一次点击时，当前红名值直接赋值给上次

                            if try_times <= 3:
                                last_red_name_values = red_name_values
                            else:
                                # 第一次点击之后，红名值对比上次的值如果在-2,2之间才赋值给上次
                                if -2 <= (red_name_values - last_red_name_values) <= 10:
                                    last_red_name_values = red_name_values
                        else:
                            # 当前红名值为空时，设置当前红名值为-1
                            red_name_values = -1
                    else:
                        # 上次红名值大于等于100时，不延时
                        delay_time = 2.4
                    time.sleep(delay_time)
                    print('血量降低，攻击次数:%3d，点击次数:%4d，延时:%3.2f，红名值(上次值):%d(%d)' % (
                        try_times, click_times, delay_time, red_name_values, last_red_name_values))
                    # 点击主城
                    mouse.click(1855, 1030)
                    time.sleep(0.6)
                    # 再次点击主城
                    mouse.click(1855, 1030)

                # 血量没减少时，间隔0.6秒点击大刀侍卫头像
                time.sleep(0.6)

            # 如果已经打完大刀侍卫，则出城练级
            in_city(click=False, out=True)
        else:
            # 大刀侍卫没有复活，检查是否在城市，在城市则出城
            in_city(click=False, out=True)
            print('大刀侍卫未复活，继续练级')

    else:  # 没有玩法图标，说明可能在战斗等页面，放弃检查
        print('非空闲状态，跳过大刀侍卫状态检测')


@cost_time
@set_lock
def clean_bag():
    """
    清理背包功能
    :return:
    """
    # 确认是否有押解囚犯奖励，有则领取，防止挡界面
    confirm_prisoner_award()
    time.sleep(1)
    if in_city(click=False, out=True):
        print('背包清理检测，在主城，出城练级')
        time.sleep(1)

    # 点击背包图标
    mouse.click(1757, 1025)
    time.sleep(1)
    # 点击回收
    mouse.click(1809, 833)
    time.sleep(1)
    position = (1430, 400, 1500, 468)
    filename = 'first_box.jpg'
    snapshot(position, filename)
    clean_amount_temp = 0
    while not compare_image('nothing.jpg', filename)[0]:
        if clean_amount_temp >= 15:
            # 防止背包没有关闭卡界面，点击右上角关闭
            mouse.click(1860, 170)
            break
        clean_amount_temp += 1
        # 点击实际回收按钮
        mouse.click(1622, 835)
        time.sleep(0.5)
        snapshot(position, filename)
        print('清理背包%s\t' % clean_amount_temp, end='')
    else:
        print('\n已经清理完毕，关闭背包')
    # 背包界面右下角关闭按钮，大概公会上方的位置
    mouse.click(1864, 848)


def cheack_auto_fight_str():
    position = (1816, 795, 1905, 819)
    filename = 'temp_autofight.bmp'
    snapshot(position, filename)
    rgb_filename = rgb_filter(filename, r_threshold=160, g_threshold=100, b_threshold=70)
    words = get_content_local(rgb_filename, lang='chi_sim')
    return words


def union_boss_str():
    """
    右下角公会BOSS被召唤文字如果遮挡自动战斗，调用公会BOSS任务
    :return:
    """
    position = (1728, 804, 1810, 827)
    filename = 'union_boss_str.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=80)
    words = get_content_local(rgb_file)
    print('检测是否存在公会BOSS文字遮挡，检测文字：%s' % words)
    result = False
    keywords = ['公会', 'BO', 'SS']
    for keyword in keywords:
        if keyword in words:
            result = True
            break
    if result:
        print('公会文字遮挡，调用公会BOSS任务，捕获文字%s' % words)
        union_boss()
        return True
    return False


@cost_time
def auto_fight():
    """
    自动战斗功能
    :return:
    """
    # 确认是否有押解囚犯奖励，有则领取，防止挡界面
    confirm_prisoner_award()
    # 防止公会BOSS被召唤文字遮挡
    union_boss_str()

    if in_city(click=False):
        return False
    words = cheack_auto_fight_str()
    print('自动挑战关卡，战斗检测文字:%s' % words)
    if words == '自动战斗':
        start_time = datetime.datetime.now()
        # 点击自动战斗
        mouse.click(1860, 808)
        # 点击后，关卡文字变为"自动战斗中"，设置字符串
        words = '自动战斗中'
        # 循环检测关卡文字，一旦是'自动战斗'字样，说明已经失败
        while '战斗' in words and '自动战斗' != words:
            time.sleep(2)
            num = 0
            while in_fight_scene() is False:
                # 如果不在战斗界面，并且是第一次，说明正在等待进入战斗，每3秒重新检查一次
                if num == 0:
                    print('等待进入战斗')
                num += 1
                # 3x15=45秒如果没有进入战斗则跳过
                if num > 15:
                    print('45秒未进入战斗，跳过等待，检查是否离线')
                    queue_jobs_list.insert(0, 'check_offline')
                    return True
                time.sleep(3)
            num = 0
            while in_fight_scene():
                if num == 0:
                    print('进入战斗界面，挑战关卡守卫')
                result = None
                wait_num = 0
                while result is None:
                    if wait_num % 10 == 0:
                        print('战斗中...')
                    if wait_num >= 40:
                        print('40秒未脱离战斗，检查是否离线')
                        queue_jobs_list.insert(0, 'check_offline')
                        return True
                    result = fight_result()
                    time.sleep(1)
                    wait_num += 1
                num += 1
                time.sleep(2)
            if result:
                words = cheack_auto_fight_str()
                print('闯关成功，脱离战斗界面,等待进入下一场,检测文字:%s \n' % words)
            else:
                # 挑战失败，任务挑战完成，返回True
                print('战斗失败，退出')
                return True
        print('战斗失败，退出，检测文字:%s' % words)
    return False


def random_action():
    """
    自动战斗、闯天关、锁妖塔、公会秘境BOSS 动作随机挑选功能，data字典里数值越大，机会越高
    :return:
    """
    data = {'auto_fight': 20, 'endless_barrier': 15, 'monster_tower': 1, 'secret_boss': 1}
    all_data = []
    for key, weight in data.items():
        temp = []
        for i in range(weight):
            temp.append(key)
        all_data.extend(temp)
    index = random.randint(0, len(all_data) - 1)
    # print(all_data)
    # print(index)
    selected_action = all_data[index]
    return selected_action


def game_method(click=True):
    """
    监测玩法图标
    :param click:bool default:True 存在则进入
    :return: bool 存在返回True 否则False
    """

    position = (1763, 892, 1799, 924)
    filename = 'temp_game_method.bmp'
    x, y = snapshot(position, filename)
    # time.sleep(1)
    result, similarity = compare_image('game_method.bmp', filename, arg=0.7)
    print('玩法相似值:%s' % similarity)
    if result:
        if click:
            # print('点击玩法')
            mouse.click(x, y)
            # time.sleep(1)
        return True
    return False


@cost_time
def endless_barrier():
    """
    闯天关
    :return:
    """
    # 确认是否有押解囚犯奖励，有则领取，防止挡界面
    confirm_prisoner_award()
    if game_method():
        print('挑战天关')
        time.sleep(1)
        # 点击闯天关
        mouse.click(1621, 286)
        time.sleep(1)
        # 点击挑战
        mouse.click(1816, 909)
        time.sleep(3)
        num = 0
        while in_fight_scene():
            if num == 0:
                print('进入战斗界面')
            if fight_result() is False:
                break
            num += 1
            time.sleep(2)
        return True
    return False


@cost_time
def monster_tower():
    """
    锁妖塔
    :return:
    """
    if game_method():
        print('挑战锁妖塔')

        time.sleep(1)
        # 点击锁妖塔
        mouse.click(1622, 714)
        time.sleep(1)
        # 点击挑战
        mouse.click(1796, 819)
        time.sleep(5)
        num = 0
        while in_fight_scene():
            if num == 0:
                print('进入战斗界面')
            if fight_result() is False:
                break
            num += 1
            time.sleep(2)
        return True
    return False


def confirm_prisoner_award():
    """
    领取押解囚徒奖励
    :return:
    """
    now = datetime.datetime.now()
    now_strf = now.strftime("%Y-%m-%d %H:%M:%S")

    filename = 'temp_confirm_prisoner.bmp'
    position = (1461, 749, 1557, 779)
    snapshot(position, filename)
    get_award_file = rgb_filter(filename, r_threshold=50, g_threshold=50, b_threshold=50)
    words = get_content_local(get_award_file, lang='chi_sim')
    if words == '领取奖励':
        time.sleep(1)
        mouse.click(1472, 763)
        content = '%s 领取押解奖励' % now_strf
        print(content)
        record_log(prisoner_log, content=content)


def boss_icon(click=True):
    """
    立即截取主界面'boss'位置坐标的图标，并判断是否是'boss'，如果是则点击进入
    :return: 返回是否是'boss'图标,bool
    """

    position = (1672, 883, 1718, 924)
    filename = 'temp_boss.bmp'
    x, y = snapshot(position, filename)
    result, similarity = compare_image('boss.bmp', filename, arg=0.7)
    print('BOSS图标相似值: %s' % similarity)
    if result:
        if click:
            print('打开BOSS菜单')
            mouse.click(x + 5, y - 10)
        return True
    return False


def practice_icon(click=True):
    """
    立即截取主界面'修炼'位置坐标的图标，并判断是否是'修炼'，如果是则点击进入
    :return: bool 返回是否是'修炼'图标
    """

    position = (1505, 881, 1544, 921)
    filename = 'temp_practice.bmp'
    x, y = snapshot(position, filename)
    result, similarity = compare_image('practice.bmp', filename, arg=0.7)
    print('修炼图标相似值:%s' % similarity)
    if result:
        if click:
            print('打开修炼菜单')
            mouse.click(x + 5, y - 10)
        return True
    return False


def union_icon(click=True):
    """
    检查公会图标是否存在
    :param click: bool default:True 是否点击进入
    :return: 存在图标返回True 否则返回False
    """

    position = (1848, 872, 1880, 913)
    filename = 'temp_union_icon.bmp'
    x, y = snapshot(position, filename)
    # time.sleep(1)
    result, similarity = compare_image('union_icon.bmp', filename, arg=0.7)
    print('公会图标相似值:%s' % similarity)
    if result:
        if click:
            print('打开公会菜单')
            mouse.click(x, y)
            # time.sleep(1)
        return True
    return False


def ladder_cost():
    position = (1555, 713, 1605, 741)
    filename = 'ladder_cost.bmp'
    snapshot(position, filename)
    words = get_content_local(filename, lang='legend_figure')
    cost_list = re.split('[ /]', words)
    if len(cost_list) == 2:
        cost = int(cost_list[0])
        # print('剩余次数:%d' % cost)
        return cost
    return None


def ladder_fight():
    """
    天梯挑战
    :return:
    """
    if game_method():
        time.sleep(1)
        # 点击天梯玩法
        mouse.click(1625, 570)
        time.sleep(1)
        cost = ladder_cost()
        print('天梯剩余次数:%d' % cost)
        if 5 <= cost <= 6:
            # 点击匹配对手
            content = '天梯匹配对手'
            print(content)
            record_log(filename=normal_log, content=content)
            mouse.click(1609, 817)
            time.sleep(5)
            while in_fight_scene():
                print('进入战斗界面')
                time.sleep(5)
            # 关闭天梯
            print('战斗完毕，关闭天梯')
            mouse.click(1858, 168)
            return True
        else:
            # 关闭天梯
            print('剩余次数不足，关闭天梯')
            mouse.click(1858, 168)
            return True
    else:
        print('未检测到玩法界面，跳过天梯')
        return False


def boss_cost_from_file():
    """
    检查boss消耗情况
    :return:int 返回当前可以打boss的次数
    """
    boss_cost_info_file = 'boss_cost.conf'
    boss_cost_info = file_operation(boss_cost_info_file)
    national_date, national_num, god_date, god_num = boss_cost_info.split(',')
    return national_date, national_num, god_date, god_num


def boss_cost(boss, lang='legend_figure', independent=False, refresh=False, close=False):
    """
    获取全民/神域boss的剩余消耗量，如果文件中有一段时间内的信息，直接返回文件内的信息，否则开boss菜单获取
    :param boss: str ['national','god'] boss的种类
    :param lang: str default:'legend_figure' 识别语言
    :param independent: bool 是否可以开启boss菜单独立检查消耗量
    :param refresh:bool 是否直接更新文件中的信息
    :param close:bool 开启independent选项后，默认不关闭boss菜单，控制是否需要关闭菜单
    :return:int 返回剩余消耗量
    """

    now = datetime.datetime.now()
    boss_cost_info_file = 'boss_cost.conf'
    national_date, national_num, god_date, god_num = boss_cost_from_file()
    # 将字符串时间转为datetime对象
    national_date_datetime = datetime.datetime.strptime(national_date, '%Y-%m-%d %H:%M:%S')
    god_date_datetime = datetime.datetime.strptime(god_date, '%Y-%m-%d %H:%M:%S')
    if not refresh:
        if boss == 'national':
            if now < national_date_datetime + datetime.timedelta(minutes=15):
                return int(national_num)
        if boss == 'god':
            if now < god_date_datetime + datetime.timedelta(minutes=30):
                return int(god_num)

    if independent:
        if boss_icon():
            time.sleep(1)
            if boss == 'national':
                # 点击'全民'字样
                mouse.click(1513, 939)
                time.sleep(1.3)
            if boss == 'god':
                # 点击'神域'字样
                mouse.click(1625, 935)
                time.sleep(1.3)
        else:
            return False

    position = (1424, 270, 1482, 290)
    filename = 'temp_boss_cost.bmp'
    snapshot(position, filename)
    # time.sleep(2)
    rgb_filename = rgb_filter(filename, r_threshold=50, g_threshold=50, b_threshold=50)
    # time.sleep(1)
    words = get_content_local(rgb_filename, lang=lang)
    print('消耗量字符串:', words)
    state = re.split('[/ ]', words)
    if len(state) == 2:
        number = state[0]
        non_figure = re.compile('[^\d]')
        if len(non_figure.findall(number)) == 0:
            if boss == 'national':
                national_num = number
                content = '%s,%s,%s,%s' % (now.strftime('%Y-%m-%d %H:%M:%S'), national_num, god_date_datetime, god_num)
                print('全民boss消耗量剩余: %s 已更新文件' % national_num)
            if boss == 'god':
                god_num = number
                content = '%s,%s,%s,%s' % (
                    national_date_datetime, national_num, now.strftime('%Y-%m-%d %H:%M:%S'), god_num)
                print('神域boss消耗量剩余: %s 已更新文件' % god_num)
            file_operation(boss_cost_info_file, operation='write', content=content)
            if close:
                print('关闭BOSS菜单\n')
                mouse.click(1861, 166)
            return int(number)
    if close:
        print('关闭BOSS菜单\n')
        mouse.click(1861, 166)
    return None


def boss_cost_sub(boss):
    """
    boss消耗量-1
    :param boss: str [ 'national','god']
    :return:
    """
    boss_cost_info_file = 'boss_cost.conf'
    boss_cost_info = file_operation(boss_cost_info_file)
    national_date, national_num, god_date, god_num = boss_cost_info.split(',')
    if boss == 'national':
        national_num_int = int(national_num)
        if national_num_int != 0:
            national_num_int -= 1
        content = '%s,%s,%s,%s' % (national_date, str(national_num_int), god_date, god_num)
        file_operation(boss_cost_info_file, operation='write', content=content)
        print('全民boss消耗量已减少,剩余:%s ，更新文件' % str(national_num_int))
    if boss == 'god':
        god_num_int = int(god_num)
        if god_num_int != 0:
            god_num_int -= 1
        content = '%s,%s,%s,%s' % (national_date, national_num, god_date, str(god_num_int))
        file_operation(boss_cost_info_file, operation='write', content=content)
        print('神域boss消耗量已减少，剩余:%s ，更新文件' % str(god_num_int))


def boss_attack_amount():
    """
    获取boss争夺人数，如果boss没有复活，人数设置为-1
    :return:boss争夺人数的信息字典{0:[0,(x,y)],1:[1,(x,y)]}
    """
    position = [1825, 424, 1867, 445]
    # 记录boss信息的字典{0:['0',(x,y)],1:['1',(x,y)]}
    boss_info = {}
    for index in range(3):
        num = -1
        filename = 'boss_p' + str(index + 1) + '.bmp'
        x, y = snapshot(position, filename)
        rgb_filename = rgb_filter(filename, r_threshold=190, g_threshold=110, b_threshold=10, b_compare='<')
        y -= 35
        words = get_content_local(rgb_filename, lang='legend_attacknum')
        # print(words)
        pattern = re.compile('\d+')
        words = pattern.findall(words)
        # print(words)
        if len(words) != 0:
            num = int(words[0])
        mouse_position = x, y
        boss_info[index] = [num, mouse_position]
        position[1] += 165
        position[3] += 165
    return boss_info


def select_boss():
    """
    选择全民神域中的可攻击BOSS，并优先选择高级的
    :return: bool 发现可攻击BOSS返回True 否则返回False
    """
    global boss_position
    boss_info = boss_attack_amount()
    for index in range(2, -1, -1):
        if boss_info[index][0] == 0:
            boss_position = boss_info[index][1]
            return True
        if index == 2:
            if boss_info[index][0] >= 0:
                boss_position = boss_info[index][1]
                return True
    return False


def get_owner_name():
    """
    获取Boss归属人
    :return:
    """
    name_log = 'name.log'
    position = (1455, 301, 1550, 325)
    filename = 'owner_name.bmp'
    snapshot(position, filename)
    owner_name_file = rgb_filter(filename, r_threshold=100)
    words = get_content_local(owner_name_file)
    # print(words)
    if words:
        # record_log(name_log, content=words)
        return words
    else:
        return None


def i_am_owner():
    """
    检查自己是否归属人
    :return:
    """
    my_names = ['大豆', '太豆']
    owner_name = get_owner_name()
    for my_name in my_names:
        if my_name in owner_name:
            return True, '大豆'
    return False, owner_name


def is_enemy(name):
    black_list = ['肥龙', '大招', '低调', '顾云', '龙哥', '霸', '星月', '青丶山', '周博涛', '游戏', '人生', '虚无', '罗若', '莲叶', '自闭', '菜',
                  '江湖', '一', '易文', '乐', '逍遥', '轻念', '惜珊', '吴楷', '雪妖', '赵鑫磊', '如风', '孙晟', '古冰', '李煜', 'midea']
    # black_list = ['星月', '臧', '翠', '萱', '凤', '青丶山', '肥龙', '大招', '雪地', '周博涛', '哼', 'midea', '王雪松', '施天宇', '离心、天曼', '缥缈',
    #               '容凌青', '皇甫', '罗若烟', '洛北北']
    # white_list = ['刺槐', '黎', '昕', '庞', '妙', '吉', '寻', '曙光', '梦山', '褚鸿', '玩味', '苦涩', '马', '李修', '钱', '仇', '孔', '相思',
    #               '笑叹',
    #               '怀', '王雪']
    # for white_name in white_list:
    #     if white_name in name:
    #         return False
    # return True
    for black_name in black_list:
        if black_name in name:
            return True
    return False


def rob_owner():
    """
    抢夺BOSS归属权
    :return:
    """

    result, owner_name = i_am_owner()

    if result is False:
        if is_enemy(owner_name):
            mouse.click(1617, 846)
            content = '尝试攻击黑名单:%s' % owner_name
            print(content)
        else:
            content = '当前BOSS归属人,不在黑名单内:%s' % owner_name
            print(content)
        copy_image('owner_name.bmp', new_dir='rob_name')
        copy_image('rgb_owner_name.bmp', new_dir='rob_name')
    else:
        content = 'BOSS归属人:大豆'
        print(content)
    record_log(boss_log, content=content)


def fight_with_boss(boss, residue):
    """
    全民/神域 BOSS 点击'挑战'后血量判断以及归属权抢夺
    :param boss:
    :param residue:
    :return:
    """

    # 初始血量
    blood = 99
    # 上次血量
    last_blood = [100]
    # 上次血量初始索引
    last_blood_index = 0
    if boss == 'national':
        # 点击'全民'选项卡
        mouse.click(1513, 939)
        print('全民boss次数:%d' % residue)
        content = '攻击全民BOSS'
    if boss == 'god':
        # 点击'神域'选项卡
        mouse.click(1625, 935)
        print('神域boss次数:%d' % residue)
        content = '攻击神域BOSS'
    time.sleep(1)

    if select_boss():
        x, y = boss_position
        print('检测到符合的BOSS，尝试攻击')
        # 点击选出的BOSS
        mouse.click(x, y)
        # 记录日志
        record_log(boss_log, content=content)
        boss_cost_sub(boss=boss)
        time.sleep(2)
        # 设置计数器num 防止卡住后一直等待获取血量
        num = 0
        while blood > 0 and num < 200:
            num += 1
            blood = get_boss_blood()
            # print(last_blood[last_blood_index], blood)
            difference = last_blood[last_blood_index] - blood
            if difference > 15 or difference < 0:
                blood = last_blood[last_blood_index]
                continue
            # 整数显示剩余血量 90% 80%
            if blood % 10 == 0:
                print('BOSS血量小于%d' % blood)
            if 2 <= blood < 30:
                rob_owner()
            last_blood.append(blood)
            # print(last_blood)
            last_blood_index += 1
            time.sleep(0.8)
        # 等待3秒确认收益
        time.sleep(3)
        # 再插入一条任务，尝试检查BOSS
        queue_jobs_list.insert(0, 'auto_boss')
        return True
    else:
        print('未检查到可攻击的BOSS')


@cost_time
@set_lock
def auto_boss(national=True, god=True):
    """
    自动攻击全民/神域boss
    :param national: bool 是否检查全民boss
    :param god: bool 是否检查神域boss
    :return: bool 是否执行成功
    """

    # if boss_icon(click=False) is False:
    #     print('不在空闲状态，跳过执行')
    #     return False
    national_residue = boss_cost(boss='national', independent=True, close=True)
    time.sleep(1)
    god_residue = boss_cost(boss='god', independent=True, close=True)
    time.sleep(1)
    if national_residue == 0 and god_residue == 0:
        print('全民/神域 BOSS剩余消耗量不足，跳过执行')
        return False
    if boss_icon():
        time.sleep(2)
        if national and national_residue is not None and national_residue != 0:
            fight_with_boss(boss='national', residue=national_residue)
        if god and god_residue is not None and god_residue != 0:
            fight_with_boss(boss='god', residue=god_residue)
        print('关闭菜单')
        mouse.click(1861, 171)
    return False


def public_message():
    position = (1383, 328, 1890, 357)
    filename = 'public_message.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=130, g_threshold=50, b_threshold=50, g_compare='<', b_compare='<')
    words = get_content_local(rgb_file)
    if '囚' in words or '终极' in words:
        print('public words :%s' % words)
        escort_prisoner()
        return True
    else:
        return False


def union_message_monitor():
    """
    公会信息监控,用于发现公会boss，和红包发布信息
    :return:
    """
    position = (1473, 358, 1794, 388)
    union_filename = 'chat_message_union.bmp'
    snapshot(position, union_filename)
    return union_filename


def union_boss_monitor():
    position = (1590, 360, 1755, 388)
    union_filename = 'chat_message_union.bmp'
    snapshot(position, union_filename)
    chat_log = 'chat.log'
    union_boss_file = rgb_filter(union_filename, r_threshold=160, g_threshold=80, b_threshold=10, b_compare='<')
    union_boss_message = get_content_local(union_boss_file)
    # print(union_boss_message)
    if '公会' in union_boss_message or 'SS' in union_boss_message:
        queue_jobs_list.insert(0, 'union_boss')
        queue_jobs_list.insert(0, 'union_boss')
        scheduler.modify_job(job_id='execute_jobs', next_run_time=datetime.datetime.now())
        content = '公会BOSS被召唤，已插入公会BOSS任务，捕获文字: %s' % union_boss_message
        record_log(chat_log, content=content)
        print(content)
        copy_image(union_filename, new_dir='union_boss')
        copy_image(union_boss_file, new_dir='union_boss')
        return True
    return False


def red_bag_monitor():
    chat_log = 'chat.log'
    union_filename = 'chat_message_union.bmp'
    red_bag_file = rgb_filter(union_filename, r_threshold=160, g_threshold=160, b_threshold=160)
    red_bag_message = get_content_local(red_bag_file)
    if '普天' in red_bag_message or '红包' in red_bag_message:
        copy_image(union_filename, new_dir='red_bag')
        copy_image(red_bag_file, new_dir='red_bag')
        content = '发现公会红包:%s' % red_bag_message
        record_log(chat_log, content=content)
        print(content)
        for num in range(5):
            if red_bag():
                record_log(chat_log, content='已经领取')
                return True
            if num < 4:
                print('红包领取失败,3秒钟后再次尝试:%d' % (num + 1))
            time.sleep(3)
        print('无法领取红包')
        return False


def get_boss_blood():
    position = (1587, 234, 1640, 255)
    filename = 'boss_blood.bmp'
    snapshot(position, filename)
    # time.sleep(1)
    rgb_file = rgb_filter(filename, r_threshold=85, g_threshold=85, b_threshold=126)
    # time.sleep(1)
    words = get_content_local(rgb_file, lang='legend_figure')
    words = words.replace(' ', '')
    find_figure = re.compile('\d{1,3}')
    figure_list = find_figure.findall(words)
    # print(figure_list)
    # record_log('blood.log', figure_list)
    if figure_list:
        figure = int(figure_list[0])
        # print(figure)
        return figure
    return 0


def check_bag_full():
    """
    背包是否满检查
    :return:
    """
    position = (1611, 934, 1769, 962)
    filename = 'bag_full.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=100)
    words = get_content_local(rgb_file)
    print(words)
    key_words = ['回收', '已满', '背包']
    bag_full = False
    for key_word in key_words:
        if key_word in words:
            bag_full = True
            break
    if bag_full:
        clean_bag()
        return True
    return False


def renewing_boss_roll():
    """
    转生BOSS抽奖
    :return:
    """
    # 初始血量
    blood = 99
    # 上次血量
    last_blood = [100]
    # 上次血量初始索引
    last_blood_index = 0
    content = '点击抽奖'

    while blood > 0:
        blood = get_boss_blood()
        difference = last_blood[last_blood_index] - blood
        if difference > 15 or difference < 0:
            blood = last_blood[last_blood_index]
            continue
        if blood % 10 == 0:
            print('BOSS血量小于%d' % blood)
        if 48 < blood <= 50:
            # 点击抽奖
            mouse.click(1610, 556)
        last_blood.append(blood)
        last_blood_index += 1
        time.sleep(3)
    record_log(boss_log, content=content)
    return True


@cost_time
def renewing_boss():
    """
    攻击转生boss
    :return:
    """
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    if boss_icon():
        time.sleep(0.5)
        # 点击'转生'字样
        mouse.click(1755, 938)
        now = datetime.datetime.now()
        start_time = datetime.datetime.strptime(now_date + ' 21:00:00', '%Y-%m-%d %H:%M:%S')
        if now < start_time:
            seconds = (start_time - now).total_seconds()
            seconds_float = float(str(seconds)[:4])
            print(seconds, seconds_float)
            time.sleep(seconds_float)
        # 点击攻击boss
        mouse.click(1621, 836)
        now_time = datetime.datetime.now()
        content = '%s 攻击转生BOSS' % now_time
        print(content)
        time.sleep(0.5)
        if not in_fight_scene():
            now_time = datetime.datetime.now()
            if datetime.datetime.strptime(now_date + ' 20:59:58',
                                          '%Y-%m-%d %H:%M:%S') < now_time < datetime.datetime.strptime(
                        now_date + ' 21:00:04', '%Y-%m-%d %H:%M:%S'):
                renewing_boss()
        else:
            record_log(boss_log, content=content)
            renewing_boss_roll()
        return True
    return False


@cost_time
@set_lock
def lucky_boss():
    # 确认是否有押解囚犯奖励，有则领取，防止挡界面
    confirm_prisoner_award()
    if not in_city(click=False):
        position = (1751, 707, 1758, 735)
        filename = 'temp_lucky_boss.bmp'
        x, y = snapshot(position, filename)
        result, similarity = compare_image('lucky_boss.bmp', filename, arg=0.78)
        # print(similarity)
        if result:
            content = '发现野外BOSS，匹配度:%s,尝试攻击' % similarity
            print(content)
            record_log(boss_log, content)
            mouse.click(x, y)
            time.sleep(1)
            mouse.click(1481, 788)
            time.sleep(30)
            return True
        else:
            content = '未发现野外BOSS，匹配度:%s' % similarity
            print(content)
            return False


@cost_time
def protect_bice():
    """
    每周1、3、5 守卫比奇活动
    :return:
    """

    print('参加保卫比奇活动')
    game_method()
    time.sleep(1)
    # 点击'限时玩法'
    mouse.click(1525, 934)
    time.sleep(0.5)
    # 点击'守卫比奇'
    mouse.click(1576, 278)
    time.sleep(1)
    # 点击自动战斗
    mouse.click(1849, 745)


@cost_time
def night_fight_bice():
    """
    每周2、4、6比奇夜战
    :return:
    """
    # 当前时间点日期
    now = datetime.datetime.now()
    key_date = now.strftime('%Y-%m-%d')
    periods = []
    # 夜战时间
    key_time1 = ['20:30:00', '20:45:00']
    # key_time2 = ['01:40:00', '01:55:00']
    periods.append(key_time1)
    # periods.append(key_time2)
    out = True
    print('参加比奇夜战活动')
    if game_method():
        time.sleep(1)
        # 点击'限时玩法'
        mouse.click(1525, 934)
        time.sleep(1)
        # 点击'夜战比奇'
        mouse.click(1625, 420)
        time.sleep(5)
        num = 0
        while out:
            for period in periods:
                key_start_str = key_date + ' ' + period[0]
                key_end_str = key_date + ' ' + period[1]
                key_start = datetime.datetime.strptime(key_start_str, '%Y-%m-%d %H:%M:%S')
                key_end = datetime.datetime.strptime(key_end_str, '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()
                if not key_start <= now <= key_end:
                    out = False
                    break
            if out:
                if num % 10 == 0:
                    print('攻击卫兵')
                    # 领取奖励位置
                    mouse.click(1459, 872)
                # 第一个士兵头像
                mouse.click(1875, 494)
                time.sleep(1)

            num += 1
        print('夜战比奇活动结束，退出,30秒后确认收益')
        time.sleep(30)
        # 确认收益
        print('确认收益')
        mouse.click(1621, 805)


@cost_time
def multi_pvp():
    """
    通天战场 每周2、4、6  19:30 19:46
    :return:
    """
    # 当前时间点日期
    now = datetime.datetime.now()
    key_date = now.strftime('%Y-%m-%d')
    periods = []
    # 通天战场时间
    key_time1 = ['19:30:00', '19:46:00']
    periods.append(key_time1)

    out = True
    print('参加通天战场活动')
    if game_method():
        time.sleep(1)
        # 点击'限时玩法'
        mouse.click(1525, 934)
        time.sleep(1)
        # 点击'通天战场'
        mouse.click(1615, 714)
        time.sleep(3)
        # 点击空白处
        mouse.click(1615, 714)
        time.sleep(10)
        num = 0
        while out:
            for period in periods:
                key_start_str = key_date + ' ' + period[0]
                key_end_str = key_date + ' ' + period[1]
                key_start = datetime.datetime.strptime(key_start_str, '%Y-%m-%d %H:%M:%S')
                key_end = datetime.datetime.strptime(key_end_str, '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()
                if not key_start <= now <= key_end:
                    out = False
                    break
            if out:
                if num % 10 == 0:
                    print('攻击卫兵')
                    # 领取奖励位置
                    mouse.click(1459, 872)

                # 第一个人物头像
                # mouse.click(1875, 498)
                # 最后一个人物头像
                mouse.click(1869, 680)
                time.sleep(1)
            num += 1
        print('通天战场活动结束，退出')


@cost_time
def personal_boss():
    """
    攻击个人BOSS
    :return:
    """
    if boss_icon():
        time.sleep(1)
        position = (1778, 287, 1843, 318)
        filename = 'personal_boss.bmp'
        x, y = snapshot(position, filename)
        new_file = rgb_filter(filename, r_threshold=200)
        words = get_content_local(new_file)
        # print(words)
        if '战' in words:
            content = '攻击个人BOSS'
            print(content)
            record_log(boss_log, content=content)
            mouse.click(x, y)
            time.sleep(1)
            while in_fight_scene():
                time.sleep(3)
            return True
        else:
            content = '个人BOSS已经全部挑战完毕，关闭界面'
            print(content)
            record_log(boss_log, content=content)
            # 没有挑战字样，说明已经全部打完，则关闭界面
            mouse.click(1857, 166)
            return True
    return False


@cost_time
def check_offline():
    """
    检查游戏是否断线，如果断线自动重连
    :return:
    """
    offline_info = False
    print('检查是否离线')
    position = (1442, 445, 1781, 508)
    filename = 'offline.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=100)
    words = get_content_local(rgb_file)
    print(words)
    time.sleep(1)
    key_words = ['服务器', '重新', '账号', '外挂', '登录']
    for key_word in key_words:
        if key_word in words:
            offline_info = True
            break
    if offline_info:
        content = '服务器断开，重新连接服务器，检查文字：%s' % words
        print(content)
        mouse.click(1509, 592)
        if '外挂' in words:
            time.sleep(5)
            mouse.click(1509, 592)
        record_log(filename=normal_log, content=content)
        time.sleep(25)
        start_game_position = (1518, 866, 1702, 906)
        start_game_filename = 'start_game.bmp'
        snapshot(start_game_position, start_game_filename)
        rgb_start_game_file = rgb_filter(start_game_filename, g_threshold=100)
        start_game_words = get_content_local(rgb_start_game_file)
        print(start_game_words)
        if '开始' in start_game_words or '游戏' in start_game_words:
            content = '开始游戏'
            print(content)
            mouse.click(1595, 883)
            record_log(filename=normal_log, content=content)
            time.sleep(25)
            # 离线收益，点击确定
            content = '确认离线收益'
            print(content)
            mouse.click(1613, 806)
            record_log(filename=normal_log, content=content)
            queue_jobs_list = []
            jobs_creater()
            return True
    return False


def get_magic_weapon_word():
    position = (1362, 268, 1397, 294)
    filename = 'magic.bmp'
    snapshot(position, filename)
    magic_file = rgb_filter(filename, r_threshold=170, g_threshold=150)
    words = get_content_local(magic_file)
    print(words)
    return words


def change_magic(weapon='魂玉金玲'):
    """
    去 舍 磺 吕] 电 机 天 及 妇
    :param weapon:str ['灵宝护符','魂玉金玲','天机晶石']
    :return:
    """

    # # 左按钮
    # mouse.click(1390, 466)
    # # 右按钮
    # mouse.click(1852, 465)
    num = 0
    if practice_icon():
        time.sleep(0.3)
        # 点击法宝
        mouse.click(1448, 764)
        time.sleep(0.5)
        if weapon == '魂玉金玲':
            while get_magic_weapon_word() not in '去也' and num < 8:
                # 左按钮
                mouse.click(1390, 466)
                time.sleep(0.3)
                num += 1
        if weapon == '灵宝护符':
            while get_magic_weapon_word() not in '舍这' and num < 8:
                # 右按钮
                mouse.click(1852, 465)
                time.sleep(0.3)
                num += 1
        if weapon == '天机晶石':
            while get_magic_weapon_word() not in '机' and num < 8:
                # 右按钮
                mouse.click(1852, 465)
                time.sleep(0.3)
                num += 1
        print('更换出战法宝: %s' % weapon)
        # 点击出战
        mouse.click(1846, 590)
        # time.sleep(0.3)
        # 关闭
        mouse.click(1860, 169)


@cost_time
@set_lock
def execute_action():
    # 检查押送奖励，防止卡界面
    confirm_prisoner_award()

    global amount_fight, amount_rush, amount_tower, amount_secret_boss
    now_time = datetime.datetime.now()
    if in_fight_scene():
        print('战斗画面，跳过随机动作')
        return False
    # if soldier_lived():
    #     print('大刀侍卫已经复活，跳过随机动作')
    #     return False
    # print('\n', now_time)
    if in_city(click=False, out=True):
        print('在主城中，出城，执行随机动作')
    action = random_action()
    time.sleep(0.5)
    # print(action)
    one_more_time = 0
    if action == 'auto_fight':
        print('动作选中自动战斗，正在检测...')
        while not auto_fight():
            if one_more_time > 5:
                # 防止背包没有关闭卡界面，点击右上角关闭
                mouse.click(1860, 170)
                break
            print('%s动作执行未成功，再次尝试' % action)
            one_more_time += 1
            time.sleep(6)
        amount_fight += 1
    if action == 'endless_barrier':
        print('动作选中闯天关，正在检测...')
        while not endless_barrier():
            if one_more_time > 5:
                # 防止背包没有关闭卡界面，点击右上角关闭
                mouse.click(1860, 170)
                break
            print('%s动作执行未成功，再次尝试' % action)
            one_more_time += 1
            time.sleep(6)
        amount_rush += 1
    if action == 'monster_tower':
        print('动作选中锁妖塔，正在检测...')
        change_magic(weapon='天机晶石')
        time.sleep(2)
        while not monster_tower():
            if one_more_time >= 5:
                # 防止背包没有关闭卡界面，点击右上角关闭
                mouse.click(1860, 170)
                break
            print('%s动作执行未成功，再次尝试' % action)
            one_more_time += 1
            time.sleep(6)
        amount_tower += 1
        time.sleep(3)
        change_magic()
    if action == 'secret_boss':
        print('动作选中公会秘境BOSS，正在检测...')
        while not secret_boss():
            if one_more_time > 5:
                # 防止背包没有关闭卡界面，点击右上角关闭
                mouse.click(1860, 170)
                break
            print('%s动作执行未成功，再次尝试' % action)
            one_more_time += 1
            time.sleep(6)
        amount_secret_boss += 1

    print(
        '自动战斗次数：%s\t闯天关次数：%s\t锁妖塔次数：%s\t公会秘境BOSS次数：%s' % (amount_fight, amount_rush, amount_tower, amount_secret_boss))


def fight_result():
    """
    战斗结果检测
    :return:
    """
    sucess_position = (1552, 799, 1642, 824)
    sucess_filename = 'fight_sucess.bmp'
    x1, y1 = snapshot(sucess_position, sucess_filename)
    rgb_sucess = rgb_filter(sucess_filename, g_threshold=100, b_threshold=100)
    sucess_words = get_content_local(rgb_sucess)
    # print(sucess_words)
    if '领取奖励' in sucess_words:
        print('挑战成功，关闭')
        mouse.click(x1, y1)
        return True

    fail_position = (1546, 829, 1640, 856)
    fail_filename = 'fight_fail.bmp'
    x2, y2 = snapshot(fail_position, fail_filename)
    rgb_fail = rgb_filter(fail_filename, r_threshold=180, g_threshold=140)
    fail_words = get_content_local(rgb_fail)
    # print(fail_words)
    if '关闭面板' in fail_words or '领取奖励' in fail_words:
        print('挑战失败，关闭')
        mouse.click(x2, y2)
        return False
    return None


def receive_red_bag():
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    position = (1431, 657, 1792, 849)
    filename = 'temp_red_bag.bmp'
    new_filename = now + '_' + filename
    # 点击红包
    print('点击红包')
    mouse.click(1615, 762)
    snapshot(position, new_filename)
    time.sleep(5)
    # 点击空白
    mouse.click(1577, 939)
    time.sleep(1)
    mouse.click(1577, 939)
    # 点击红包
    print('关闭红包')


@cost_time
def secret_boss():
    if union_icon():
        time.sleep(0.5)
        print('攻击公会秘境BOSS')
        # 点击活动大厅
        mouse.click(1872, 602)
        time.sleep(0.5)
        # 点击'公会秘境'
        mouse.click(1750, 932)
        time.sleep(0.5)
        # 点击'挑战'
        mouse.click(1621, 831)
        time.sleep(3)
        num = 0
        while in_fight_scene():
            if num == 0:
                print('进入战斗界面')
            if fight_result() is False:
                break
            num += 1
            time.sleep(2)
        print('秘境BOSS挑战结束')
        return True
    return False


@cost_time
@set_lock
def union_boss():
    """
    攻击公会BOSS
    :return:
    """
    if union_icon():
        chat_log = 'chat.log'
        time.sleep(0.4)
        # 点击活动大厅
        print('进入活动大厅')
        mouse.click(1872, 602)
        time.sleep(0.4)
        # 点击'公会BOSS'选项卡
        print('点击公会BOSS')
        mouse.click(1638, 932)
        time.sleep(0.3)
        # 点击攻击
        print('尝试攻击公会BOSS')
        mouse.click(1806, 428)
        time.sleep(0.8)
        # 如果没有进入战斗画面，说明公会BOSS攻击失败
        if not in_fight_scene():
            time.sleep(0.3)
            # 点击关闭'公会任务'菜单
            print('关闭公会任务菜单')
            mouse.click(1852, 169)
            time.sleep(0.5)
            # 点击返回
            print('退出公会界面')
            mouse.click(1866, 932)
            content = '未能击杀公会BOSS'
            record_log(chat_log, content=content)
            print(content)
            return False
        content = '已经击杀公会BOSS'
        print(content)
        record_log(chat_log, content=content)
        return True
    else:
        print('公会图标不可用，跳过攻击公会BOSS')
        return False


def prisoner_empty():
    position = (1380, 506, 1816, 693)
    filename = 'temp_prisoner_background.bmp'
    snapshot(position, filename)
    result, similarity = compare_image('prisoner_background.bmp', filename, arg=0.93)
    print('空背景相似度%s' % similarity)
    if result:
        return True
    return False


def prisoner_cost(flush=False, independent=False):
    """
    押解囚徒押解次数，夺取次数统计
    :param flush:bool 是否强制刷新，强制刷新不读取文件，不强制刷新优先读取文件
    :param independent:bool 是否可以独立运行，点击商城
    :return:tuple (escort_num, rob_num)
    """
    # 当前年月日
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # 当天0:00的时间点 20xx-xx-xx 00:00:00
    base_time = datetime.datetime.strptime(now_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
    prisoner_cost_info_file = 'prisoner_cost.conf'
    prisoner_cost_info = file_operation(prisoner_cost_info_file)
    prisoner_date, escort_num, rob_num = prisoner_cost_info.split(',')
    # 文件里的时间转成datime对象
    prisoner_date_datetime = datetime.datetime.strptime(prisoner_date, '%Y-%m-%d %H:%M:%S')
    if flush is False:
        if prisoner_date_datetime > base_time:
            return escort_num, rob_num
    if independent:
        if game_method():
            time.sleep(1)
            # 点击押解囚徒
            mouse.click(1620, 408)
            time.sleep(1)
        else:
            return False
    position = (1483, 911, 1498, 960)
    filename = 'prisoner_cost.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, r_threshold=50)
    words = get_content_local(rgb_file, lang='legend_figure', psm=6)
    escort_num, rob_num = words.strip().split('\n')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = now + ',' + escort_num + ',' + rob_num
    file_operation(filename=prisoner_cost_info_file, operation='write', content=content)
    print('文件已经更新，押解次数:%s 掠夺次数:%s' % (escort_num, rob_num))

    if independent:
        print('关闭押解囚徒界面')
        # time.sleep(1)
        mouse.click(1861, 166)
    return escort_num, rob_num


def get_prisoner_info():
    # 押解归属人
    position = (1443, 432, 1551, 461)
    filename = 'prisoner_name.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, g_threshold=100)
    name = get_content_local(rgb_file).strip()

    # 战斗力
    capacity_position = (1523, 462, 1626, 487)
    capacity_filename = 'prisoner_capacity.bmp'
    snapshot(capacity_position, capacity_filename)
    capacity_file = rgb_filter(capacity_filename, g_threshold=60)

    capacity_words = get_content_local(capacity_file, lang='eng')
    print(capacity_words)
    capacity_list = re.split('[^\d]+', capacity_words)
    print(capacity_list)
    if len(capacity_list) != 0:
        try:
            capacity_num = float(capacity_list[0])
        except:
            capacity_num = None
    else:
        capacity_num = None
        # print('战斗力获取失败')

    # 劫镖奖励
    # 一级：    # 龙珠碎片30 成就令1 金币10万
    # 二级：    # 龙珠碎片60 成就令2 金币20万
    # 三级:     # 龙珠碎片100 成就令4 金币30万
    # 终极:     # 成就令6
    # awards_position = (1470, 587, 1540, 632)
    awards_position = (1495, 587, 1538, 606)
    awards_file = 'prisoner_awards.bmp'
    snapshot(awards_position, awards_file)
    rgb_awards_file = rgb_filter(awards_file, r_threshold=165, g_threshold=165, b_threshold=165)
    awards_words = get_content_local(rgb_awards_file, lang='eng')
    # print(awards_words)
    if awards_words == 'é':
        awards_words = '6'
    awards_num_result = re.match('\d+', awards_words)
    # print(awards_num_result)
    if awards_num_result:
        awards_num = int(awards_num_result.group())
    else:
        awards_num = None
        # print('奖励获取失败')
    # print('归属人:%s\t战斗力:%s\t奖励:%s' % (name, capacity_num, awards_num))
    awards_scope = [6, 30, 60, 100]
    if name and capacity_num and awards_num in awards_scope:
        print('归属人:%s\t战斗力:%s\t奖励:%s' % (name, capacity_num, awards_num))
        return name, capacity_num, awards_num
    elif name and capacity_num is None and awards_num in awards_scope:
        capacity_num = 999999
        print('归属人:%s\t战斗力:%s\t奖励:%s' % (name, capacity_num, awards_num))
        return name, capacity_num, awards_num
    else:
        return None


def prisoner_title():
    position = (1555, 144, 1683, 179)
    filename = 'prisoner_title.bmp'
    snapshot(position, filename)
    rgb_file = rgb_filter(filename, g_threshold=100)
    words = get_content_local(rgb_file)
    if '押解' in words:
        return True
    return False


# @cost_time
# @set_lock
def escort_prisoner(capacity_condition=4615):
    """
    抢夺押解囚徒
    :param capacity_condition: int 战斗力符合设置的值会抢夺
    :return:
    """
    white_lists = ['钱弘', '向山']
    escort_num, rob_num = prisoner_cost(independent=True)
    if rob_num == '0':
        print('押解囚徒:掠夺次数不足，跳过')
        return True
    time.sleep(1)
    if game_method():
        time.sleep(1)
        # 点击押解囚徒
        mouse.click(1620, 408)
        time.sleep(1)
        prisoner_cost(flush=True)
        time.sleep(1)
        if prisoner_empty():
            print('当前没有押镖囚徒，关闭界面')
            # 关闭
            time.sleep(1)
            mouse.click(1861, 166)
            return True
        y_position = 610
        during = False

        y_num = 0
        while during is False and y_position <= 780:
            x_num = 0
            y_num += 1
            x_position = 1865
            while during is False and x_position > 1400:
                x_num += 1
                print('尝试点击囚徒,横坐标:%4d 纵坐标:%4d,第%d行,第%d列' % (x_position, y_position, y_num, x_num))
                mouse.click(x_position, y_position)
                time.sleep(0.5)
                result = get_prisoner_info()
                if result:
                    name, capacity_num, awards_num = result
                    time.sleep(0.5)
                    if (
                                    awards_num == 100 or awards_num == 6) and 20 < capacity_num <= capacity_condition and name not in white_lists:
                        content = '符合抢夺条件，归属人:%s\t战斗力:%s\t奖励:%s' % (name, capacity_num, awards_num)
                        print('符合抢夺条件，点击抢夺')
                        during = True
                        # 点击抢夺
                        mouse.click(1610, 726)
                        record_log(filename=prisoner_log, content=content)
                        time.sleep(3)
                        while not prisoner_title():
                            print('正在抢夺囚徒')
                            time.sleep(2)
                        print('抢夺完毕')
                        time.sleep(2)
                        prisoner_cost(flush=True)
                        time.sleep(2)
                        # 关闭
                        mouse.click(1861, 166)

                    else:
                        print('不符合抢夺条件，关闭界面')
                        # 关闭提示界面
                        mouse.click(1888, 385)
                        time.sleep(0.5)

                x_position -= 85
                # time.sleep(0.5)
            y_position += 70

        if result is False:
            print('未找到囚徒，关闭')
        # 关闭
        time.sleep(1)
        mouse.click(1861, 166)
        return True
    return False


@cost_time
def receive_prisoner():
    """
    接收囚徒功能，用于押解囚徒
    :return:
    """
    escort_num, rob_num = prisoner_cost(independent=True)
    if escort_num == '0':
        print('押解囚徒:押解次数不足，跳过')
        return True
    time.sleep(1)
    if game_method():
        time.sleep(1)
        # 点击押解囚徒
        mouse.click(1620, 408)
        time.sleep(1)
        # 点击接取囚徒
        print('接取囚徒')
        mouse.click(1613, 938)
        time.sleep(1)
        # 点击开始押解
        content = '开始押解'
        print(content)
        mouse.click(1617, 864)
        time.sleep(1)
        # 点击确定
        mouse.click(1505, 604)
        time.sleep(2)
        # 记录日志
        record_log(filename=prisoner_log, content=content)
        time.sleep(2)
        # 刷新剩余次数
        prisoner_cost(flush=True)
        time.sleep(2)
        # 关闭
        print('关闭押解囚徒界面')
        mouse.click(1861, 166)


def mall_icon(click=True):
    """
    商城图标
    :return: 返回是否是'boss'图标,bool
    """

    position = (1589, 259, 1633, 290)
    filename = 'temp_mall.bmp'
    x, y = snapshot(position, filename)
    result, similarity = compare_image('mall.bmp', filename, arg=0.7)
    print('商城图标相似值 %s' % similarity)
    if result:
        if click:
            print('打开商城')
            mouse.click(x, y)
        return True
    return False


@cost_time
@set_lock
def purchase_by_coin():
    """
    购买金币商品
    :return:
    """
    # 确认是否有押解囚犯奖励，有则领取，防止挡界面
    confirm_prisoner_award()
    if mall_icon() is False:
        print('未获取到商城图标，退出')
        return False
    print('进入商城，检测金币销售商品')
    log_file = 'mall.log'
    time.sleep(1)
    money_ly = 502
    money_ry = 527
    purchase_y = 491
    goods_ly = 453
    goods_ry = 479
    money_head = 'money_'
    goods_head = 'goods_'
    for num in range(3):
        purchase_position = 1792, purchase_y
        money_position = (1506, money_ly, 1568, money_ry)
        goods_position = (1478, goods_ly, 1584, goods_ry)
        money_filename = money_head + str(num) + '.bmp'
        goods_filename = goods_head + str(num) + '.bmp'
        snapshot(money_position, money_filename)
        snapshot(goods_position, goods_filename)
        rgb_money = rgb_filter(money_filename, r_threshold=190, g_threshold=190, b_threshold=190)
        rgb_goods = rgb_filter(goods_filename, r_threshold=120)
        money_words = get_content_local(rgb_money).strip()
        print(money_words)
        goods_words = get_content_local(rgb_goods)
        result = re.match('(.+)?\d+([. ]\d+)?[万亿].*$', money_words)
        if result:
            content = '购买商品:%s\t价格:%s' % (goods_words, money_words)
            print(content)
            mouse.click(*purchase_position)
            copy_image(goods_filename, new_dir='mall')
            copy_image(rgb_goods, new_dir='mall')
            copy_image(money_filename, new_dir='mall')
            copy_image(rgb_money, new_dir='mall')
            record_log(filename=log_file, content=content)
            queue_jobs_list.insert(0, 'purchase_by_coin')
        money_ly += 107
        money_ry += 107
        goods_ly += 107
        goods_ry += 107
        purchase_y += 107
        time.sleep(1)
    # 关闭商城
    print('检测完毕，退出商城')
    mouse.click(1867, 188)
    return True


def rennewingboss_control():
    """
    转生boss任务控制
    :return:
    """
    jid = 'renewing_boss'
    accurate_time = '20:59:57'
    now_date = datetime.datetime.now().strftime('%Y-%m-%d ')
    job = scheduler.get_job(job_id=jid)
    if job:
        job.modify(next_run_time=now_date + accurate_time)
        print('%25s 任务已经更新:%s' % (jid, scheduler.get_job(job_id=jid)))
    else:
        # 转生boss 每天晚上21点执行
        scheduler.add_job(eval(jid), next_run_time=now_date + accurate_time, coalesce=True, misfire_grace_time=600,
                          id=jid)
        print('%25s 任务已经添加:%s' % (jid, scheduler.get_job(job_id=jid)))


def tempboss_control():
    """
    元旦boss任务控制
    :return:
    """
    jid1 = 'temp_boss1'
    jid2 = 'temp_boss2'
    accurate_time1 = '13:00:01'
    accurate_time2 = '19:00:01'
    now_date = datetime.datetime.now().strftime('%Y-%m-%d ')
    job1 = scheduler.get_job(job_id=jid1)
    job2 = scheduler.get_job(job_id=jid2)
    if job1:
        job1.modify(next_run_time=now_date + accurate_time1)
        job2.modify(next_run_time=now_date + accurate_time2)
        print('%25s 任务已经更新:%s' % (jid1, scheduler.get_job(job_id=jid1)))
        print('%25s 任务已经更新:%s' % (jid2, scheduler.get_job(job_id=jid2)))
    else:
        # tempboss 每天晚上19点执行
        scheduler.add_job(eval('temp_boss'), next_run_time=now_date + accurate_time1, coalesce=True,

                          id=jid1)
        scheduler.add_job(eval('temp_boss'), next_run_time=now_date + accurate_time2, coalesce=True,

                          id=jid2)
        print('%25s 任务已经添加:%s' % (jid1, scheduler.get_job(job_id=jid1)))
        print('%25s 任务已经添加:%s' % (jid2, scheduler.get_job(job_id=jid2)))


def scheduler_everyday_task():
    """
    每日0点整，固定时间点任务日期部分更新，例：2019-01-01
    :return:
    """
    now = datetime.datetime.now()
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_time = datetime.datetime.strptime(now_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
    end_time = start_time + datetime.timedelta(minutes=1)

    jobs_list = [
        # 转生BOSS任务控制器更新器
        'rennewingboss_control',
        # 个人BOSS任务控制器更新
        'personal_boss_control',
        # # 元旦
        # 'tempboss_control'
    ]

    for job_id in jobs_list:
        # 时间如果不在0:00:00-0:01内，立即执行任务
        if not start_time < now < end_time:
            exec(job_id + '()')
        # 将列表中的任务创建在0:00分执行的任务，未执行补偿时间24小时
        scheduler.add_job(eval(job_id), 'cron', coalesce=True, misfire_grace_time=86400, hour='0', minute='0',
                          id=job_id)
        print('%25s 任务生成器已经创建:%s' % (job_id, scheduler.get_job(job_id=job_id)))


def scheduler_protect_bice():
    """
    守卫比奇任务调度，周1、3、5 20:30 - 20:45
    :return:
    """
    scheduler.add_job(protect_bice, 'cron', hour='20', minute='30', day_of_week='mon,wed,fri', coalesce=True,
                      misfire_grace_time=900, id='protect_bice')
    print('%25s 任务已经添加:%s' % ('protect_bice', scheduler.get_job(job_id='protect_bice')))


def scheduler_night_fight_bice():
    """
    比奇夜战任务调度，周2、4、6 20:30 - 20:45
    :return:
    """
    scheduler.add_job(night_fight_bice, 'cron', hour='20', minute='30', day_of_week='tue,thu,sat', coalesce=True,
                      misfire_grace_time=900, id='night_fight_bice')
    print('%25s 任务已经添加:%s' % ('night_fight_bice', scheduler.get_job(job_id='night_fight_bice')))


def scheduler_multi_pvp():
    """
    通天战场任务调度，周2、4、6 19:30 - 19:46
    :return:
    """
    scheduler.add_job(multi_pvp, 'cron', hour='19', minute='30', day_of_week='tue,thu,sat', coalesce=True,
                      misfire_grace_time=900, id='multi_pvp')
    print('%25s 任务已经添加:%s' % ('multi_pvp', scheduler.get_job(job_id='multi_pvp')))


def scheduler_global_rob():
    """
    跨服镖车，每天早上11点第一场
    :return:
    """

    # 跨服镖车，每天早上11点第一场
    scheduler.add_job(global_rob, 'cron', hour='11', minute='0', day_of_week='mon-sat', coalesce=True,
                      misfire_grace_time=3600,
                      id='global_rob')
    print('%25s 任务已经添加:%s' % ('global_rob', scheduler.get_job(job_id='global_rob')))


def personal_boss_control():
    """
    个人boss任务控制
    :return:
    """
    global queue_jobs_list
    jid = 'personal_boss'
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d ')
    start_time = datetime.datetime.strptime(now_date + ' 00:00:30', '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(now_date + ' 00:20:00', '%Y-%m-%d %H:%M:%S')
    # 如果当前时间在开始与结束时间内，则添加任务
    if start_time <= now <= end_time:
        for num in range(20):
            queue_jobs_list.insert(0, jid)
            if num % 5 == 0:
                queue_jobs_list.insert(0, 'clean_bag')
        print('已插入个人BOSS任务')
    else:
        # print('已过时段，个人BOSS任务未添加')
        pass


def soldier_control():
    """
    大刀侍卫计划任务控制
    :return:
    """
    # 获取大刀侍卫复活时间
    deny_second = datetime.timedelta(seconds=3)
    resurgence_time = soldier_resurgence_time() + deny_second
    if resurgence_time:
        # 如果时间存在，将格式化的时间作为任务开始时间
        start_time = resurgence_time.strftime('%Y-%m-%d %H:%M:%S')
        job = scheduler.get_job('kill_soldier')
        if not job:
            # 检查当前任务中是否存在kill_soldier 任务，如果没有则添加指定时间攻击大刀侍卫的任务
            scheduler.add_job(kill_soldier, coalesce=True, misfire_grace_time=36000, next_run_time=start_time,
                              id='kill_soldier')
        else:
            # 如果已经有任务，则更新定时任务
            print('更新大刀侍卫自动攻击任务', scheduler.get_job('kill_soldier'))
            job.modify(next_run_time=start_time)

    else:
        # 如果时间不存在，添加立即攻击大刀侍卫的任务
        scheduler.add_job(kill_soldier, next_run_time=datetime.datetime.now(), coalesce=True, misfire_grace_time=36000,
                          id='kill_soldier')
        # kill_soldier()


def scheduler_soldier():
    """
    大刀侍卫控制器调度
    :return:
    """
    soldier_control()
    scheduler.add_job(soldier_control, 'cron', hour='*/1')
    print('%25s 任务已经添加:%s' % ('soldier_control', scheduler.get_job(job_id='kill_soldier')))


@cost_time
@set_lock
def red_bag():
    """
    抢红包
    :return:
    """
    if union_icon():
        time.sleep(0.6)
        # 点击仓库
        print('点击仓库')
        mouse.click(1674, 821)
        time.sleep(0.6)
        # 点击'红包'选项卡
        print('点击红包选项卡')
        mouse.click(1519, 933)
        time.sleep(0.6)
        # 点击抢红包
        print('抢红包')
        # mouse.click(1617, 685)
        time.sleep(1)
        # 点击关闭仓库
        print('关闭仓库')
        mouse.click(1857, 167)
        time.sleep(0.6)
        # 点击关闭公会
        print('关闭公会界面')
        mouse.click(1867, 896)

        # 点击确认领取
        mouse.click(1493, 604)

        return True
    return False


def temp_boss():
    """
    春节临时BOSS
    :return:
    """
    # 点击贺新春
    mouse.click(1696, 273)
    time.sleep(0.5)
    # 点击金猪送福
    mouse.click(1796, 254)
    time.sleep(0.5)
    # 点击前往作战
    mouse.click(1619, 928)


def in_key_periods(lead_time=10):
    """
    检查当前时间是否在关键时间内
    :param lead_time: int 提前几分钟
    :return: bool 如果在关键时间内返回True,否则返回False
    """
    global queue_jobs_list
    now = datetime.datetime.now()
    sunday = False
    if now.strftime('%w') in '0':
        sunday = True

    periods = []
    # 石墓阵、通天战场
    key_time1 = ['19:30:00', '19:50:00']
    # 守卫比奇、夜战比奇
    key_time2 = ['20:30:00', '20:45:00']
    # 转生BOSS & 跨服镖车第三场
    key_time3 = ['21:00:00', '21:10:00']
    # 每天刷新后个人BOSS等
    key_time4 = ['00:00:00', '00:10:00']
    # 跨服押镖 第一场
    key_time5 = ['11:00:00', '11:20:00']
    # key_time6 = ['18:00:00', '18:30:00']


    # 临时，主城宝箱
    key_time7 = ['12:00:00', '12:35:00']
    # 临时、主城宝箱
    key_time8 = ['17:50:00', '18:35:00']
    # 临时、沙城
    # key_time9 = ['19:50:00', '21:15:00']

    # 每天都生效的关键时间点加入此处
    # 转生BOSS & 跨服镖车第三场
    periods.append(key_time3)
    # 每天刷新后个人BOSS等
    # periods.append(key_time4)
    # periods.append(key_time7)
    # periods.append(key_time8)
    # periods.append(key_time9)

    # 非星期日的关键时间点，加入此处
    if not sunday:
        # 石墓阵、通天战场
        periods.append(key_time1)
        # 守卫比奇、夜战比奇
        periods.append(key_time2)
        # 跨服押镖 第一场
        periods.append(key_time5)
        # periods.append(key_time6)

    key_date = now.strftime('%Y-%m-%d')

    for period in periods:
        key_start_str = key_date + ' ' + period[0]
        key_end_str = key_date + ' ' + period[1]

        minutes_earlier = datetime.timedelta(minutes=lead_time)
        key_start = datetime.datetime.strptime(key_start_str, '%Y-%m-%d %H:%M:%S') - minutes_earlier
        key_end = datetime.datetime.strptime(key_end_str, '%Y-%m-%d %H:%M:%S')
        if key_start < now < key_end:
            if now == key_start + datetime.timedelta(seconds=5) or now == key_end - datetime.timedelta(seconds=5):
                print('开始:%s ----> 当前:%s ----> 结束:%s' % (
                    key_start.strftime('%H:%M:%S'), now.strftime('%H:%M:%S'), key_end.strftime('%H:%M:%S')))
            queue_jobs_list = []
            return True
    return False


def queue_jobs_list_add(job_name, insert_job=False):
    """
    向queue_jobs_list中添加任务
    :param job_name: str 任务名称
    :param  insert_job: bool True 插入任务，Fasle 追加任务
    :return:
    """
    global queue_jobs_list
    # 如果队列长度超过20，并且新任务已经在队列中，则跳过
    queue_lenth = len(queue_jobs_list)
    if queue_lenth >= 25 and job_name in queue_jobs_list:
        print('当前任务队列长度:%3d ,已经超过20，放弃添加任务:%s' % (queue_lenth, job_name))
        # check_offline()
        job_id = 'execute_jobs'
        job = scheduler.get_job(job_id=job_id)
        if job.next_run_time is None:
            job.resume()
        if queue_lenth >= 40:
            queue_jobs_list = []

    else:
        if insert_job:
            queue_jobs_list.insert(0, job_name)
            print('%25s 任务已插入至列表头部，当前队列长度:%3d' % (job_name, queue_lenth))
        else:
            queue_jobs_list.append(job_name)
            print('%25s 任务已追加至列表尾部，当前队列长度:%3d' % (job_name, queue_lenth))


def execute_jobs():
    """
    消费队列中的任务
    :return:
    """
    global queue_jobs_list
    if len(queue_jobs_list) != 0:
        # 执行任务本身
        job_id = 'execute_jobs'
        execute_self = scheduler.get_job(job_id=job_id)
        if execute_lock == 'common' and execute_self:
            execute_self.pause()
        job = queue_jobs_list.pop(0)
        print('执行任务:%s，当前队列长度:%d，下5个任务为：%s' % (job, len(queue_jobs_list), queue_jobs_list[0:5]))
        try:
            exec(job + '()')
        except Exception as e:
            print(e)
        if len(queue_jobs_list) != 0:
            print('即将执行任务：%s' % queue_jobs_list[0])

        if execute_lock == 'common' and execute_self:
            execute_self.resume()
            if len(queue_jobs_list) >= 2 and queue_jobs_list[0] == job:
                scheduler.modify_job(job_id=job_id, next_run_time=datetime.datetime.now())
    else:
        print('当前队列为空，任务已经全部消费')


def execute_jobs_control():
    global execute_lock
    global queue_jobs_list
    advance_time = 10
    job_id = 'execute_jobs'
    job = scheduler.get_job(job_id=job_id)
    # 如果当前在大刀侍卫复活前n分钟内或者关键点时间内
    if pass_soldier_lead_time(advance_time) or in_key_periods(advance_time):
        # 任务存在并且下次运行时间不是空，则暂停任务
        if job and job.next_run_time is not None:
            job.pause()
            queue_jobs_list = []
            execute_lock = 'key'
            print('目前处于大刀侍卫复活或关键点前%d分钟，暂停%s任务' % (advance_time, job_id))

        else:
            print('目前处于大刀侍卫复活或关键点时期，%s任务已经暂停' % job_id)
    else:
        # 如果当前不在大刀侍卫复活前n分钟内，则恢复或增加任务
        if job:
            # 任务存在，但下次运行时间是空的，说明被暂停，
            if job.next_run_time is None:
                # 如果执行锁关键字是key 则恢复任务
                if execute_lock == 'key':
                    print('不在侍卫复活期或关键点时期，恢复%s任务' % job_id)
                    job.resume()
                    execute_lock = 'common'
        else:
            # 任务不存在，则添加任务
            scheduler.add_job(execute_jobs, trigger='cron', second='*/8', next_run_time=datetime.datetime.now(),
                              coalesce=True, misfire_grace_time=15, id=job_id)


def loop_jobs():
    jobs_list = {
        # 公会消息
        # 'union_message_monitor': [{'second': '*/4'}, 10],
        # 公会BOSS监控
        # 'union_boss_monitor': [{'second': '*/7'}, 10],
        # 检查是否离线
        'check_offline': [{'minute': '*/15'}, 10],
        # 检查背包是否满
        'check_bag_full': [{'minute': '*/15'}, 10],
    }
    # 任务白名单，关键时间点与大刀侍卫复活时也自动执行
    job_white_list = ['check_offline']
    for job_id, kwargs in jobs_list.items():
        job = scheduler.get_job(job_id=job_id)
        # 如果当前在大刀侍卫复活前n分钟内或者关键点时间内
        if pass_soldier_lead_time(kwargs[1]) or in_key_periods(kwargs[1]):
            # 任务存在并且下次运行时间不是空，则暂停任务
            if job and job.next_run_time is not None and job not in job_white_list:
                job.pause()
                print('目前处于大刀侍卫复活或关键点前%d分钟，暂停%s任务' % (kwargs[1], job_id))

            else:
                print('目前处于大刀侍卫复活或关键点时期，%s任务已经暂停' % job_id)
        else:
            # 如果当前不在大刀侍卫复活前n分钟内，则恢复或增加任务
            if job:
                # 任务存在，但下次运行时间是空的，说明被暂停，则恢复任务
                if job.next_run_time is None:
                    print('不在侍卫复活期或关键点时期，恢复%s任务' % job_id)
                    job.resume()
            else:
                # 任务不存在，则添加任务
                scheduler.add_job(eval(job_id), trigger='cron', coalesce=True, misfire_grace_time=1,
                                  **kwargs[0], next_run_time=datetime.datetime.now(), id=job_id)
                print('%25s 任务生成器已经创建:%s' % (job_id, scheduler.get_job(job_id=job_id)))


def scheduler_execute_jobs():
    """
    任务列表调度
    :return:
    """
    # 常规循环任务
    # jobs_creater()
    scheduler.add_job(jobs_creater, 'cron', minute='*/2', next_run_time=datetime.datetime.now())
    # 监控类循环任务
    # loop_jobs()
    scheduler.add_job(loop_jobs, 'cron', minute='*/2', next_run_time=datetime.datetime.now())

    # 消费任务
    # execute_jobs_control()
    scheduler.add_job(execute_jobs_control, 'cron', minute='*/2', next_run_time=datetime.datetime.now())


def jobs_creater():
    """
    任务生成器
    :return:
    """
    jobs_list = {

        # 全民/神域BOSS任务
        'auto_boss': [{'second': '*/40'}, 10],
        # 随机动作任务
        # 'execute_action': [{'minute': '*/3'}, 10],
        # 自动挑战关卡
        'auto_fight': [{'minute': '*/1'}, 10],
        # 闯天关
        'endless_barrier': [{'minute': '*/5'}, 10],
        # 清理背包任务
        'clean_bag': [{'minute': '*/4'}, 10],
        # 锁妖塔
        'monster_tower': [{'minute': '*/40'}, 10],
        # 公会秘境BOSS
        # 'secret_boss': [{'minute': '*/1'}, 10],
        # 野外boss任务
        'lucky_boss': [{'minute': '*/5'}, 5],
        # 自动野战任务
        # 'auto_pk': [{'hour': '0-22', 'minute': '*/5'}, 10],
        'auto_pk': [{'minute': '*/5'}, 10],

        # 抢劫囚徒
        'escort_prisoner': [{'minute': '*/15'}, 10],
        # 购买金币商品
        'purchase_by_coin': [{'minute': '*/20'}, 10],
        # 检查掉线状态
        # 'check_offline': [{'minute': '*/6'}, 10],
        # 抢红包
        'red_bag': [{'minute': '*/10'}, 10],
        # 天梯挑战
        'ladder_fight': [{'minute': '*/45'}, 10],
        # 押解囚徒，每天4:00
        'receive_prisoner': [{'hour': '4', 'minute': '50'}, 10],
        # 春节红包
        # 'receive_red_bag': [{'hour': '12,18', 'minute': '1'}, 10],
    }
    # 抢劫囚徒次数为零，则不添加public_message  escort_prisoner
    escort_num, rob_num = prisoner_cost(independent=True)
    if rob_num == '0':
        print('抢夺次数不足,放弃添加任务:escort_prisoner')
        del jobs_list['escort_prisoner']
        escort_job = scheduler.get_job(job_id='escort_prisoner')
        if escort_job:
            print('已经清除任务:escort_prisoner')
            escort_job.remove()
    # 是否大刀侍卫复活前10分钟
    pre_soldier_lived = pass_soldier_lead_time(10)

    for job_id, kwargs in jobs_list.items():
        job = scheduler.get_job(job_id=job_id)
        # 如果当前在大刀侍卫复活前n分钟内或者关键点时间内
        if pre_soldier_lived or in_key_periods(kwargs[1]):
            # 掉线检查任务不暂停，跳过
            if job_id == 'check_offline':
                continue
            # 任务存在并且下次运行时间不是空，则暂停任务
            if job and job.next_run_time is not None:
                job.pause()
                print('目前处于大刀侍卫复活或关键点前%d分钟，暂停%s任务' % (kwargs[1], job_id))
            else:
                print('%s任务已经暂停' % job_id)
        else:
            # 如果当前不在大刀侍卫复活前n分钟内，则恢复或增加任务
            if job:
                # 任务存在，但下次运行时间是空的，说明被暂停，则恢复任务
                if job.next_run_time is None:
                    print('不在侍卫复活期或关键点时期，恢复%s任务' % job_id)
                    job.resume()
            else:
                # 任务不存在，添加任务，但不立即执行，跳过的任务列表:检查掉线状态、押解囚徒、野战PK、春节红包
                skip_immediately = ['check_offline', 'receive_prisoner', 'auto_pk', 'receive_red_bag']
                # 需要插入的任务列表
                insert_jobs_list = ['receive_red_bag', 'receive_prisoner', 'auto_pk']
                # 在插入任务列表中的任务，标志变量设置为True,否则为False
                if job_id in insert_jobs_list:
                    insert_job = True
                else:
                    insert_job = False
                if job_id in skip_immediately:
                    scheduler.add_job(queue_jobs_list_add, args=(job_id, insert_job), trigger='cron', coalesce=True,
                                      misfire_grace_time=1, **kwargs[0], id=job_id)
                else:
                    # 任务不存在，添加任务，并立即执行一次
                    scheduler.add_job(queue_jobs_list_add, args=(job_id, insert_job), trigger='cron', coalesce=True,
                                      misfire_grace_time=1,
                                      **kwargs[0], next_run_time=datetime.datetime.now(), id=job_id)
                print('%25s 任务生成器已经创建:%s' % (job_id, scheduler.get_job(job_id=job_id)))


def update_icon(src_file, dst_file):
    src_result = os.path.isfile(imgs_dir + src_file)
    dst_result = os.path.isfile(imgs_dir + dst_file)
    if src_result and dst_result:
        result, similarity = compare_image(src_file, dst_file)
        if similarity < 1:
            os.remove(imgs_dir + dst_file)
            os.rename(imgs_dir + src_file, imgs_dir + dst_file)
            print('图标文件已经更新\n')
        else:
            print('图标文件相似值为1，无需更新\n')


def check_icon():
    if mall_icon():
        src_file = 'temp_mall.bmp'
        dst_file = 'mall.bmp'
        time.sleep(2)
        mouse.click(1867, 187)
        print('关闭商城')
        update_icon(src_file, dst_file)
    time.sleep(2)

    if pk_icon():
        src_file = 'temp_pk.bmp'
        dst_file = 'pk.bmp'
        time.sleep(2)
        mouse.click(1859, 167)
        print('关闭野战菜单')
        update_icon(src_file, dst_file)
    time.sleep(2)

    if practice_icon():
        src_file = 'temp_practice.bmp'
        dst_file = 'practice.bmp'
        time.sleep(2)
        mouse.click(1845, 795)
        print('关闭修炼菜单')
        update_icon(src_file, dst_file)
    time.sleep(2)

    if boss_icon():
        src_file = 'temp_boss.bmp'
        dst_file = 'boss.bmp'
        time.sleep(2)
        mouse.click(1859, 167)
        print('关闭BOSS菜单')
        update_icon(src_file, dst_file)
    time.sleep(2)

    if game_method():
        src_file = 'temp_game_method.bmp'
        dst_file = 'game_method.bmp'
        time.sleep(2)
        mouse.click(1859, 167)
        print('关闭玩法菜单')
        update_icon(src_file, dst_file)
    time.sleep(2)

    if union_icon():
        src_file = 'temp_union_icon.bmp'
        dst_file = 'union_icon.bmp'
        time.sleep(2)
        mouse.click(1866, 897)
        print('关闭公会菜单')
        update_icon(src_file, dst_file)
    time.sleep(2)

    print('图标文件已经全部检查完毕')
    return True


def repeat_execute(job):
    """
    重复执行某任务
    :param job: str 任务名称
    :return:
    """
    result = eval(job + '()')

    num = 1
    while result:
        time.sleep(1)
        if num % 15 == 0:
            result = eval('auto_pk()')
        else:
            result = eval(job + '()')
        num += 1


def scheduler_list():
    """
    总任务列表
    :return:
    """
    # 每天定点任务更新，包括转生BOSS、个人BOSS
    scheduler_everyday_task()

    # 大刀侍卫
    scheduler_soldier()
    # 守护比奇活动
    scheduler_protect_bice()
    # 比奇夜战活动
    scheduler_night_fight_bice()
    # 通天战场活动
    scheduler_multi_pvp()

    # 跨服押镖 早上第一场
    scheduler_global_rob()

    # 包含以下任务:自动战斗、闯天关、锁妖塔、清理背包、野外boss、全民/神域BOSS、红包、公会秘境BOSS、押解囚徒
    scheduler_execute_jobs()


if __name__ == '__main__':
    # 定位并重新设置窗口
    reset_window()
    # 获取计划表对象
    scheduler = BlockingScheduler()
    # scheduler = BackgroundScheduler()
    # 刷新图标文件
    # check_icon()
    # repeat_execute('endless_barrier')
    # repeat_execute('auto_fight')
    # repeat_execute('secret_boss')
    # 任务集合
    scheduler_list()
    # secret_boss()
    # monster_tower()
    # confirm_prisoner_award()
    # lucky_boss()
    # in_city()
    # auto_fight()
    # in_fight_scene()
    # union_boss()
    # union_boss_str()
    # night_fight_bice()
    # global_rob()
    # lucky_boss()
    # check_bag_full()
    # competitor_inspection_time()

    # num = 0
    # while True:
    #     if num %2 ==0:
    #         mouse.click(1613,584)
    #     else:
    #         mouse.click(1611,644)
    #     num +=1
    #     time.sleep(1)
    # purchase_by_coin()
    # multi_pvp()

    # rob_list()
    # auto_pk()
    # secret_boss()
    # in_city(report=True)
    # union_boss_monitor()
    # check_offline()
    # get_prisoner_info()
    # kill_soldier()
    # print(soldier_resurgence_time())
    # purchase_by_coin()
    # receive_prisoner()
    # escort_prisoner()
    # get_prisoner_info()
    # in_city()
    # red_bag()
    # ladder_fight()
    # union_boss()
    # get_red_name_values()
    # print(get_red_name_values())

    # escort_prisoner()
    # get_prisoner_info()
    # auto_boss()
    # auto_pk()
    # auto_fight()
    # check_offline()
    # change_magic(weapon='灵宝护符')
    # change_magic('天机晶石')
    # change_magic(weapon='魂玉金玲')
    # night_fight_bice()

    scheduler.start()
