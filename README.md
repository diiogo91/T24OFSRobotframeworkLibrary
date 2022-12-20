# T24 OFS Robotframework Client Library

    This is a T24 Client that allows to execute OFS and Routine Instructions on a T24 TAFJ Environment.
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