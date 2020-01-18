# 软件系统

## 系统架构

Flask + MongoDB + Vue.js

希望大家在安装编程语言环境的时候，不要直接安装，而是采用版本管理工具进行安装，例如
- pipenv(python)
- nvm(nodejs)
- jenv(java)
- phpenv(php)  
...

### 后端参考资料

[Flask](https://flask.palletsprojects.com/en/0.12.x/)  
[Flask-Login](https://flask-login.readthedocs.io/en/latest/)  
[Flask-Script](https://flask-script.readthedocs.io/en/latest/)  
[Flask-Blueprints](https://flask.palletsprojects.com/en/0.12.x/blueprints/)  
[Flask-MongoEngine](https://flask-mongoengine.readthedocs.io/en/latest/)  
[MongoEngine](http://docs.mongoengine.org/)

### 前端参考资料
[Vue](https://cn.vuejs.org/v2/guide/index.html)  
[Vuex](https://vuex.vuejs.org/zh/)  
[Vue-Router](https://router.vuejs.org/zh/)  
[axios](http://www.axios-js.com/)  
[VeeValidate](https://logaretm.github.io/vee-validate/)  
[Element UI](https://element.eleme.io/#/zh-CN/component/installation)  
[Babel](https://www.babeljs.cn/docs/)  
[Webpack](https://www.webpackjs.com/concepts/)  
[Scss](https://www.sass.hk/docs/)  
[PostCSS](https://www.postcss.com.cn/)


### 后端

### 环境搭建
1. 安装启动MongoDB, 可选项：
- 本机安装MongoDB并启动
- 安装 [Docker]()， 进入项目目录执行 docker-compose up -d 即可

> [Docker For Mac](https://docs.docker.com/docker-for-mac/install/)  
[Docker For Linux](https://docs.docker.com/install/linux/docker-ce/centos/)  
[Docker For Windows](https://docs.docker.com/docker-for-windows/install/)

2. 安装pipenv [参考](https://pipenv.kennethreitz.org/en/latest/install/#installing-pipenv) 或自行百度  
> 能用命令行在任意目录运行 pipenv 命令，表示安装成功

3. 运行项目

进入 `${project}/src/backend` 目录下  
```bash
pipenv --three # 初始化一个 python3 的虚拟环境
pipenv shell # 进入虚拟环境
pipenv install # 只有第一次运行程序才需要执行，类似于nodejs的 npm install
# 运行程序，二选一
python run.py
FLASK_APP=app flask run
```

> 本地安装的MongoDB需要修改配置文件，以链接本地的MongoDB，配置文件位置`src/backend/app/config.py`

### 项目目录结构

```
- backend
  - app/            # flask app 模块
  - auth/           # 访问控制代码
  - models/         # 数据模型定义
  - views/          # API接口定义
    - form/         # 表单校验类定义
    - account.py        # 用户管理相关API
    - deivce.py         # 设备管理相关API
  - run.py          # 程序入口
```

## 前端

### 环境搭建

1. 安装 nvm [参考](https://github.com/nvm-sh/nvm/blob/master/README.md)
> 能用命令行在任意目录运行 nvm 命令，表示安装成功

2. 安装node环境  
> 本项目使用的node环境是 10.16.3
```bash
nvm install 10.16.3
nvm use 10.16.3
node -v
npm install -g yarn
```

3. 运行项目，进入`${project}/src/frontend`目录下，执行
```bash
yarn
yarn run serve
```
然后浏览器访问 `http://localhost:8080/#/`

### 目录结构

```
- frontend
  - public/         # 静态文件
  - src/            # js 代码
    - assets/         # 资源文件
    - components/     # vue 组件
    - libs/           # 第三方库
    - pages/          # 页面
    - plugins/        # 插件
    - store/          # vue store
    - utils/          # 工具方法目录
    - App.vue         # root vue
    - main.js         # 程序入口
```

## 测试及部署

### 生产环境部署

1. 上传代码

```bash
scp -r adsms root@ip:/root
```

2. 安装docker
```bash
yum update
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io
yum install -y docker-compose
systemctl enable docker # 将docker设置为开机自启
systemctl start docker # 启动docker

# 换源
sudo tee /etc/docker/daemon.json <<-'EOF'
{
"registry-mirrors": ["https://brgmc2ov.mirror.aliyuncs.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker
```

3. 构建项目

   进入项目环境，执行./build.sh*  
     *windows上传的文件没有访问权限，需要添加权限
```bash
chmod +x ./build.sh
./build.sh
docker-compose build
docker-compose up -d

docker-compose up -d --build # 一步到位，等价于上面两条命令
```

4. 执行初始化脚本
```python
docker exec -it backend bash
flask shell

from models.user import User
from models.setting import Setting

user = User()
user.username = 'admin'
user.email = 'admin@qq.com'
user.author_type = 1
user.author_editable = False
user.deletable = False
user.password = 'Abc123__'
user.save()

if Setting.objects().first() is None:
    Setting(update_user=user.id).save()

```

5. 运行维护
```bash
# 查看运行日志
docker-compose logs -f # 查看所有运行日志
docker-compose logs -f backend # 查看Backend运行日志
docker-compose logs -f nginx   # 查看Nginx运行日志
docker-compose logs -f mongodb # 查看MongoDB运行日志

# 停止项目
docker-compose stop # 停止所有服务
docker-compose stop backend # 只停止Backend服务
docker-compose stop nginx   # 只停止Nginx服务
docker-compose stop mongodb # 只停止MongoDB服务

# 启动项目
docker-compose start # 启动所有服务
docker-compose start backend # 只启动Backend服务
docker-compose start nginx   # 只启动Nginx服务
docker-compose start mongodb # 只启动MongoDB服务

# 重启项目
docker-compose restart # 重启所有服务
docker-compose restart backend # 只重启Backend服务
docker-compose restart nginx   # 只重启Nginx服务
docker-compose restart mongodb # 只重启MongoDB服务

# 卸载项目
docker-compose stop && docker-compose rm -f
```
