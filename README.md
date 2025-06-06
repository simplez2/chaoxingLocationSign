# chaoxingLocationSign
这是用于针对超星学习通定位签到的一套python代码，参考原作者仓库地址[https://github.com/cxOrz/chaoxing-sign-cli], 仅限于用于学习网络请求的接收和发送。

# 1.项目简介

主要用于<u>超星学习通</u>**定位签到**的python代码

# 2.项目下载

在使用代码之前，请确保已经下载并安装了**python解释器**，并且可以通过**pip**进行包的安装，详细细节请上网自行搜索。

同时，请确保已经安装了以下的python包，如果没有，可执行下列命令进行安装

```bash
pip install requests pycryptodome Flask
```

## 2.1.使用git进行下载

打开终端执行下列命令将代码拷贝到本地

```
git clone https://github.com/alextomdog/chaoxingLocationSign.git
```

进入项目目录

```
cd ./chaoxingLocationSign
```

## 2.2.通用方式下载

通过点击左上角的`code`下载其压缩包，然后进行解压

# 3.使用方式

## 3.1.配置

在`location_sign.py`中修改下列参数进行配置

> 用户登录配置

```
username = "18888888888"  # 手机号
password = "**********"  # 密码
```

> 坐标地理位置配置

请使用坐标拾取器获得地理位置的经度纬度，当前使用的是<u>百度坐标拾取器</u>，如下：

https://api.map.baidu.com/lbsapi/getpoint/

将下列内容替换为自己拾取的坐标的地址

```
location_geography = '104.19107,30.827562'
```

> 定位地址名配置

请在学习通中找到已经进行过定位签到的`签到`, 然后查看这个签到的详细信息，其中包含**地址名称信息**，请复制这个地址，然后对下列地址名称进行替换

*注意：签到地址名字是显示在教师端和学生端地址信息名字的一种标识*

```
address_name = "中国四川省成都市xxxxxx"
```

此外，脚本也可以从环境变量读取这些配置，并支持通过 `COURSE_INDEX` 指定课程序号实现无交互运行：

```bash
export USERNAME=18888888888
export PASSWORD=**********
export LOCATION_GEOGRAPHY="104.19107,30.827562"
export ADDRESS_NAME="中国四川省成都市xxxxxx"
# 自动选择第一门课程
export COURSE_INDEX=1
python location_sign.py
```

## 3.2.运行程序

进入到项目根目录，然后执行python脚本

```
python ./location_sign.py
```

将会弹出以下内容，然后按照内容提示输入签到的课程序号，将针对该课程进行定位签到

![image-20240926203942120](README.assets/image-20240926203942120.png)

## 3.3.Docker运行

如果你在服务器上使用Docker，也可以通过构建容器来运行此脚本。

首先在项目根目录构建镜像：

```bash
docker build -t chaoxing-sign .
```

然后以环境变量方式传入账号信息和签到配置并启动容器：

```bash
docker run --rm -it \
  -e USERNAME=18888888888 \
  -e PASSWORD=********** \
  -e LOCATION_GEOGRAPHY="104.19107,30.827562" \
  -e ADDRESS_NAME="中国四川省成都市xxxxxx" \
  chaoxing-sign
```

环境变量会覆盖`location_sign.py`中对应的默认参数，方便在不同环境中部署。

### 3.4. Web 界面

项目新增了基于 Flask 的简单 Web 界面 `webapp.py`，运行后可以在浏览器中完成登录与签到操作：

```bash
pip install Flask
python webapp.py
```

在 Docker 中启动 Web 界面：

```bash
docker run --rm -p 5000:5000 chaoxing-sign python webapp.py
```

浏览器访问 `http://localhost:5000` 即可使用图形界面进行签到。



