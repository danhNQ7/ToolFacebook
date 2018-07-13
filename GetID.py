import requests
import time
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import threading
class ThreadGetData(QThread):
    processUpdate = pyqtSignal(float)
    processError = pyqtSignal(str)
    def __init__(self,url,params,table,flag=0,count=-1):
        QThread.__init__(self)
        self.url = url
        self.params=params
        self.flag =flag
        self.table = table
        self.current =0
        self.count=count
        # self.error =error
    def load_QTable(self,data,tab):
        print(self.current)
        # tab ={0:self.tableWidget_1,1:self.tableWidget_2,2:self.tableWidget_3,3:self.tableWidget_4,3:self.tableWidget_5}
        for row_number,data_row in enumerate(data):
            tab.insertRow(tab.rowCount())
            for col_number,value in enumerate(data_row):
                tab.setItem(tab.rowCount()-1,col_number,QtWidgets.QTableWidgetItem(str(value)))
        # print(tab.rowCount())
    def get_data(self,url,params=None,flag = 0):       
        if params!=None:
            # params['fields']='name,id,birthday,email,mobile_phone,location,age_range'
            r = requests.get(url=url,params=params)
            # print(r.url)
            result = r.json()
            if 'summary' in result:
                self.total = result['summary']['total_count']
                self.current =0
            elif self.count>0:
                self.total=self.count
                self.current=0
            else:
                self.total=0.1
        else :
            r = requests.get(url=url)
            result = r.json()
        print(r.url)
        print(r.status_code)
        if r.status_code ==200 and 'error' not in result:
            if 'data' in result:
                data=[]
                # self.save_data(str(result['data']))
                data.append(result['data'])
                # print(data)
            #User like post
                if flag ==1:
                    if params is not None:
                        self.payload2=params
                        self.total=len(data)
                    temp_data = []
                    print(data)
                    for i in data:
                        for j in i:
                            # print(j['id'])
                            temp_data.append(self.get_info_user(j['id']))
                    data = [temp_data]
                if flag ==2:
                    # print(data)
                    dataFormat =self.format_json_post(data)
                    data =[]
                    # print(dataFormat)
                # print(self.data)
                else:
                    dataFormat =self.format_json(data)
                # print(self.current)
                self.processUpdate.emit(self.current*1.0/self.total)
                # print(dataFormat)
                self.load_QTable(dataFormat,self.table)
                # input()
                if 'paging' in result and 'next' in result['paging'] and flag!=2:
                    return self.get_data(result['paging']['next'],None,flag)
                else :
                    self.processUpdate.emit(float(1))
                    self.current =0
        else: 
            # self.processError.emit('Đã có lỗi xảy ra(Mã lỗi): '+result['error']['message'])
            self.load_QTable([['Đã có lỗi xảy ra(Mã lỗi): '+result['error']['message']]],self.table)
            # time.sleep(3)
            # error='Đã có lỗi xảy ra(Mã lỗi): '+result['error']['message']
    def format_json(self,data):
        result =[]
        for tempData in data:
            for numRow,dataI in enumerate(tempData):
                self.current =self.current +1
                # print(dataI['name'])
                if 'from' in dataI:
                    dataI=dataI['from']
                # print(dataI)
                tempResult={'stt':self.current,'uid' :'','name' :'','gender':'','birthday' :'','age_range' :'', 'email' : '','mobile_phone' : '','location' : ''}
                if 'gender' in dataI:
                    tempResult['gender']=dataI['gender']
                if 'name' in dataI:
                    tempResult['name']=dataI['name']
                if 'id' in dataI:
                    tempResult['uid']=dataI['id']
                if 'birthday' in dataI:
                    tempResult['birthday']=dataI['birthday']
                if 'email' in dataI:
                    tempResult['email']=dataI['email']
                if 'mobile_phone' in dataI:
                    tempResult['mobile_phone']=dataI['mobile_phone']
                if 'location' in dataI:
                    tempResult['location']=dataI['location']['name']
                if 'age_range' in dataI:
                    tempResult['age_range']=dataI['age_range']
                result.append(list(tempResult.values()))
        return result
    
        # return  self.format_json(self.data)
    def format_json_post(self,data):
        result =[]
        for numRow,dataI in enumerate(data[0]):
            print(self.current)
            self.current=self.current+1
            tempResult={'stt':self.current,'id':'','message' :'','likes':'','comments' :'','shares' :'?'}
            if 'message' in dataI:
                tempResult['message']=dataI['message']
            else :
                tempResult['message']='Post Share'
            if 'id' in dataI:
                tempResult['id']=dataI['id']
            if 'shares' in dataI:
                tempResult['shares']=dataI['shares']['count']
            if 'likes' in dataI:
                tempResult['likes']=dataI['likes']['count']
            if 'comments' in dataI:
                tempResult['comments']=dataI['comments']['count']
            result.append(list(tempResult.values()))
        return result
    def get_info_user(self,iduser):
        query = str(iduser)
        data=[]
        r = requests.get('https://graph.facebook.com/v3.0/'+query,params=self.payload2)
        # print(r)
        result = r.json()
        return result
    def __del__(self):
        self.wait()
    def run(self):
        self.get_data(self.url,self.params,self.flag)

