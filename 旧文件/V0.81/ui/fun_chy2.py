import struct 
crc_table = [
    0,1996959894,3993919788,2567524794,124634137,1886057615,3915621685,2657392035,
    249268274,2044508324,3772115230,2547177864,162941995,2125561021,3887607047,2428444049,
    498536548,1789927666,4089016648,2227061214,450548861,1843258603,4107580753,2211677639,
    325883990,1684777152,4251122042,2321926636,335633487,1661365465,4195302755,2366115317,
    997073096,1281953886,3579855332,2724688242,1006888145,1258607687,3524101629,2768942443,
    901097722,1119000684,3686517206,2898065728,853044451,1172266101,3705015759,2882616665,
    651767980,1373503546,3369554304,3218104598,565507253,1454621731,3485111705,3099436303,
    671266974,1594198024,3322730930,2970347812,795835527,1483230225,3244367275,3060149565,
    1994146192,31158534,2563907772,4023717930,1907459465,112637215,2680153253,3904427059,
    2013776290,251722036,2517215374,3775830040,2137656763,141376813,2439277719,3865271297,
    1802195444,476864866,2238001368,4066508878,1812370925,453092731,2181625025,4111451223,
    1706088902,314042704,2344532202,4240017532,1658658271,366619977,2362670323,4224994405,
    1303535960,984961486,2747007092,3569037538,1256170817,1037604311,2765210733,3554079995,
    1131014506,879679996,2909243462,3663771856,1141124467,855842277,2852801631,3708648649,
    1342533948,654459306,3188396048,3373015174,1466479909,544179635,3110523913,3462522015,
    1591671054,702138776,2966460450,3352799412,1504918807,783551873,3082640443,3233442989,
    3988292384,2596254646,62317068,1957810842,3939845945,2647816111,81470997,1943803523,
    3814918930,2489596804,225274430,2053790376,3826175755,2466906013,167816743,2097651377,
    4027552580,2265490386,503444072,1762050814,4150417245,2154129355,426522225,1852507879,
    4275313526,2312317920,282753626,1742555852,4189708143,2394877945,397917763,1622183637,
    3604390888,2714866558,953729732,1340076626,3518719985,2797360999,1068828381,1219638859,
    3624741850,2936675148,906185462,1090812512,3747672003,2825379669,829329135,1181335161,
    3412177804,3160834842,628085408,1382605366,3423369109,3138078467,570562233,1426400815,
    3317316542,2998733608,733239954,1555261956,3268935591,3050360625,752459403,1541320221,
    2607071920,3965973030,1969922972,40735498,2617837225,3943577151,1913087877,83908371,
    2512341634,3803740692,2075208622,213261112,2463272603,3855990285,2094854071,198958881,
    2262029012,4057260610,1759359992,534414190,2176718541,4139329115,1873836001,414664567,
    2282248934,4279200368,1711684554,285281116,2405801727,4167216745,1634467795,376229701,
    2685067896,3608007406,1308918612,956543938,2808555105,3495958263,1231636301,1047427035,
    2932959818,3654703836,1088359270,936918000,2847714899,3736837829,1202900863,817233897,
    3183342108,3401237130,1404277552,615818150,3134207493,3453421203,1423857449,601450431,
    3009837614,3294710456,1567103746,711928724,3020668471,3272380065,1510334235,755167117
]

def calculate_td_hex(data_list):
    struct_string = 'BbhhhhhhiiihBBBBBBBbhHhhHbBBb'
    struct_list = [i for i in struct_string]
    struct_endian = '<'
    struct_para = [
        1,1,0.0054931640625,0.0054931640625,0.0054931640625,
        0.02,0.02,0.02,0.0003017485/3600,0.0003017485/3600,0.01,
        1,1,1,1,1,1,10,0.1,1,
        0.5,0.0054931640625,0.0054931640625,0.0054931640625,0.0054931640625,
        1,5,1,1
    ]
    struct_return_list = []
    for i in range(len(struct_string)):
        try: pack_data = struct.pack(struct_endian+struct_list[i],int(data_list[i]/struct_para[i]))
        except: pack_data = struct.pack(struct_endian+struct_list[i],0)
        struct_return_list.append(pack_data)
    return struct_return_list
    
