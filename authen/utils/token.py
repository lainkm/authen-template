from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import re

class Token():

	def __init__(self,security_key):
		self.security_key = security_key # SECRET_KEY
		self.salt = base64.b64encode(security_key.encode()) # base64加密
	
	def generate_validate_token(self,username):
		serializer = utsr(self.security_key) 
		return serializer.dumps(username,self.salt) # 使用用户名加盐生成一个令牌
	
	def confirm_validate_token(self, token, expiration=3600):   # 令牌没过期之前验证，就返回用户名
		serializer = utsr(self.security_key)
		return serializer.loads(token,
			salt=self.salt,
			max_age=expiration)