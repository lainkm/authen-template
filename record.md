# Record

## 认证系统

1.先用自带的django认证,使用Django自带的login和logout的视图就行，增加signup-view, 和用户身份信息-model

widget:Form属性，比如一个charfield默认对应一个html的textinput，如果想使用Textarea，可以使用
message = forms.CharField(widget=forms.Textarea)

自带的login默认的跳转界面通过settings里面设置

2.