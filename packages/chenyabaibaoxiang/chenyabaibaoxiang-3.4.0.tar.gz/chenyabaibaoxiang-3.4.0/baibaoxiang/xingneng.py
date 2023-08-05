import time
import threading
from baibaoxiang import baibaoxiangInterface,excel,sys_powel


ex=excel.InputExcel()
go= baibaoxiangInterface.go()
class a(threading.Thread):
    def __init__(self,url, data, header,name,user_sum):
        threading.Thread.__init__(self)
        self.url=url
        self.data = data
        self.header = header
        self.name = name
        self.user_sum=int(user_sum)


    def run(self):
        for i in range(self.user_sum):
            iss=[]
            run_time=time.time()
            name=str(self.name)+"-"+str(i)
            # print(self.name,"-",i,"本次执行时间是：",run_time)
            f=go.post(self.url,self.data,self.header,name)
            on_to_over_time=f.elapsed.total_seconds()
            # print(name,"发送请求到接收完数据的时间(总时长)",on_to_over_time,"秒，相当于",on_to_over_time*1000,"毫秒")
            iss.append(name)
            iss.append(f.status_code)
            try:
                iss.append(f.text)
            except:
                iss.append(f.json())
            iss.append(run_time)
            iss.append(on_to_over_time)
            # print(iss)
            ex.input_excel(iss)
            iss=[]



class Bingfa_test:
    def bingfa_test_go(self,url,data,name,user_sum,excel_address,excel_name,*headler):
        t1=time.time()
        k1=a(url,data,headler,name,user_sum)
        k1.start()
        t2 = time.time()
        t3 = float(t2) - float(t1)
        print("发起",user_sum,"请求，共耗时：", t3)
        ex.end(excel_address,excel_name)



