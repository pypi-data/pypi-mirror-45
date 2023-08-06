# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPpaOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import ResourceClient


class SasLogicalJbods(object):
    """
    SAS Logical JBODs API client.

    Note:
        This resource is only available on HPE Synergy

    """
    URI = '/rest/sas-logical-jbods'
    DRIVES_PATH = '/drives'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of SAS logical JBODs based on optional sorting and filtering and constrained by
        start and count parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of all SAS logical JBODs.
        """
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets the specified SAS logical JBODs resource by ID or by URI.

        Args:
            id_or_uri: Can be either the SAS logical JBOD ID or the SAS logical JBOD URI.

        Returns:
            dict: The SAS logical JBOD.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def get_by(self, field, value):
        """
        Gets all SAS Logical JBODs that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of SAS Logical JBODs.
        """
        return self._client.get_by(field, value)

    def get_drives(self, id_or_uri):
        """
        Gets the list of drives allocated to this SAS logical JBOD.

        Args:
            id_or_uri: Can be either the SAS logical JBOD ID or the SAS logical JBOD URI.

        Returns:
            list: A list of Drives
        """
        uri = self._client.build_uri(id_or_uri=id_or_uri) + self.DRIVES_PATH
        return self._client.get(id_or_uri=uri)