def calculate_fz_hex(data_list):
    struct_string = 'BbiiiiiiB'
    struct_list = [i for i in struct_string]
    struct_endian = '<'
    struct_para = [
        1,1,
        0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,
        1
    ]
    struct_return_list = []
    for i in range(len(struct_string)):
        try: pack_data = struct.pack(struct_endian+struct_list[i],int(data_list[i]/struct_para[i]))
        except: pack_data = struct.pack(struct_endian+struct_list[i],0)
        struct_return_list.append(pack_data)
    return struct_return_list
    
def calculate_gnss_hex(data_list):
    struct_string = 'BBBhhh'+ 'iiii'+ 'HBBBBBB'+ 'BBBHBBHB'+ 'HhBBBBB'+'BBBB'
    struct_list = [i for i in struct_string]
    struct_endian = '<'
    struct_para = [
        1,1,0.1,0.02,0.02,0.02,
        0.0003017485/3600,0.0003017485/3600,0.01,0.01,
        1,1,1,1,1,1,0.1,
        1,1,1,1,1,1,1,1,
        0.0054931640625,0.0054931640625,0.1,0.1,0.1,1,1
    ]
    struct_return_list = []
    for i in range(len(struct_string)):
        try: pack_data = struct.pack(struct_endian+struct_list[i],int(data_list[i]/struct_para[i]))
        except: pack_data = struct.pack(struct_endian+struct_list[i],0)
        struct_return_list.append(pack_data)
    return struct_return_list

def calculate_crc32(buffer: bytearray) -> int:
    """
    计算给定二进制缓冲区的 CRC32 值
    :param buffer: 二进制缓冲区（bytearray）
    :return: 计算得到的 CRC32 值
    """
    ul_crc = 0
    for byte in buffer:
        ul_crc = crc_table[(ul_crc ^ byte) & 0xff] ^ (ul_crc >> 8)
    return ul_crc

def try_int_data(data,default=1):
    try:
        return int(data),False
    except Exception as e:
        return default,e
def try_float_data(data,default=1):
    try:
        return float(data),False
    except Exception as e:
        return default,e
def try_hex_data(data,default=1):
    try:
        return bytes.fromhex(data),False
    except Exception as e:
        return bytes.fromhex(default),e

def crc_1188a(data_add):
    len_word = len(data_add) // 2  # 计算数据长度的一半
    word = [0] * len_word  # 初始化word数组
    crc_value = 0x0000  # 初始化CRC值

    for i in range(len_word):
        word[i] = (data_add[2 * i] << 8) + data_add[2 * i + 1]
        word[i] = ((word[i] >> (i % 16)) | (word[i] << (16 - (i % 16)))) & 0xFFFF
        crc_value ^= word[i]
    
    return crc_value

