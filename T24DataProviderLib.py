# ==========================================
# Company:  Standard Bank Mozambique
# Created by: DXP QA
# Date:   11 February 2022
# ==========================================
from robot.api.deco import keyword, library

from .T24Client import T24Client


@library
class T24DataProviderLib:
    """DXP T24 Data Provider Library."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @keyword("Execute Routine")
    def execute_routine(self, address, configFile, routineName: str, inParameters: list):
        client = T24Client()
        client.init_client(address, config=configFile)
        response = client.execute_routine(
            routineName, inParameters)
        return response

    @keyword("Execute OFS")
    def execute_ofs(self, address, configFile, ofs_command):
        client = T24Client()
        client.init_client(address, config=configFile)
        response = client.execute_ofs(
            ofs_command)
        return response
