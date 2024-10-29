import requests

from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

baidu_ak = 'xvG15kXT0PwKPvWvisfIKlx4X9tGpFve'


@app.route('/api/weather', methods=['POST'])
def list_baidu_weather():
    """
    获取指定地区的天气数据。
    ---
    parameters:
      - name: region_item
        in: body
        type: string
        default: ""
        example: {"region_item": "110101"}
        required: false
        description: 指定地区代码，默认获取每个省份地区的天气数据。
    
    responses:
      200:
        description: 指定地区的天气数据列表。
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 0
              description: 状态码，正常时返回0，异常时返回其他数字
            message:
              type: string
              example: "成功"
              description: 状态信息，正常时返回"成功"，异常时返回具体信息
            data:
              type: array
              items:
                type: object
                properties:
                  province:
                    type: string
                    example: "北京市"
                    description: 省份
                  city:
                    type: string
                    example: "北京市"
                    description: 城市
                  name:
                    type: string
                    example: "北京市"
                    description: 区县
                  temp:
                    type: number
                    example: 19
                    description: 实时温度，单位为℃
                  feels_like:
                    type: number
                    example: 19
                    description: 体感温度，单位为℃
                  rh:
                    type: number
                    example: 45
                    description: 相对湿度，单位为%
                  text:  
                    type: string
                    example: "晴"
                    description: 天气现象
                  uptime:
                    type: string
                    example: "20241029151500"
                    description: 更新时间
    """
    
    if request.json.get('region_item', ''):
        region_list = [request.json['region_item']]
    else:
        region_data = get_baidu_region('中国', 2)
        region_list = sorted([each['code'] for each in region_data])
        
    baidu_list = []
    for region in region_list:
        baidu_data = get_baidu_weather(region)
        if not baidu_data:
            continue

        baidu_list.append(baidu_data)
        
    result = {'code': 0, 'message': '成功', 'data': baidu_list}
    return jsonify(result)


@app.route('/api/region', methods=['POST'])
def list_baidu_region():
    """
    获取指定地区的下一级区域数据。
    ---
    parameters:
      - name: region_from
        in: body
        type: string
        default: "中国"
        example: {"region_from": "110100"}
        required: false
        description: 指定地区代码，默认获取中国所有省份的地区数据。
    
    responses:
      200:
        description: 指定地区的下一级区域数据列表。
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 0
              description: 状态码，正常时返回0，异常时返回其他数字
            message:
              type: string
              example: "成功"
              description: 状态信息，正常时返回"成功"，异常时返回具体信息
            data:
              type: array
              items:
                type: object
                properties:
                  code:
                    type: string
                    example: "110101"
                    description: 下一级地区代码
                  name:
                    type: string
                    example: "东城区"
                    description: 下一级地区名称
    """
    
    region_from = request.json.get('region_from', '中国')
    region_list = sorted(get_baidu_region(region_from, 1), key=lambda x: x['code'])
    result = {'code': 0, 'message': '成功', 'data': region_list}
    return jsonify(result)


def get_baidu_weather(baidu_region):
    baidu_url = 'https://api.map.baidu.com/weather/v1/'
    baidu_param = {
        'district_id': baidu_region,
        'data_type': 'now',
        'ak': baidu_ak,
    }
    
    baidu_data = requests.get(baidu_url, baidu_param).json()
    if baidu_data['status'] != 0:
        return {}
    
    result = {**baidu_data['result']['location'], **baidu_data['result']['now']}
    return result


def get_baidu_region(baidu_from, baidu_sub):
    baidu_url = 'https://api.map.baidu.com/api_region_search/v1/'
    baidu_param = {
        'keyword': baidu_from, 
        'sub_admin': baidu_sub, 
        'extensions_code': 1,
        'ak': baidu_ak, 
    }

    baidu_data = requests.get(baidu_url, baidu_param).json()
    if baidu_data['status'] != 0:
        return {}
    
    baidu_list = baidu_data['districts'][0]['districts']
    if baidu_sub == 1:
        result = [{'code': each['code'], 'name': each['name']} for each in baidu_list]
    else:
        result = [each['districts'][0] for each in baidu_list]
        
    return result


if __name__ == '__main__':
    app.run(debug=True)