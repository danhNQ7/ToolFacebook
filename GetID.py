import requests
import time
# from PyQt5.QtCore import QThread,pyqtSignal
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
    def update_token(self,token):
        self.accessToken=token
        self.payload['access_token']=self.accessToken
    def save_data(self,data):
        # with open(self.fileName,'a') as f:
        #     f.write(data+'\n')
        return data
    def get_info_user(self,iduser):
        query = str(iduser)
        data=[]
        r = requests.get(self.host+self.defaultVersion+query,params=self.payload)
        # print(r)
        result = r.json()
        return result
    def get_all_members_group(self,idGroup):
        # self.fileName = nameFileSave
        # self.save_data("GroupID: "+str(idGroup))
        query = str(idGroup)+'/members'
        return self.get_data(self.host+self.defaultVersion+query,self.payload)
    def get_all_friends_user(self,uid):
        # self.fileName=nameFileSave
        query=str(uid)+'/friends'
        return self.get_data(self.host+self.defaultVersion+query,self.payload)
    def get_all_user_liked_fanpage(self):
        pass
    def get_post_from_page_user(self,uid,limit=10):
        query =str(uid)+'/feed'
        customPayload = self.payload
        customPayload['fields'] ='id,message,shares,likes.summary(true),comments.summary(true).limit(1)'
        customPayload['limit']=str(limit)
        return self.get_data(self.host+self.defaultVersion+query,customPayload,2)
    def get_all_user_comment_post(self,idpost):
        query=str(idpost)+'/comments'
        customPayload = self.payload
        customPayload['fields']='from{name,id,gender,birthday,email,mobile_phone,location,age_range}'
        return self.get_data(self.host+'/v2.3/'+query,customPayload)
    def get_all_user_like_post(self,idpost):
        query=str(idpost)+'/likes'
        customPayload = self.payload
        customPayload['fields']='name,id,gender,birthday,email,mobile_phone,location,age_range'
        return self.get_data(self.host+'/v2.3/'+query,customPayload,1)
    def format_json(self,data):
        result =[]
        for tempData in data:
            for numRow,dataI in enumerate(tempData):
                # print(dataI['name'])
                if 'from' in dataI:
                    dataI=dataI['from']
                # print(dataI)
                tempResult={'stt':numRow,'uid' :'','name' :'','gender':'','birthday' :'','age_range' :'', 'email' : '','mobile_phone' : '','location' : ''}
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
    def get_data(self,url,params=None,flag = 0):
        
        if params!=None:
            # params['fields']='name,id,birthday,email,mobile_phone,location,age_range'
            r = requests.get(url=url,params=params)
            print(r.url)
        else :
            r = requests.get(url=url)
        print(r)
        result = r.json()
        if 'data' in result:
            # self.save_data(str(result['data']))
            self.data.append(result['data'])
            if 'next' in result['paging'] and flag!=2:
                return self.get_data(result['paging']['next'],None,flag)
            else:
        # print(data)
        #User like post
                if flag ==1:
                    temp_data = []
                    for i in self.data:
                        for j in i:
                            # print(j['id'])
                            temp_data.append(self.get_info_user(j['id']))
                    self.data = [temp_data]
                # print(data)
                # print(data)
                #Xu ly bai post cua trang or user
                if flag ==2:
                    # print(data)
                    dataFormat =self.format_json_post(self.data)
                    self.data =[]
                    return dataFormat
                # print(self.data)
                dataFormat =self.format_json(self.data)
                self.data =[]
                return dataFormat
        # return  self.format_json(self.data)
    def format_json_post(self,data):
        result =[]
        for numRow,dataI in enumerate(data[0]):
            tempResult={'stt':numRow,'id':'','message' :'','likes':'','comments' :'','shares' :'?'}
            if 'message' in dataI:
                tempResult['message']=dataI['message']
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
    def get_all_videos_group(self,idGroup,nameFileSave):
        
        self.fileName=nameFileSave
        # self.save_data("GroupID: "+str(idGroup))
        query=str(idGroup)+"/videos"
        payload={'fields':'source','limit':'1000','access_token':self.accessToken}
        self.get_data(self.host+query,payload)
    
def main():
    begin = time.time()
    ob = GetID("EAAAAUaZA8jlABAJCGmz5jXILm66IkQNZArr7jTaaL4ZBxwiAcgqumKZAI8znD7fzmcVlg4ZBD0RgIubup86JvPAvU5yOLthWQQNq6tIJDTnxL6QH5Tx7EKiqz5OaFY1U7N9ZClfV7sZBvxYS2pU1jaOExELMLxPHsAZD")
    # ob.get_all_members_group(263827544051298,'data.txt')
    # ob.get_all_videos_group(1173636692750000,'linkvideos.txt')
    # ob.get_all_user_comment_post('100005526070786_796691553858373','data3.txt')
    # ob.get_all_friends_user(
    # 
    # ,'data2.txt')
    # print(ob.get_info_user(100008122898339))
    # print(ob.get_all_user_like_post('941568386026009'))
    print(ob.get_post_from_page_user('548664955331244',10))
    print("Time: {} s".format(time.time()-begin))
def test():
    a =[]
    for i in range(50000000):
        a.append([i,i,i])
if __name__=='__main__':
    main()
    # test()
