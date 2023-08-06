import requests
import json



def login():
    data = {"username": "admin",
            "password": "1qaz2wsx"
            }

    headers = {'Content-Type': 'application/json'}  ## headers中添加上content-type这个参数，指定为json格式
    response = requests.post(url='https://test-hechun.cloud.sensorsdata.cn/api/auth/login?project=yuejianzhong',
                             headers=headers,
                             data=json.dumps(data))  ## post的时候，将data字典形式的参数用json包转换成json格式。
    return response

    # print(response.json())
    # json = json.dumps(response.text)
    # print('\n')
    # print(response.text)

def saapi():
    data2 = {"measures": [{"event_name": "$AppStart", "aggregator": "unique"}], "unit": "day", "sampling_factor": 64,
             "axis_config": {"isNormalize": False, "left": [], "right": []}, "from_date": "2019-03-19",
             "to_date": "2019-03-25", "tType": "n", "ratio": "n", "approx": False, "by_fields": [], "filter": {},
             "detail_and_rollup": True, "request_id": "1553596932966:761148", "use_cache": True}

    headers = {'Content-Type': 'application/json'}  ## headers中添加上content-type这个参数，指定为json格式
    response = requests.post(
        url='https://test-hechun.cloud.sensorsdata.cn/api/events/report?token=570cff04c9bc7b802d11abccd2035bb558e8b5ec221943c1e35b10ec269caed0&project=yuejianzhong',
        headers=headers,
        data=json.dumps(data2))
    return response
    # print(response.json())
    # json = json.dumps(response.text)
    # print(response.status_code)
    # print('\n')
    #
    # print(response.text)

if __name__ == '__main__':
    re = login()
    print(re.text)
    print('\n')
    re1 = saapi()
    print(re1.text)