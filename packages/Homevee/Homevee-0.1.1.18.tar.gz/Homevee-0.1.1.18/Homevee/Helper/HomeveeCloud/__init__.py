import json

from Homevee.Helper.HomeveeCloud.CloudAPI import CloudAPI
from Homevee.Helper.HomeveeCloud.Exception import APINotAuthenticatedException, APIErrorException


class HomeveeCloudWrapper():
    def __init__(self, remote_id=None, access_token=None):
        self.remote_id = remote_id
        self.access_token = access_token

        self.cloud_api = CloudAPI(remote_id, access_token)

    def is_premium(self):
        response = self.cloud_api.do_get("/ispremium/"+self.remote_id, {})

        data = self.check_response(response)

        return data['is_premium']

    def set_ip(self, ip):
        response = self.cloud_api.do_put("/setlocalip/"+self.remote_id, {'ip': ip})
        data = self.check_response(response)
        return data['status']

    def set_cert(self, cert):
        response = self.cloud_api.do_put("/setlocalcert/"+self.remote_id, {'cert': cert})
        data = self.check_response(response)
        return data['status']

    def get_ip(self):
        response = self.cloud_api.do_get("/getlocalip/"+self.remote_id, {})
        data = self.check_response(response)
        return data['local_ip']

    def get_cert(self):
        response = self.cloud_api.do_get("/getlocalcert/"+self.remote_id, {})
        data = self.check_response(response)
        return data['local_cert']

    def get_used_cloud(self):
        response = self.cloud_api.do_get("/get_used_cloud/"+self.remote_id, {})
        data = self.check_response(response)
        return data['cloud']

    def check_response(self, response):
        if response.status_code == 401:
            raise APINotAuthenticatedException("Invalid credentials given")

        #print(response.get_dict())

        if response.status_code != 200:
            raise APIErrorException("API-Call not successful")

        return json.loads(response.response)