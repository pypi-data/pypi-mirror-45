import json
import requests as req


class Cspd_msg91:
    def __init__(self,apikey):
        self.apikey = apikey
   
    def send(self,route,sender,phone,msg):
        url = 'http://api.msg91.com/api/sendhttp.php'
        params = {
         'route':route,
         'sender':sender,
         'mobiles':phone,
         'authkey':self.apikey,
         'message':msg,
         'response':'json'
        }
        res = req.get(url,params=params)
        return json.loads( res.content )
    
    def send_otp(self,sender,phone,msg,otp_length=6,otp_expiry=10):
        url = 'http://control.msg91.com/api/sendotp.php'
        params = {
         'sender':sender,
         'mobiles':phone,
         'authkey':self.apikey,
         'message':msg,
         'otp_length':otp_length,
         'otp_expiry':otp_expiry
        }
        res = req.post(url,params=params)
        return json.loads( res.content )

    def verify_otp(self,phone,otp):
        url = 'https://control.msg91.com/api/verifyRequestOTP.php'
        params = {
         'authkey':self.apikey,
         'mobile':phone,
         'otp':otp,
        }
        res = req.post(url,params=params)
        return json.loads( res.content )

    def resend_otp(self,phone,retrytype="text"):
        url = 'http://control.msg91.com/api/retryotp.php?retrytype=text'
        params = {
         'authkey':self.apikey,
         'mobile':phone,
         'retrytype':retrytype,
        }
        res = req.post(url,params=params)
        return json.loads( res.content )