class class_rule:
    def __init__(self):
        self.rules_lists_format = 'xcbB?hHiIlLqQfdspPtyY'   # 解算规则可用范围
        # 通用参数
        # 规则文件名称
        self.filename = ''
        # 帧头
        self.header = b''
        # 帧尾
        self.ender = b''
        # 大小端
        self.format = '>'
        # 规则长度
        self.rule_length = 1
        # 结算规则
        self.decode_rules = ''
        # 文件标题
        self.file_title = []
        # 结算格式
        self.rule_list = []
        # 是否保存
        self.save_list = []
        # 系数
        self.para_list = []
        # 标题
        self.titl_list = []
        # 排序
        self.cout_list = []
        # 默认值/其他 - 废弃
        self.defa_list = []
        # 是否结算时输出hex原始数
        self.dhex_list = []
        
        # 1553 指定参数
        self.mode = 'normal'
        # 发送间隔
        self.send_ms = 1
        # 每秒频率
        self.send_hz = 1000
        # 子地址
        self.addr = 1

        # 调试报错信息列表
        self.debug_flag_onetime = False
        self.debug_flag_alltime = False
        self.debug_list = []
        self.debug_decode_list = []
        # 调试显示标志位
        self.debug_flag1 = False
        self.debug_flag2 = False
        self.debug_flag3 = False
        self.debug_flag4 = False
        self.debug_flag5 = False
    def reset_debug(self):
        if self.debug_flag_onetime | self.debug_flag_alltime:
            self.debug_flag_onetime = False
            self.debug_list = []
            self.debug_decode_list = []

    def read_rule_file(self,files,filename = 'None'):
        line_count = -1
        self.filename = filename.split('.')[0]
        if len(files)<=0:
            return False,'文件长度为0'
        if '\n' not in files:
            return False,'规则文件读取错误' 
        for line in files.split('\n'):
            if len(line)==0:
                break
            line_count+=1
            rules = line.split()
            if line_count==0:
                self.file_title = rules
            elif len(rules[0])>1:
                self.debug_list.append('{} 规则文件长度不符:<{}>'.format(line_count,rules[0]))
                continue
            elif '#' in rules[0]:
                # 发送频率
                if 'send_ms' in rules[1]:
                    self.send_ms = int(rules[2])
                    if self.send_ms==0:
                        self.send_hz = 0
                    else:
                        self.send_hz = int( 1000/self.send_ms )
                # 大小端
                elif 'rulehead' in rules[1]:
                    self.format = rules[2]
                elif 'send' in rules[1]:
                    self.debug_list.append('{} send-废弃参数{}'.format(line_count,rules[2]))
                    continue
                elif 'rece' in rules[1]:
                    self.debug_list.append('{} rece-废弃参数{}'.format(line_count,rules[2]))
                    continue
                # 1553专用 子地址
                elif 'addr' in rules[1]:
                    self.addr,result = try_int_data(rules[2])
                    if result != False:
                        self.debug_list.append('{} addr取整数错误<{} {}>'.format( line_count,rules[2],result ))
                # 帧头
                elif ('head' in rules[1])&('rule' not in rules[1]):
                    self.header,result = try_hex_data(''.join(rules[2:]))
                    if result != False:
                        self.debug_list.append('{} head取hex错误<{} {}>'.format( line_count,''.join(rules[2:]),result ))

            elif rules[0] in self.rules_lists_format:
                try:
                    self.rule_list.append(rules[0])
                    self.save_list.append(rules[1])
                    self.para_list.append(rules[2])
                    self.titl_list.append(rules[3])
                    self.cout_list.append(rules[4])
                    try:
                        self.defa_list.append(rules[5])
                    except Exception as e:
                        self.defa_list.append('0')
                        self.debug_list.append('{} 注释为空 ：{}'.format(line_count,e))

                except Exception as e:
                    debug_messages = '{} 严重错误：逐行读取规则文件失败:{} '.format(line_count,e)
                    self.debug_list.append(debug_messages)
                    print(debug_messages)

            else:
                self.debug_list.append('{} 未知规则<{}>'.format(line_count,' '.join(rules)))
        self.update_decode_rules()
        self.update_rule_length()
        self.float_para_list()
        return True,'解算完成'

    def update_decode_rules(self):
        self.decode_rules = self.format+''.join(self.rule_list)
    def update_rule_length(self):
        self.rule_length = struct.calcsize(self.decode_rules)
    def float_para_list(self):
        self.dhex_list = []
        for i in range(len(self.para_list)):
            # 不结算而是按照hex格式输出
            if ('h' in self.para_list[i]) | ('H' in self.para_list[i]):
                self.dhex_list.append(1)
                float_data = int(1)
            else:
                self.dhex_list.append(0)
                float_data = float(self.para_list[i])
            # int_data = int(self.para_list[i])
            if float_data.is_integer():
                self.para_list[i] = int(float_data)
            else:
                self.para_list[i] = float_data
    def decode_hex_data(self,hex_data):
        if not hex_data.startswith(self.header):
            self.debug_decode_list.append('帧头错误 {}'.format(hex_data[:len(self.header)+2]))
        if len(hex_data)>self.rule_length:
            hex_data = hex_data[:self.rule_length]
            self.debug_decode_list.append('长度过长 rule_length:{} hex_length:{}'.format(self.rule_length,len(hex_data)))
        if len(hex_data)<self.rule_length:
            hex_data = hex_data.rjust(self.rule_length,b'\x00')
        try:
            decode_data = struct.unpack(self.decode_rules,hex_data)
            decode_data = list(decode_data)
        except Exception as e:
            # decode_data = False
            self.debug_decode_list.append('解算错误 :{} {}'.format(hex_data.hex(),e))
            return False
        try:
            for i in range(len(self.para_list)):
                decode_data[i] *= self.para_list[i]
        except Exception as e :
            self.debug_decode_list.append('参数错误:{} {}'.format(e,decode_data))


        # print(decode_data)
        # return list(decode_data)
        return decode_data

        

