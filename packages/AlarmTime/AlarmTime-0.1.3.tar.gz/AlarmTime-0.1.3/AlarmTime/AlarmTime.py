import datetime
from dateutil.relativedelta import relativedelta
import re
import operator
import time
  
class DetectDate():
    mon = ['january','february','march','april','may','june','july','august','september','october','november','december']
    def __init__(self,device_time = '0'):
        if type(device_time)!=str:
            device_time = str(device_time)
        self.now = datetime.datetime.now()
        if '/' in device_time:
            cal_time = device_time.split('/')
            self.now = self.now.replace(year = int(cal_time[0]),month = int(cal_time[1]),day = int(cal_time[2]),hour = int(cal_time[3]),minute = int(cal_time[4]))
            
        elif device_time!='0':
            device_time = int(device_time)/1000.0
            year = datetime.datetime.fromtimestamp(int(device_time)).strftime('%Y')
            month = datetime.datetime.fromtimestamp(int(device_time)).strftime('%m')
            day = datetime.datetime.fromtimestamp(int(device_time)).strftime('%d')
            hour = datetime.datetime.fromtimestamp(int(device_time)).strftime('%H')
            minute = datetime.datetime.fromtimestamp(int(device_time)).strftime('%M')
            self.now = self.now.replace(year = int(year),month = int(month),day = int(day),hour = int(hour),minute = int(minute))
        self.start_time = self.now
        self.alarm_hour = self.now.hour
        self.alarm_minute = self.now.minute
        self.alarm_day = self.now.day
        self.alarm_month = self.now.month
        self.alarm_year = self.now.year
        self.text="ok"
        self.status = 1
