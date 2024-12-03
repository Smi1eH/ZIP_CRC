import zipfile
import argparse
import string
import binascii
import os, sys

def title():
    print("""  ______                   _     __             ____  ____    
.' ____ \                 (_)   /  |           |_   ||   _|   
| (___ \_|  _ .--..--.    __    `| |    .---.    | |__| |     
 _.____`.  [ `.-. .-. |  [  |    | |   / /__\\\\    |  __  |     
| \____) |  | | | | | |   | |   _| |_  | \__., _| |  | |_    
 \______.' [___||__||__] [___] |_____|  '.__.' |____||____|         
                                            python CRC32-Tools.py -h
                                     https://github.com/Smi1eH/ZIP_CRC\n""")


def FileRead(zipname):
    try:
        f =open(zipname)                               # 打开目标文件
        f.close()
    except FileNotFoundError:
        print ("未找到同目录下的压缩包文件" + zipname) # 如果未找到文件，输出错误
        return                                         # 退出线程，进行详细报错
    except PermissionError:
        print ("无法读取目标压缩包（无权限访问）")     # 如果发现目标文件无权限，输出错误
        return


# 获取zip中的文件Crc值
def ReadCrc(zipname):
    zip_url = "./" + zipname
    file_zip = zipfile.ZipFile(zip_url)    # 用zipfile读取指定的压缩包文件
    name_list = file_zip.namelist()        # 使用一个列表，获取并存储压缩包内所有的文件名
    crc_list = []
    crc32_list = []
    print('+--------------遍历指定压缩包的CRC值----------------+')
    for name in name_list:
        name_message = file_zip.getinfo(name)
        crc_list.append(name_message.CRC)
        crc32_list.append(hex(name_message.CRC))
        print('[+] {0}: {1}'.format(name,hex(name_message.CRC)))
    print('+-------------对输出的CRC值进行碰撞-----------------+')
    return crc_list, crc32_list


def OneByte(zipname):
    crc_list,crc32_list = ReadCrc(zipname)
    comment = ''
    chars = string.printable
    for crc_value in crc_list:
        for char1 in chars:
            thicken_crc = binascii.crc32(char1.encode())
            calc_crc = thicken_crc & 0xffffffff
            if calc_crc == crc_value:
                print('[Success] {}: {}'.format(hex(crc_value),char1))
                comment += char1
    print('+-----------------CRC碰撞结束！！！-----------------+')
    crc32_list = str(crc32_list)
    crc32_list = crc32_list.replace('\'' , '')
    print("读取成功，导出CRC列表为：" + crc32_list)
    if comment:
        print('CRC碰撞成功，结果为: {}'.format(comment))
    else:
        print('CRC碰撞没有结果，请检查压缩包内文件是否为1Byte！！！')

def TwoByte(zipname):
    crc_list, crc32_list = ReadCrc(zipname)
    comment = ''
    chars = string.printable
    for crc_value in crc_list:
        for char1 in chars:
            for char2 in chars:
                res_char = char1 + char2
                thicken_crc = binascii.crc32(res_char.encode())
                calc_crc = thicken_crc & 0xffffffff
                if calc_crc == crc_value:
                    print('[Success] {}: {}'.format(hex(crc_value),res_char))
                    comment += res_char
    print('+-----------------CRC碰撞结束！！！-----------------+')
    crc32_list = str(crc32_list)
    crc32_list = crc32_list.replace('\'' , '')
    print("读取成功，导出CRC列表为：" + crc32_list)
    if comment:
        print('CRC碰撞成功，结果为: {}'.format(comment))
    else:
        print('CRC碰撞没有结果，请检查压缩包内文件是否为2Byte！！！')

def ThreeByte(zipname):
    crc_list, crc32_list = ReadCrc(zipname)
    comment = ''
    chars = string.printable
    result_dict={}
    for char1 in chars:
        for char2 in chars:
            for char3 in chars:
                res_char = char1 + char2 + char3
                thicken_crc = binascii.crc32(res_char.encode())
                calc_crc = thicken_crc & 0xffffffff
                for crc_value in crc_list:
                    if calc_crc == crc_value:
                        index = crc32_list.index(hex(crc_value))
                        num = int(index)
                        new_data = {num : res_char}
                        print('[Success] 第 {} 个文件 {}: {}'.format(num,hex(crc_value),res_char))
                        result_dict.update(new_data)
                        break
    sorted_items = sorted(result_dict.items())
    for key, res_char in sorted_items:
        comment += res_char
    print('+-----------------CRC碰撞结束！！！-----------------+')
    crc32_list = str(crc32_list)
    crc32_list = crc32_list.replace('\'' , '')
    print("读取成功，导出CRC列表为：" + crc32_list)
    if comment:
        print('CRC碰撞成功，结果为: {}'.format(comment))
    else:
        print('CRC碰撞没有结果，请检查压缩包内文件是否为3Byte！！！')

