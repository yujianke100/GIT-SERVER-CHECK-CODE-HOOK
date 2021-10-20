# GIT-SERVER-CHECK-CODE-HOOK
GIT钩子，可在服务器端确认更新的代码是否合法，并发送邮件提醒

## 使用方式：
1. 根据需求修改`pre-receive`,主要是仓库路径。
2. 将`pre-receive`,文件存放于服务器端的仓库文件夹下的`./.git/hooks`下。
3. 将`check_code.py`文件存放于`~`目录下

##关于python

使用的是python3，若需要使用2，请自行修改代码。

python的用途即为判断代码合法性并在发现不合法时发送邮件。可根据自己的需求修改代码。

## 若需要阻止不合法的代码上传，可将`pre-receive`中73行的`exit 0`改为`exit 1`