# =============================================================================
# =============================================================================
    def DateTimeDetect(self,data):
        data = data.lower()
        data = data.replace('one','1').replace('two','2').replace('three','3').replace('four','4').replace('five','5').replace('six','6').replace('seven','7').replace('eight','8').replace('nine','9').replace('zero','0')
        # =============================================================================
        #     #detect hour and minute from integers
        # =============================================git commit -m "my comment about the changes"================================     
        integer = re.findall('\d+', data)
        alarm = self.now
        data_list = data.split(' ')
        dictionary = {}
        if 'day' in data_list:
            dictionary['day'] = data_list.index('day')
        elif 'days' in data_list:
            dictionary['day'] = data_list.index('days')
            
        if 'minute' in data_list:
            dictionary['minute'] = data_list.index('minute')
        if 'minutes' in data_list:
            dictionary['minute'] = data_list.index('minutes')
        
        if 'second' in data_list:
            dictionary['second'] = data_list.index('second')
        elif 'seconds' in data_list:
            dictionary['second'] = data_list.index('seconds')
        
        if 'hour' in data_list:
            dictionary['hour'] = data_list.index('hour')
        elif 'hours' in data_list:
            dictionary['hour'] = data_list.index('hours')
                    
        if 'month' in data_list:
            dictionary['month'] = data_list.index('month')
        elif 'months' in data_list:
            dictionary['month'] = data_list.index('months')
            
                    
        if 'year' in data_list:
            dictionary['year'] = data_list.index('year')
        elif 'years' in data_list:
            dictionary['year'] = data_list.index('years')
        
        sort_dictionary = sorted(dictionary.items(), key = operator.itemgetter(1))
        if ('hour' in dictionary.keys() or 'minute' in dictionary.keys() or 'second' in dictionary.keys() or 'day' in dictionary.keys() or 'month' in dictionary.keys()):
            for i in sort_dictionary:
                if 'day' in i[0] and len(integer)>0:
                    alarm = alarm + datetime.timedelta(days=int(integer[0]))
                    integer.remove(integer[0])
                if 'hour' in i[0] and len(integer)>=1:
                    alarm = alarm + datetime.timedelta(hours=int(integer[0]))
                    integer.remove(integer[0])
    #                print(alarm,integer)
                if 'minute' in i[0] and len(integer)>=1:
                    alarm = alarm + datetime.timedelta(minutes=int(integer[0]))
                    integer.remove(integer[0])
                if 'second' in i[0] and len(integer)>=1:
                    alarm = alarm + datetime.timedelta(seconds=int(integer[0]))
                    integer.remove(integer[0])
                if 'month' in i[0] and len(integer)>=1:
                    month = alarm.month+int(integer[0])
                    alarm = alarm+relativedelta(year=alarm.year+(month//12))
                    
                    alarm = alarm + relativedelta(month=(month%12))
                    integer.remove(integer[0])
                if 'year' in i[0] and len(integer)>=1:
                    alarm = alarm+relativedelta(year=alarm.year+int(integer[0]))
                    integer.remove(integer[0])
            
        else:

    # =============================================================================
    #  process data
    # =============================================================================
            key=0    
            if 'august' in data:
                key = 1
            data=data.replace("th","").replace("nd","").replace("st","").replace("rd","") 
            if(key):
                data = data.replace('augu','august')
            list_data = []
            for i in data.split(' '):
                 list_data.append(i)
    # =============================================================================
    #detect month and day for specific after 8 days type command or tomorrow/after tomorrow command
    # =============================================================================
            self.flag = 0
            if(('day'in data) and 'after tomorrow' in data):

                self.flag = 1
                n = self.now+datetime.timedelta(days=2)
                if(n.day==1):
                    n = self.now+relativedelta(month=self.now.month+1)
                    if(n.month==1):
                        n = self.now+relativedelta(year=self.now.year+1)
                        self.alarm_year = n.year
                self.alarm_day = n.day 
            elif('tomorrow' in data):
                self.flag = 1
                n = self.now+datetime.timedelta(days=1)
                self.alarm_day = n.day
                if(n.day==1):
                    n = self.now+relativedelta(month=self.now.month+1)
                    self.alarm_month = n.month
                    if(n.month==1):
                        n = self.now+relativedelta(year=self.now.year+1)
                        self.alarm_year = n.year
    # =============================================================================
    #         checking date
    # =============================================================================
            for i in self.mon:
                if(i in data):
                    pos2 = list_data.index(i)
                    self.alarm_month =self.mon.index(i)+1
    
                    for j in integer:
                        if j in list_data and (pos2>0 and list_data.index(j) == pos2-1):
                            self.alarm_day=int(j)
                            self.flag=1
                            integer.remove(j)
                            break
                        elif j in list_data and (pos2<len(list_data)-1 and list_data.index(j) == pos2+1):
                            self.alarm_day=int(j)
                            self.flag=1
                            integer.remove(j)
                            break
                    if self.alarm_month<self.now.month:
                        n = self.now+relativedelta(year=self.now.year+1)
                        self.alarm_year = n.year
                    elif self.alarm_month==self.now.month and self.alarm_day<self.now.day:
                        n = self.now+relativedelta(year=self.now.year+1)
                        self.alarm_year = n.year
                    elif self.alarm_month==self.now.month and self.alarm_day==self.now.day and self.alarm_hour<self.now.hour:
                        n = self.now+relativedelta(year=self.now.year+1)
                        self.alarm_year = n.year
                    elif self.alarm_month==self.now.month and self.alarm_day==self.now.day and self.alarm_hour==self.now.hour and self.alarm_minute<=self.now.minute:
                        n = self.now+relativedelta(year=self.now.year+1)
                        self.alarm_year = n.year
                    self.flag = 1    
                    break
            
            if(len(integer) == 2):
                self.alarm_hour = int(integer[0])
                self.alarm_minute = int(integer[1])
            elif(len(integer) == 1):
                self.alarm_hour = int(integer[0])
                self.alarm_minute = 0
                if(self.alarm_hour>23): #convert invalid time to valid
                    hour_str = str(self.alarm_hour)
                    if(len(hour_str)==4):
                        self.alarm_minute = int(hour_str[2:])
                        self.alarm_hour = int(hour_str[:2])
                    elif(len(hour_str)==3):
                        self.alarm_minute = int(hour_str[1:])
                        self.alarm_hour = int(hour_str[0])
                    elif(len(hour_str)==2):
                        self.alarm_minute = int(hour_str[1])
                        self.alarm_hour = int(hour_str[0])       
            else:
                if self.flag ==1:
                    self.alarm_hour = 0
                    self.alarm_minute = 0
                else:
                    self.text = "When do you want to set?"
                    self.status=2
    # =============================================================================
    #      #add extra 12 hours for 'pm'  
    # =============================================================================
            
            if ("p.m" in data or 'pm' in data) and (self.alarm_hour !=12):
                self.alarm_hour+=12
            elif("a.m" in data or 'pm' in data) and (self.alarm_hour==12):
                self.alarm_hour-=12
    # =============================================================================
    #             for checking valid time
    # =============================================================================
            if(self.alarm_hour>24 or self.alarm_minute>60):
                self.text = "Invalid Time! Would you like to tell me the right time again."
                self.alarm_hour = 1
                self.alarm_minute = 1
                self.status=2
    # =============================================================================
    #             making half valid time full valid
    # =============================================================================
            elif (self.alarm_hour<self.now.hour and self.flag!=1):
                self.alarm_hour+=12
                if 'p.m' in data or 'pm' in data:
                    self.alarm_hour+=12
                elif('a.m' in data or 'am' in data):
                    self.alarm_hour+=12
                if (self.alarm_hour<self.now.hour):
                    self.alarm_hour+=12
                elif (self.alarm_hour==self.now.hour and self.alarm_minute<=self.now.minute):
                    self.alarm_hour+=12
                if(self.alarm_hour>=24):
                    self.alarm_hour-=24
                    n = self.now+datetime.timedelta(days=1)
                    self.alarm_day = n.day
                   
                    if(n.day==1):
                        n = self.now+relativedelta(month=self.now.month+1)
                        self.alarm_month = n.month
                        if(n.month==1):
                            n = self.now+relativedelta(year=self.now.year+1)
                            self.alarm_year = n.year
    
            elif(self.alarm_hour==self.now.hour  and self.alarm_minute<=self.now.minute and self.flag!=1):
                
                self.alarm_hour+=12
                if 'p.m' or 'P.M' in data:
                    self.alarm_hour+=12
                if(self.alarm_hour>=24):
                    self.alarm_hour-=24
                    
                    n = self.now+relativedelta(day=self.now.day+1)
                    self.alarm_day = n.day
                   
                    if(n.day==1):
                        n = self.now+relativedelta(month=self.now.month+1)
                        if(n.month==1):
                            n = self.now+relativedelta(year=self.now.year+1)
                            self.alarm_year = n.year
            elif(self.alarm_hour==self.now.hour  and self.alarm_minute<=self.now.minute and self.alarm_day == self.now.day and self.flag ==1):
                self.alarm_hour+=12
                if(self.alarm_hour>=24):
                    self.text = "Invalid Time! Would you like to tell me the right time again."
                    self.alarm_hour = 1
                    self.alarm_minute = 1
                    self.status=2
             
            elif(self.alarm_hour<self.now.hour and self.alarm_day == self.now.day and self.flag ==1):
                self.alarm_hour+=12
                if(self.alarm_hour>=24):
                    self.text = "Invalid Time! Would you like to tell me the right time again."
                    self.alarm_hour = 1
                    self.alarm_minute = 1
                    self.status=2
            alarm = self.now.replace(year=self.alarm_year, month=self.alarm_month, day = self.alarm_day,hour=self.alarm_hour, minute=self.alarm_minute, second = 0)

        return alarm
    
    
    def minute_diff_from_now(self,data):
        alarm = self.DateTimeDetect(data)
        alarm_sec = time.mktime(alarm.timetuple())
        now_sec = time.mktime(self.start_time.timetuple())
        ###  calculate second distance from now to alarm
        difference = alarm_sec-now_sec
        return difference/60
    
    
    def hour_diff_from_now(self,data):
        alarm = self.DateTimeDetect(data)
        alarm_sec = time.mktime(alarm.timetuple())
        now_sec = time.mktime(self.start_time.timetuple())
        ###  calculate second distance from now to alarm
        difference = alarm_sec-now_sec
        return difference/3600
    
    
    def day_diff_from_now(self,data):
        alarm = self.DateTimeDetect(data)
        alarm_sec = time.mktime(alarm.timetuple())
        now_sec = time.mktime(self.start_time.timetuple())
        ###  calculate second distance from now to alarm
        difference = alarm_sec-now_sec
        return difference/(3600*24)
    
    
    def second_diff_from_now(self,data):
        alarm = self.DateTimeDetect(data)
        alarm_sec = time.mktime(alarm.timetuple())
        now_sec = time.mktime(self.start_time.timetuple())
        ###  calculate second distance from now to alarm
        difference = alarm_sec-now_sec
        return difference
    
    
    def milisecond_diff_from_now(self,data):
        alarm = self.DateTimeDetect(data)
        alarm_sec = time.mktime(alarm.timetuple())
        now_sec = time.mktime(self.start_time.timetuple())
        ###  calculate second distance from now to alarm
        difference = alarm_sec-now_sec
        return difference*1000

