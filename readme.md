# 项目说明 (简易天气查询应用-后端)

### 在线示例：https://weather.huahuohui.cn/front

### 接口文档：https://weather.huahuohui.cn/apidocs

### 前端代码：https://github.com/Volcano-we/weather-web

<br>

# 安装部署

### 1. 设置虚拟环境

+ 创建虚拟环境：python -m venv ~/venv/weather_env

+ 激活虚拟环境：source ~/venv/weather_env/bin/activate

### 2. 安装依赖包

+ pip install -r require.txt

### 3. 配置运行环境

+ 配置 nginx，参考 nginx.conf

+ 配置 supervisor，参考 supervisor.conf

### 4. 启动项目运行

+ 重载 nginx：sudo service nginx reload 或 sudo nginx -s reload

+ 重载 supervisor：在项目目录下执行 source reload.sh