def GPGGA2loc(strings):
    defalut_GGA = [0]*5
    try:
        strings = strings.split(',')
        if len(strings)<6: return 0
        if strings[2]=='' or strings[4]=='' or strings[6]=='' or strings[7]=='':
            return defalut_GGA
        else:
            lat = sate2location(strings[2])
            lon = sate2location(strings[4])
            sat = float(strings[7])
            num = float(strings[8])
            try:
                high = float(strings[9])+float(strings[11])
            except:
                high = 0
            return [lat,lon,sat,num,high]
    except Exception as e:
        print('GPGGA2loc:{}'.format(e))
        return defalut_GGA
def GNVTG2loc(strings):
    default_VTG = [0]*5
    return default_VTG
def HEADINGA2loc(strings):
    default_heading = [0]*6
def KSXT2loc(strings):
    default_ksxt = [0]*7
    try:
        strings = strings.split(',')
        if len(strings)<6: return 0
        if strings[1]=='' or strings[2]=='' or strings[3]=='' :
            return default_ksxt
        else:
            time = float(strings[1])
            lon = float(strings[2])
            lat = float(strings[3])
            high = float(strings[4])
            east = float(strings[17])
            north = float(strings[18])
            up = float(strings[19])
            return [time,lon,lat,high,east,north,up]
    except Exception as e:
        print('GPGGA2loc:{}'.format(e))
        return default_ksxt

def sate2location(sate_data):
    try:
        sate_data = float(sate_data)
        int_date = sate_data//100
        float_date = (sate_data-int_date*100)/60
        return int_date+float_date
    except:
        return 0