def FourByte(zipname):
    crc_list, crc32_list = ReadCrc(zipname)
    comment = ''
    chars = string.printable
    result_dict={}
    for char1 in chars:
        for char2 in chars:
            for char3 in chars:
                for char4 in chars:
                    res_char = char1 + char2 + char3 + char4        # 获取任意4Byte字符
                    thicken_crc = binascii.crc32(res_char.encode()) # 获取任意4Byte字符串的CRC32值
                    calc_crc = thicken_crc & 0xffffffff             # 将任意4Byte字符串的CRC32值与0xffffffff进行与运算
                    for crc_value in crc_list:
                        if calc_crc == crc_value:                       # 匹配两个CRC32值
                            index = crc32_list.index(hex(crc_value))
                            num = int(index)
                            new_data = {num : res_char}
                            print('[Success] 第 {} 个文件 {}: {}'.format(num,hex(crc_value),res_char))
                            result_dict.update(new_data)
                            break
    sorted_items = sorted(result_dict.items())
    for key, res_char in sorted_items:
        comment += res_char
    print('+-----------------CRC碰撞结束！！！-----------------+')
    crc32_list = str(crc32_list)
    crc32_list = crc32_list.replace('\'' , '')
    print("读取成功，导出CRC列表为：" + crc32_list)                     # 导出CRC列表
    if comment:
        print('CRC碰撞成功，结果为: {}'.format(comment))                  # 输出CRC碰撞结果
    else:
        print('CRC碰撞没有结果，请检查压缩包内文件是否为4Byte！！！')

def CrackCrc(crc):
    for i in dic:
        for j in dic:
            for k in dic:
                for h in dic:
                    s = i + j + k + h
                    if crc == (binascii.crc32(s.encode())):
                        f.write(s)
                        return

def CrackZip():
    str_head = input("[+]输入规律字符串\n>>>")
    num = int(input("[+]输入需要重复次数\n>>>"))
    print("+-------------正在碰撞破解请耐心等待！！！-------------+")
    for i in range(0,num):
        file = str_head+str(i)+'.zip'
        crc = zipfile.ZipFile(file,'r').getinfo('data.txt').CRC
        CrackCrc(crc)

if __name__ == '__main__':
    title()
    parser = argparse.ArgumentParser(description="python CRC32-Tools.py -h")
    parser.add_argument('-m', action='store', dest='morezip', help='读取全部压缩包，输出每个压缩包CRC值列表，不需要加文件名')
    parser.add_argument('-1', action='store', dest='onebyte', help='对1Byte的压缩包自动进行CRC碰撞并输出文件内容')
    parser.add_argument('-2', action='store', dest='twobyte', help='对2Byte的压缩包自动进行CRC碰撞并输出文件内容')
    parser.add_argument('-3', action='store', dest='threebyte', help='对3Byte的压缩包自动进行CRC碰撞并输出文件内容')
    parser.add_argument('-4', action='store', dest='fourbyte', help='对4Byte的压缩包自动进行CRC碰撞并输出文件内容')
    args = parser.parse_args()
    try:
        if args.morezip:
            dic = string.ascii_letters + string.digits + '+/=' # 包含所有ASCII字母（a-z, A-Z）、数字（0-9）以及字符 '+', '/', '=' 的字符串。
            try:
                with open('out.txt','w') as f:
                    CrackZip()

                parent_directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                print(f"[+]碰撞结果文件成功写入，写入位置为:{parent_directory_path}\\out.txt")
                print('+-----------------CRC碰撞结束！！！-----------------+')
            except Exception as e:
                print(f"文件并没有被写入，发生错误为：{e}")
                print('+-----------------CRC碰撞结束！！！-----------------+')
        if args.onebyte:
            FileRead(args.onebyte)
            OneByte(args.onebyte)
        if args.twobyte:
            FileRead(args.twobyte)
            TwoByte(args.twobyte)
        if args.threebyte:
            FileRead(args.threebyte)
            ThreeByte(args.threebyte)
        if args.fourbyte:
            FileRead(args.fourbyte)
            FourByte(args.fourbyte)
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except BaseException as e:
        err = str(e)
        print('脚本详细报错：' + err)
        sys.exit(0)
