import serial,time

############## 事件函数-串口操作函数

# 尝试开启串口
def tryOpenSerial(com,baund=460800,parity='N',stopbits=1,maxReryCount=3,delay=0.5):
    debug_list = []
    serials = False
    emsg = ''
    for i in range(maxReryCount):
        try:serials = serial.Serial(com, baund,parity=parity,stopbits=stopbits);break
        except Exception as e:time.sleep(delay);emsg = e 
    if not serials:
        debug_list.append(emsg)
        debug_list.append('{} in {}?'.format(com,list(serial.tools.list_ports.comports())))
    return serials,debug_list
# 尝试发送数据
# 废弃
def trySendSerial( serials,delay:float=0.5,msgList:list = [],msgType='hex' ):
    debug_list = []
    pass
# 尝试打开串口并发送数据
def tryOpenAndSend(com,baund=460800,parity='N',stopbits=1,maxReryCount=3,delay=0.1,msgList=[],msgType='hex'):
    """
    尝试打开串口并发送数据
    :param com: 串口号
    :param baund: 波特率
    :param parity: 校验位
    :param stopbits: 停止位
    :param maxReryCount: 最大重试次数
    :param delay: 重试延迟时间
    :param msgList: 发送的数据列表
    :param msgType: 数据类型（'hex' 或 'ascii'）
    :return: 返回串口对象和调试信息列表
    """
    emsg = ''
    serials = False
    serial_receive_list = []
    for i in range(maxReryCount):
        try:serials = serial.Serial(com, baund, parity=parity, stopbits=stopbits);break
        except Exception as e:
            time.sleep(delay)
            emsg = e
    if not serials:
        return False, '开启串口失败', emsg
    if serials.in_waiting > 0:
        serials.read(serials.in_waiting)  # 清空接收缓冲区
    if isinstance(msgList, str):
        msgList = [msgList]
    for msg in msgList:
        try:
            if msgType == 'hex':
                if isinstance(msg, str):        write_msg = bytes.fromhex(msg)
                elif isinstance(msg, bytes):    write_msg = msg
                else:
                    emsg = 'msgList must be str or bytes:{}'.format(type(msg))
                    serials.close()
                    return False, '发送类型错误', emsg
                serials.write(write_msg)
            elif msgType == 'ascii':
                serials.write(msg.encode('ascii'))
            else:
                emsg = 'msgType must be hex or ascii:{}'.format(msgType)
            for i in range(maxReryCount):
                if serials.in_waiting > 0:
                    response = serials.read(serials.in_waiting)
                    receive_msg = response.hex() if msgType == 'hex' else response.decode('ascii')
                    serial_receive_list.append(receive_msg)
                    break
                time.sleep(delay)
        except Exception as e:
            serials.close()
            return False, '发送信息失败', e
    serials.close()
    return True, serial_receive_list, emsg
    