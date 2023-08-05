# Copyright 1997 - 2018 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class StartRate(Base):
	"""The StartRate class encapsulates a required startRate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the StartRate property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'startRate'

	def __init__(self, parent):
		super(StartRate, self).__init__(parent)

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def Enabled(self):
		"""Enabled

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enabled')

	@property
	def Interval(self):
		"""The time interval in milliseconds during which the rate is calculated(rate = count/interval)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interval')

	@property
	def Rate(self):
		"""Number of times an action is triggered per time interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rate')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	@property
	def ScaleMode(self):
		"""Indicates whether the control is specified per port or per device group.

		Returns:
			str(deviceGroup|port)
		"""
		return self._get_attribute('scaleMode')
	@ScaleMode.setter
	def ScaleMode(self, value):
		self._set_attribute('scaleMode', value)

	def get_device_ids(self, PortNames=None, Enabled=None, Interval=None, Rate=None):
		"""Base class infrastructure that gets a list of startRate device ids encapsulated by this object.

		Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

		Args:
			PortNames (str): optional regex of port names
			Enabled (str): optional regex of enabled
			Interval (str): optional regex of interval
			Rate (str): optional regex of rate

		Returns:
			list(int): A list of device ids that meets the regex criteria provided in the method parameters

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._get_ngpf_device_ids(locals())

	def FetchAndUpdateConfigFromCloud(self, *args, **kwargs):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		fetchAndUpdateConfigFromCloud(Mode:string)
			Args:
				args[0] is Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		payload = { "Arg1": self.href }
		for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
		for item in kwargs.items(): payload[item[0]] = item[1]
		return self._execute('fetchAndUpdateConfigFromCloud', payload=payload, response_object=None)
