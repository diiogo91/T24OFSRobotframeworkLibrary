# ==========================================
# Company:  Standard Bank Mozambique
# Created by: DXP QA
# Date:   14 June 2022
# ==========================================

import base64
import json
import requests
import configparser as ConfigParser
from robot.api import logger

from .T24ResponseWorker import T24ResponseWorker

headers = {
    'authorization': '',
    'cache-control': 'no-cache',
    'Content-Type': 'application/json;'
}


class T24Client:

    """
     This is a T24 Client Objects that allows to execute OFS and Routine Instructions on a T24 TAFJ Environment.
     Preconditions: This Client is dependant of the TAFJRestServices.war/TAFJJEE_EAR.ear APIs and must be
     deployed & enabled on the T24 TAFJ JBoss application server or related.
     Notes:
         1. This is not compatible with T24 TAFC.
         2. In case of struggling with security permissions on API requests locate and comment/disable the security
         session on the TAFJRestservices.war web.xml file.
                Example:
                    <!-- <security-constraint>
                            <web-resource-collection>
                                <web-resource-name>TAFJRestServices</web-resource-name>
                                <url-pattern>/resources/*</url-pattern>
                            </web-resource-collection>
                            <auth-constraint>
                                <role-name>TAFJAdmin</role-name>
                            </auth-constraint>
                        </security-constraint>
                        <security-role>
                            <role-name>TAFJAdmin</role-name>
                        </security-role>
                        <login-config>
                            <auth-method>BASIC</auth-method>
                            <realm-name>TAFJRealm</realm-name>
                        </login-config> -->
    """

    def __init__(self):
        self.address = None
        self.username = None
        self.password = None
        self.headers = {}

    def init_client(self, address, config=None):
        t24Config = ConfigParser.ConfigParser()
        t24Config.read([config])
        self.address = address
        if t24Config:
            self.username = None or t24Config.get('default', 'tUsername')
            self.password = None or t24Config.get('default', 'tPassword')
            if self.username and self.password:
                self.headers = {
                    "Authorization": "Basic {}".format(
                        base64.b64encode(bytes(f"{self.username}:{self.password}", "utf-8")).decode("ascii")
                    )
                }

    def execute_ofs(self, ofsRequest: str, first_or_all: bool = False):
        """
        Parameter example:
            "ofsRequest": "ENQUIRY.SELECT,,ENQUIRYUSER01/USERXXX/COMPANYZZZZ,CUSTOMER,@ID:EQ=232344"
            "first_or_all": false: will return only the first result | true: will return list of results
        """
        ofs_endpoint = "/TAFJRestServices/resources/ofs"
        payload = {
            "ofsRequest": ofsRequest
        }
        response = requests.post(self.address + ofs_endpoint, headers=self.headers,
                                 json=payload)
        logger.console("- Response Status Code: " + str(response.status_code))
        logger.console("- Response Elapsed Time: " + str(response.elapsed))
        json_object = json.loads(response.text)
        t24resp = None
        if json_object:
            t24util = T24ResponseWorker(json_object["ofsResponse"])
            t24resp = t24util.get_response_list()
        if (first_or_all and len(t24resp) > 0) or len(t24resp) == 1:
            return t24resp[0]
        return t24resp

    def execute_routine(self, routinename: str, inparameters: list):
        """
            Parameter example:
               "routinename" : "EXCHRATE",
               "inparameters" : ["1", "CHF", "500", "GBP", "", "", "", "", "", ""]
         """
        logger.info("-- Executing Routine on T24 Tafj Server")
        routine_endpoint = "/TAFJRestServices/resources/callAt"
        payload = {
            "routineName": routinename,
            "inParameters": inparameters
        }
        response = requests.post(self.address + routine_endpoint, headers=headers,
                                 json=payload)
        logger.info("Response Status Code: " + str(response.status_code))
        return response.text
