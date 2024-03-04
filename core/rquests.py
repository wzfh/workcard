import requests


class Rquests():
    def __init__(self,api_url):
        self.api_url=api_url
        self.session=requests.session()

    def get(self,url,**kwargs):
        return self.request(url,'GET',**kwargs)
    def post(self,url,data=None,json=None,**kwargs):
        return self.request(url,'POST',json,data,**kwargs)

    def request(self,url,method,data=None,json=None,**kwargs):
        url=self.api_url+url
        if method == 'GET':
            return self.session.get(url,**kwargs)
        if method == 'POST':
            return self.session.post(url,data,json,**kwargs)



if __name__ == '__main__':
    url='http://47.107.232.149:18088/account/login'
    headers={
        'Content-Type':'application/x-www-form-urlencoded',
    }
    body={
        'name':'欧发超',
        'password':'888888',
    }
    res=requests.post(url=url,headers=headers,data=body)
    print(res.json())