class Turntable_class:
    def __init__(self):
        # 转台通讯协议数据帧格式
        self.header='AAAA5555'
        self.command_length = '3800'
        self.command_count = '0100'
        self.inside_command='80'
        self.inside_para1 = '00000000'
        self.inside_para2 = '00000000'
        self.inside_para3 = '00000000'
        self.outside_command='00'
        self.outside_para1 = '00000000'
        self.outside_para2 = '00000000'
        self.outside_para3 = '00000000'
        self.otherside_command='00'
        self.otherside_para1 = '00000000'
        self.otherside_para2 = '00000000'
        self.otherside_para3 = '00000000'
        self.thermostat_command = 'FF'
        self.thermostat_speed = '00'
        self.thermostat_target= '0000'
        self.spare_command = 'FFFFFFFF'
        self.check_command = '00'
        self.all_hex = ''
        self.split_hex = ''
    # 组合各数据帧 计算校验并返回总指令
    def get_command(self):
        all_hex = ''.join([self.command_length,self.command_count,self.inside_command,self.inside_para1,self.inside_para2,self.inside_para3,self.outside_command,self.outside_para1,self.outside_para2,self.outside_para3,self.otherside_command,self.otherside_para1,self.otherside_para2,self.otherside_para3,self.thermostat_command,self.thermostat_speed,self.thermostat_target,self.spare_command])
        # self.command_count = int2hex(int(reverse(self.command_count),16)+1,4)
        # print(self.command_count)
        split_hex = ''
        check = 0
        for i in range(len(all_hex)//2):
            bit = all_hex[i*2:i*2+2]
            split_hex+=bit+' '
            check+=int(bit,16)
        check = int2hex(check)
        all_hex += check
        split_hex += check
        self.check_command = check
        self.all_hex = self.header+all_hex
        self.split_hex = 'AA AA 55 55 '+split_hex
        return self.all_hex
    # 内框置零
    def reset_inside(self):
        self.inside_command='00'
        self.inside_para1 = '00000000'
        self.inside_para2 = '00000000'
        self.inside_para3 = '00000000'
        return self.get_command()
    # 外框置零
    def reset_outside(self):
        self.outside_command='00'
        self.outside_para1 = '00000000'
        self.outside_para2 = '00000000'
        self.outside_para3 = '00000000'
        return self.get_command()
    # 内框归零
    def reset_inside(self):
        self.inside_command = '81'
        self.inside_para1 = reverse(int2hex(0*10000,8))
        self.inside_para2 = reverse(int2hex(10*10000,8))
        self.inside_para3 = reverse(int2hex(10*100,8))
        return self.get_command()
    # 外框归零
    def reset_outside(self):
        self.outside_command = '81'
        self.outside_para1 = reverse(int2hex(0*10000,8))
        self.outside_para2 = reverse(int2hex(10*10000,8))
        self.outside_para3 = reverse(int2hex(10*100,8))
        return self.get_command()
    # 内框设置位置
    def inside_location(self,location=0,speed=10,acceleration=10):
        self.inside_command = '81'
        self.inside_para1 = reverse(int2hex(int(location*10000),8))
        self.inside_para2 = reverse(int2hex(int(speed*10000),8))
        self.inside_para3 = reverse(int2hex(int(acceleration*100),8))
        return self.get_command()
    # 内框设置速率
    def inside_speed(self,speed=10,acceleration=10):
        self.inside_command = '82'
        self.inside_para1 = reverse(int2hex(int(speed*10000),8))
        self.inside_para2 = reverse(int2hex(int(acceleration*100),8))
        self.inside_para3 = '00000000'
        return self.get_command()
    # 外框设置位置

    def outside_location(self,location=0,speed=10,acceleration=10):
        self.outside_command = '81'
        self.outside_para1 = reverse(int2hex(int(location*10000),8))
        self.outside_para2 = reverse(int2hex(int(speed*10000),8))
        self.outside_para3 = reverse(int2hex(int(acceleration*100),8))
        return self.get_command()
    # 外框设置速率
    def outside_speed(self,speed=10,acceleration=10):
        self.outside_command = '82'
        self.outside_para1 = reverse(int2hex(int(speed*10000),8))
        self.outside_para2 = reverse(int2hex(int(acceleration*100),8))
        self.outside_para3 = '00000000'
        return self.get_command()

decode_rule_01 = '''#	大小端	是否保存	系数	标题	排序	注释
#	baund	115200				
#	check	none	(none/odd/even			
#	header	99	66			
#	latitude	39.73675				
#	longitude	116.50984				
#	height	20				
#	alignment_time	100				
#	receive_hz	50		
#	drop0data    None   [1]					
#	rulehead	<				
B	0	1	0x99	N		
B	0	1	0x66	N		
B	0	1	帧数据长度	N		
I	1	1	导航时间	0		
i	1	8.381903175442434e-08	纬度	1		
i	1	7.628928873515189e-06	高度	2		
i	1	8.381903175442434e-08	经度	3		
h	1	0.007812738425855281	X轴速度	N		
h	1	0.007812738425855281	Y轴速度	N		
h	1	0.007812738425855281	Z轴速度	N		
h	1	0.005493331705679495	横滚角	N		
h	1	0.005493331705679495	航向角	N		
h	1	0.005493331705679495	俯仰角	N		
h	1	0.009155552842799158	X轴角速率	N		
h	1	0.009155552842799158	Y轴角速率	N		
h	1	0.009155552842799158	Z轴角速率	N		
h	1	0.0030518509475997192	X轴加速度	N		
h	1	0.0030518509475997192	Y轴加速度	N		
h	1	0.0030518509475997192	Z轴加速度	N		
I	1	1	状态字低32位	N		
I	1	1	状态字高32位	N		
I	1	1	算法状态字低32位	N		
B	1	1	导航方式状态字	N						
#	rulehead	<	
B	1	1	GPS状态	N		
B	1	1	接收机定位星数	N		
B	1	1	备份	N		
i	1	8.381903175442434e-08	接收机纬度	N		
i	1	7.628928873515189e-06	接收机高度	N		
i	1	8.381903175442434e-08	接收机经度	N		
h	1	0.005493331705679495	接收机航向	N		
h	1	0.028125878933716678	接收机前向速度	N		
h	1	0.007812738425855281	接收机PDOP值	N					
#	rulehead	<		
h	1	1	导航软件版本号	N		
I	1	1	惯导产品编号	N		
h	1	1	惯导滚动角误差估计值	N		
h	1	1	惯导俯仰角误差估计值	N		
h	1	1	X加表零位估计值	N		
h	1	1	Y加表零位估计值	N		
h	1	1	Z加表零位估计值	N		
h	1	0	备份	N		
h	1	0	备份	N		
B	1	0	备份	N		
B	1	0	异或校验	N		
B	1	0	和校验	N		'''
decode_rule_02 = '''#	是否保存	系数	标题	排序	注释
#	baund	460800			
#	check	none	(none/odd/even		
#	header	55	AA		
#	ender	C0	FF		
#	latitude	39.73675			
#	longitude	116.50984			
#	height	20			
#	alignment_time	200			
#	receive_hz	200			
#	special_flag	gd1s_wd			
#	sum_check	None	[2,3:61]
#	drop0data    [1]			
#	rulehead	>			
B	0	1	0x55	N	
B	0	1	0xAA	N	
B	0	1	校验和	N	（3~61字节的和）
B	0	1	PPS到来时间差	N	（4us/LSB
H	0	1	状态字	N	（0x07:标识PPS到来；）
h	1	0.0625	z加表温度	12	（输出值/16为加表温度℃）
I	1	0.005	5ms计数	0	
f	1	41256000	Gx	1	（5ms的角度增量，单位为弧度）
f	1	41256000	Gy	2	（5ms的角度增量，单位为弧度）
f	1	41256000	Gz	3	（5ms的角度增量，单位为弧度）
f	1	200	Ax	4	（5ms的速度增量，m/s）
f	1	200	Ay	5	（5ms的速度增量，m/s）
f	1	200	Az	6	（5ms的速度增量，m/s）
h	1	0.0625	x陀螺温度	7	（输出值为陀螺温度℃）
h	1	0.0625	y陀螺温度	8	（输出值为陀螺温度℃）
h	1	0.0625	z陀螺温度	9	（输出值为陀螺温度℃）
h	1	0.0625	x加表温度	10	（输出值/16为加表温度℃）
h	1	0.0625	y加表温度	11	（输出值/16为加表温度℃）
B	1	1	校正使能	N	
B	1	1	无线电有效标志	N	
B	1	1	气压高度标志	N	
B	1	1	卫导模式	N	
B	1	1	保留	N	
B	1	1	系统工作状态	N	
B	1	1	卫导1更新标志	N	
B	1	1	卫导2更新标志	N	
B	1	1	5ms标志	N	
x	0	1	状态0	N	
x	0	1	状态1	N	
x	0	1	状态2	N	
x	0	1	保留	N	
x	0	1	保留	N	
x	0	1	保留	N	
x	0	1	保留	N	
x	0	1	0xC0	N	
x	0	1	0xFF	N	
#	rulehead	<			
B	0	1	0x66	N	
B	0	1	0x99	N	
B	0	1	校验和	N	（3~61字节的和）
H	1	1	GPS周	N	
I	1	1.00E-03	GPS秒	N	
i	1	1.00E-07	卫导1纬度	N	
i	1	1.00E-07	卫导1经度	N	
i	1	1.00E-03	卫导1高度	N	
H	1	1.00E-03	卫导1PDOP	N	
B	1	1.00E+00	卫导1定位状态	N	
B	1	1.00E+00	卫导1卫星数	N	
i	1	1.00E-03	真北航向角	N	
i	1	1.00E-03	地面速度	N	
B	1	1.00E+00	模式指示	N	
B	1	1.00E+00	卫导选择使能	N	
B	1	1.00E+00	卫导通道标志	N	
B	1	1.00E+00	卫导模式	N	
i	1	1.00E-07	卫导2纬度	N	
i	1	1.00E-07	卫导2经度	N	
i	1	1.00E-03	卫导2高度	N	
H	1	1.00E-03	卫导2PDOP	N	
B	1	1.00E+00	卫导2定位状态	N	
B	1	1.00E+00	卫导2卫星数	N	
i	1	1.00E-03	卫导2真北航向角	N	
i	1	1.00E-03	卫导2地面速度	N	
B	1	1.00E+00	卫导2模式指示	N	
B	0	1	0xC0	N	
B	0	1	0xFF	N	
#	rulehead	<			
B	0	1	0xAA	N	
B	0	1	0xBB	N	
B	0	1	校验和	N	（3~61字节的和）
H	1	1	周	N	（低字节在前）
I	1	0.001	秒	N	（低字节在前），量纲：1e-3
i	1	1.00E-07	纬度	N	（4字节，低字节在前，单位：度）
i	1	1.00E-07	经度	N	（4字节，低字节在前，单位：度）
i	1	1.00E-03	高度	N	（4字节，低字节在前，单位：米）
i	1	1.00E-04	东向速度x	N	（低字节在前），量纲：1e-4，单位：m/s
i	1	1.00E-04	北向速度y	N	（低字节在前），量纲：1e-4，单位：m/s
i	1	1.00E-04	天向速度z	N	（低字节在前），量纲：1e-4，单位：m/s
i	1	1.00E-06	俯仰角x	N	（低字节在前），量纲：1e-6，单位：度
i	1	1.00E-06	滚转角y	N	（低字节在前），量纲：1e-6，单位：度
i	1	1.00E-06	偏航角z	N	（低字节在前），量纲：1e-6，单位：度
B	1	1	状态字	N	（0x01：初始对准；0x02：纯惯性；0x03：纯惯性
H	1	1	耗时	N	
h	1	1	加表X零位	N	（低字节在前，单位：ug）
h	1	1	加表Y零位	N	（低字节在前，单位：ug）
h	1	1	加表Z零位	N	（低字节在前，单位：ug）
b	1	1.00E-03	陀螺X零位	N	（低字节在前，单位：度）
b	1	1.00E-03	陀螺Y零位	N	（低字节在前，单位：度）
b	1	1.00E-03	陀螺Z零位	N	（低字节在前，单位：度）
B	0	1	保留	N	
H	0	1	保留	N	
H	0	1	保留	N	
B	0	1	0xC0	N	
B	0	1	0xFF	N	'''