from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import time
import sys
import json
from config import SecretId, SecretKey, VIP
def clone_load_balancer(clb_id, vip):
    from tencentcloud.clb.v20180317 import clb_client, models
    request_id = ""
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(SecretId, SecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "clb.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = clb_client.ClbClient(cred, "ap-shanghai", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.CloneLoadBalancerRequest()
        params = {
            "LoadBalancerId": clb_id, # 被克隆的 CLB ID
            "Vip" : vip, # 指定 Vip
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个CloneLoadBalancerResponse的实例，与请求对象对应
        resp = client.CloneLoadBalancer(req)
        # 输出json格式的字符串回包
        # print(resp.to_json_string())
        resp_data_obj = json.loads(resp.to_json_string())
        request_id = resp_data_obj['RequestId']

    except TencentCloudSDKException as err:
        print(err)

    return request_id

def get_task_result(clb_id):
    from tencentcloud.clb.v20180317 import clb_client, models
    task_data_obj = {}
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(SecretId, SecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "clb.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = clb_client.ClbClient(cred, "ap-shanghai", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.CloneLoadBalancerRequest()
        params = {
            "LoadBalancerId": clb_id,
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个CloneLoadBalancerResponse的实例，与请求对象对应
        resp = client.CloneLoadBalancer(req)
        # 输出json格式的字符串回包
        # print(resp.to_json_string())
        task_data_obj = json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)

    return task_data_obj


def main():
    clb_id = sys.argv[1]
    request_id = clone_load_balancer(clb_id, VIP)
    clone_clb_id = ""
    # 根据克隆CLB返回的request_id, 间隔1s轮询任务结果
    while True and request_id != "":
        task_data_obj = get_task_result(request_id)
        if task_data_obj.has("LoadBalancerIds") and task_data_obj["LoadBalancerIds"] is not None:
            clone_clb_id = task_data_obj["LoadBalancerIds"][0]
            break
        time.sleep(1)
    print("rollback clb id is %s" % clone_clb_id)
    

if __name__ == '__main__':
    main()