class GetID():
    
    def __init__(self,accessToken):
        self.accessToken=accessToken
        self.host ="https://graph.facebook.com"
        self.defaultVersion = '/v3.0/'
        self.payload={}
        self.payload['fields']='name,id,gender,birthday,email,mobile_phone,location,age_range'
        self.payload['limit']='2000'
        self.payload['access_token']=self.accessToken
        self.data =[]
        self.processGui =None
        self.error=''
    def update_token(self,token):
        self.accessToken=token
        self.payload['access_token']=self.accessToken
    def save_data(self,data):
        return data
    def check_error(self,error):
        print(error)
        self.error=error
    def get_all_members_group(self,idGroup,table):
        # self.fileName = nameFileSave
        # self.save_data("GroupID: "+str(idGroup))
        # self.error=''
        test =self.payload
        test['fields'] = 'member_count'
        r = requests.get(self.host+self.defaultVersion+str(idGroup)+'/',params=test)
        result = r.json()
        print(r.url)
        count =result['member_count']
        query = str(idGroup)+'/members'
        customPlayload =self.payload
        customPlayload['fields']='name,id,gender,birthday,email,mobile_phone,location,age_range'    
        thread= ThreadGetData(self.host+self.defaultVersion+query,self.payload,table,0,count)
        thread.processUpdate.connect(self.show)
        # thread.processError.connect(self.check_error)
        thread.start()
        thread.finished()
        # return self.error
    def show(self,val):
        self.processGui.setValue(val*100)
    def thread_wait(self):
        while self.error =='':
            time.sleep(2)
            print('dangchay')
            
    def get_all_friends_user(self,uid,table):
        # self.fileName=nameFileSave
        # self.error=''
        query=str(uid)+'/friends'
        thread = ThreadGetData(self.host+self.defaultVersion+query,self.payload,table)
        thread.processUpdate.connect(self.show)
        # thread.processError.connect(self.check_error)
        
        # t=threading.Thread(target=self.thread_wait)
        thread.start()
        
        # t.start()
        # t.join()
        thread.finished()
        # time.sleep(3)
        # print(self.error)
        # return self.error
        # return self.get_data(self.host+self.defaultVersion+query,self.payload)
    def get_all_user_liked_fanpage(self):
        pass
    def get_post_from_page_user(self,uid,limit,table):
        # self.error=''
        query =str(uid)+'/feed'
        customPayload = self.payload
        customPayload['fields'] ='id,message,shares,likes.summary(true),comments.summary(true).limit(1)'
        customPayload['limit']=str(limit)
        thread= ThreadGetData(self.host+self.defaultVersion+query,customPayload,table,2,int(limit))
        thread.processUpdate.connect(self.show)
        # thread.processError.connect(self.check_error)
        thread.start()
        thread.finished()
        # return self.error
    def get_all_user_comment_post(self,idpost,table):
        # self.error=''
        test =self.payload
        test['fields'] = 'comments'
        test['limit']=5
        r = requests.get(self.host+self.defaultVersion+str(idpost)+'/',params=test)
        result = r.json()
        print(r.url)
        count =result['comments']['count']
        query=str(idpost)+'/comments'
        customPayload = self.payload
        customPayload['fields']='from{name,id,gender,birthday,email,mobile_phone,location,age_range}'
        thread = ThreadGetData(self.host+'/v2.3/'+query,customPayload,table,0,count)
        thread.processUpdate.connect(self.show)
        # thread.processError.connect(self.check_error)
        thread.start()
        thread.finished()
        # return self.error
    def get_all_user_like_post(self,idpost,table,main):
        # self.error=''
        query=str(idpost)+'/likes'
        customPayload = self.payload
        customPayload['fields']='name,id,gender,birthday,email,mobile_phone,location,age_range'
        thread= ThreadGetData(self.host+'/v2.3/'+query,customPayload,table,main,1)
        thread.processUpdate.connect(self.show)
        thread.processError.connect(self.check_error)
        thread.start()
        thread.finished()
        # return self.error
    
    def get_all_videos_group(self,idGroup,nameFileSave):
        
        self.fileName=nameFileSave
        # self.save_data("GroupID: "+str(idGroup))
        query=str(idGroup)+"/videos"
        payload={'fields':'source','limit':'1000','access_token':self.accessToken}
        self.get_data(self.host+query,payload)
    
def main():
    import sys
    a = QtCore.QCoreApplication(sys.argv)
    begin = time.time()
    ob = GetID("EAAAAUaZA8jlABAJCGmz5jXILm66IkQNZArr7jTaaL4ZBxwiAcgqumKZAI8znD7fzmcVlg4ZBD0RgIubup86JvPAvU5yOLthWQQNq6tIJDTnxL6QH5Tx7EKiqz5OaFY1U7N9ZClfV7sZBvxYS2pU1jaOExELMLxPHsAZD")
    ob.get_all_members_group(263827544051298,None)
    # ob.get_all_videos_group(1173636692750000,'linkvideos.txt')
    # ob.get_all_user_comment_post('100005526070786_796691553858373','data3.txt')
    # ob.get_all_friends_user(
    # 
    # ,'data2.txt')
    # print(ob.get_info_user(100008122898339))
    # print(ob.get_all_user_like_post('941568386026009'))
    # print(ob.get_post_from_page_user('548664955331244',10))
    # ob.get_all_friends_user('100006122645127')
    print("Time: {} s".format(time.time()-begin))
    sys.exit(a.exec_())
if __name__=='__main__':
    main()
