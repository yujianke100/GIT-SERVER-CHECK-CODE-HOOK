# GIT-SERVER-CHECK-CODE-HOOK
GIT钩子，可在服务器端确认更新的代码是否合法，并发送邮件提醒

## 使用方式：
1. 根据需求修改`pre-receive`,主要是临时目录路径。
2. 将`pre-receive`,文件存放于服务器端的仓库文件夹下的`./.git/hooks`下。
3. 将`check_code.py`文件存放于`~`目录下

## gitlab使用：
gitlab钩子[官方文档](https://docs.gitlab.com/ee/administration/server_hooks.html)。
1. 更改配置文件`/etc/gitlab/gitlab.rb`中的`gitlab_shell['custom_hooks_dir']`，默认路径为`/var/opt/gitlab/gitaly/custom_hooks`。注意启用后reload并restart：
```
sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart
```
3. 建立上述路径，并在该路径下创建`pre-receive.d`。
4. 根据要求修改`pre-receive`文件，主要是修改所需匹配的分支名称：
```
while read oldVersion newVersion branch; do
    # 只对main分支做检查
    result=$(echo ${branch}| grep "main")
```
以及python脚本路径。
5. 在上一步设置的路径下放置python脚本，并修改邮箱信息。需要时可修改判断逻辑。当python使用sys.exit(1)时，将返回脚本失败结果，脚本可以使用exit 1终止更新操作。
6. 注意文件夹和脚本权限。
## 关于python

使用的是python3，若需要使用2，请自行修改代码。

python的用途即为判断代码合法性并在发现不合法时发送邮件。可根据自己的需求修改代码。

### 若需要阻止不合法的代码上传，可将`pre-receive`中73行的`exit 0`改为`exit 1`
