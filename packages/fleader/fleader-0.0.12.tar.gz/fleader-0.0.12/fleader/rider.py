from fleader import fleader as rq
import time,os

local,queue,sem=rq.getGevent()#异步队列

q=queue()
l=local()
lennum=0
arr={}

def getp(_):
    while 1:
        qs=q.qsize()
        if qs==0:
            time.sleep(0.2)
        else:
            qg=q.get()
            url,request,parse,meta=qg['url'],qg['request'],qg['parse'],qg['meta']
            rp=response()
            try:
                rp.result=request(url)
                rp.meta=meta
                parse(rp)
            except Exception as e:
                print(e)
        qsz=q.qsize()
        #break
        if qs==0:
            global arr,lennum
            arr[_]=[qs,qsz]
            x=0
            for i in arr:
                if arr[i]==[0,0]:
                    x+=1
            if x==lennum:
                os._exit(0)
                # break

class response():
    result=''
    meta={}

class spider():
    start_urls = []
    mode=1
    if mode==1:
        num=20
    if mode==2:
        num=800
    def __init__(self):
        self.start()

    def request(self,url):
        return rq.get(url)

    def parse(self, response):
        pass

    def feed(self,url,meta={},callback=None,request=None):
        if callback == None:
            callback=self.parse
        if request == None:
            request=self.request
        if type(url)==str:
            url=[url]
        for u in url:
            food={}
            food['url']=u
            food['request']=request
            food['parse']=callback
            food['meta']=meta
            q.put(food) 

    def start(self):
        if len(self.start_urls)>0:
            self.feed(self.start_urls)
            num = self.num
            global lennum
            lennum=num
            mode = self.mode
            if mode==1:
                rq.pool(getp,range(num),num)
            if mode==2:
                rq.gPool(getp,range(num),num)
        else:
            print('hello rider')

if __name__ == '__main__':
    spider()
