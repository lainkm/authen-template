# django-authen(用户管理相关)

<b>clone到本地后：</b>

需要自己定义bbs/base_settings.py填入隐私配置信息

	# 第三方登陆
	GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
	GITHUB_CLIENTID = 'your lient_id'
	GITHUB_CLIENTSECRET = 'your lient_secret'
	GITHUB_CALLBACK = 'http://localhost:8001/oauth/github/'

	# 上传到cloudinay，需要注册
	CLOUD_NAME = 'yours'
	CLOUD_KEY = 'yours'
	CLOUD_SECRET = 'yours'

> 或者，手动改settings，写成环境变量 .env中读取<br>
或者，写成config.py，顺便写出不同环境的配置类..因为不用部署先就省了

## 解决如下功能

用户注册，登陆，重置密码，个人资料，邮箱注册（手机短信）

上传头像，第三方登陆如github，二维码登陆，邮箱验证

TODO：<br>
绑定多个社交网站<br>
除了github, weibo之外的第三方登陆<br>

### 用户注册方案：

#### 方案一：直接使用Django自带的用户认证

> 优点：快速建站
 
> 缺点：使用username和password认证方式，不支持email登陆(在django2.0里email不是unique，但django之前的版本email是unique)，用户资料的其他信息不能储存。

#### 方案二：在Django自带的用户认证的基础上进行重写

实例：[authen](https://github.com/lainkm/authen-template/tree/master/authen)

重写1：继承自AbstractUser类，在原有数据库表基础上添加额外字段(settings里增加AUTH_USER_MODEL)。修改user和email共同认证，重写authenticate方法(settings里增加Backend认证列表). login使用自带auth，重新写了register和pwreset

重写2：添加新类和原User类一对一(OneToOneField)关联，使用User.profile.birthday等可查询

> 优点：上面两种重写基本上能满足自己小网站的需求，实现了自定义email认证

> 缺点：管理者和用户共用同一张表，分开管理比较好

#### 方案三：使用第三方包，禁用管理后台/或开启/或后台也用第三方

（这里所有包的源码读一读就能明白，可以用来完善自己的）

TODO

> 优点：很多第三方包，对国内网站习惯进行了很好的支持，被人广泛使用的也很多

> 缺点：总可能有写东西是你不期望的

#### 方案四：自己写认证，连带着写后台

TODO

> 优点：自己写一整套，对于深入理解django也有好处；不同项目可复用

> 缺点：花时间造轮子，不如跳舞

### 用户头像方案

#### 方案一：存在本地media文件夹

实例：[]()

数据库字段使用ImageField，每个用户一个默认图片，前端直接上传文件，保存在服务器文件夹（根据日期等保存）

#### 方案二：存在云里

实例：[authen.views](https://github.com/lainkm/authen-template/blob/master/authen/views.py)

数据库字段使用CharField保存图片的url，每个用户使用一个默认图片，前端上传文件，保存在cloudinary

> 方案一，方案二：对第三方登陆，只要解析出avatar_url，将这个url保存在数据库即可。两个方案本质上没差，但是方案一是将图片保存在本地，所以用到ImageField和其他函数逻辑处理，方案二需要提前申请账号密码

#### 方案三：使用gravatar提供的头像关联唯一email

使用flask的时候使用过，不再复述。

#### 方案四：使用第三方认证包提供的处理

比如：<br>
django-allauth<br>
提供了很好的url

#### 方案五..

TODO


### 第三方登陆方案

#### 方案一：模拟oauth认证流程，

oauth2.0(开放授权)：互联网标准协议，获得储存在其他服务商的信息<br>
原理：<br>
user要通过github登陆client，<br>
client向user询问授权,<br>
user同意授权<br>
client告诉github已经拿到授权，<br>
github(认证服务器)验证授权无误，向client发放token(令牌)<br>
client拿到token，向github(资源服务器)申请获取资源<br>
github(资源服务器)确认token无误，同意给予资源<br>
（第三方认证服务器和资源服务器可以是同一个）<br>

几种模式：授权码模式，简化模式，密码模式，客户端模式<br>




实例：[oauth](https://github.com/lainkm/authen-template/tree/master/oauth)

1.首先在github上setting的开发者选项里找到添加oauth，填上服务器ip:port/域名/本地，创建，并在本页找到自己的client_id，和client_secret<br>
2.在自己的项目中settings里添加

	GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
	GITHUB_CLIENTID = 'your client_id'
	GITHUB_CLIENTSECRET = 'your client_secret'
	GITHUB_CALLBACK = 'http://localhost:8000/oauth/github/'  # 认证好之后返回的url

3.在urls里添加github_login，和github两个url，并在views里实现oauth逻辑，解析access_token得到email，username等信息填进数据库等步骤


#### 方案二：第三方包


### 邮箱验证(含异步)：

邮箱认证机制：
生成用户信息，并将用户is_active字段设置为False，验证成功改成True
根据填入的用户名或邮箱生成token，生成验证url：
> 最简单使用base64编码，也可以使用序列化的方法
发送验证邮箱
用户登陆
处理

#### 方案一：使用自带mail(很好了已经)

实例：

官网的栗子：

	from django.core.mail import send_mail
	 
	send_mail('Subject here', 'Here is the message.', 'from@example.com',
	    ['to@example.com'], fail_silently=False)

> 缺点：send_mail会建立一个连接，发送多个邮件用send_mass_mail，可以在只建立一个连接的情况下发多个邮件

#### 方案二：使用自带email+celery异步发送邮件

注册邮箱验证还需要发送一个邮件，如果管理员想全部的用户都发一封邮件，就没必要等待页面反应，使用异步

#### 方案三：使用自带的email+celery异步+定时使得未激活的邮箱失效





#### 方案四：自己写

### 二维码登陆：

扫描弹出的二维码，在手机上弹出授权，即可登陆