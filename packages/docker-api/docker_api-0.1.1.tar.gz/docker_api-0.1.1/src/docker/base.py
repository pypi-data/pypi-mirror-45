#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Docker API
# Copyright (c) 2008-2019 Hive Solutions Lda.
#
# This file is part of Hive Docker API.
#
# Hive Docker API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Docker API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Docker API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import base64

import appier

from . import container

BASE_URL = "http://localhost:2375/"

class API(
    appier.API,
    container.ContainerAPI
):

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("DOCKER_BASE_URL", BASE_URL)
        self.username = appier.conf("DOCKER_USERNAME", None)
        self.password = appier.conf("DOCKER_PASSWORD", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.username = kwargs.get("username", self.username)
        self.password = kwargs.get("password", self.password)

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        auth = kwargs.pop("auth", True)
        if auth: headers["Authorization"] = self.get_authorization()

    def get_authorization(self):
        if not self.username or not self.password: None
        payload = "%s:%s" % (self.username, self.password)
        payload = appier.legacy.bytes(payload)
        authorization = base64.b64encode(payload)
        authorization = appier.legacy.str(authorization)
        return "Basic %s" % authorization
