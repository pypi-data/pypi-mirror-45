from openhltest_client.base import Base


class FrameLength(Base):
	"""TBD
	"""
	YANG_NAME = 'frame-length'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Fixed": "fixed", "Imix": "imix", "LengthType": "length-type"}

	def __init__(self, parent):
		super(FrameLength, self).__init__(parent)

	@property
	def Random(self):
		"""Random frame size options

		Get an instance of the Random class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicetraffic.framelength.random.random.Random)
		"""
		from openhltest_client.openhltest.sessions.config.devicetraffic.framelength.random.random import Random
		return Random(self)._read()

	@property
	def Increment(self):
		"""TBD

		Get an instance of the Increment class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicetraffic.framelength.increment.increment.Increment)
		"""
		from openhltest_client.openhltest.sessions.config.devicetraffic.framelength.increment.increment import Increment
		return Increment(self)._read()

	@property
	def CustomImix(self):
		"""TBD

		Get an instance of the CustomImix class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicetraffic.framelength.customimix.customimix.CustomImix)
		"""
		from openhltest_client.openhltest.sessions.config.devicetraffic.framelength.customimix.customimix import CustomImix
		return CustomImix(self)

	@property
	def QuadGaussian(self):
		"""TBD

		Get an instance of the QuadGaussian class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicetraffic.framelength.quadgaussian.quadgaussian.QuadGaussian)
		"""
		from openhltest_client.openhltest.sessions.config.devicetraffic.framelength.quadgaussian.quadgaussian import QuadGaussian
		return QuadGaussian(self)

	@property
	def LengthType(self):
		"""TBD

		Getter Returns:
			FIXED | INCREMENTAL | RANDOM | AUTO | IMIX | CUSTOM_IMIX | QUAD_GAUSSIAN

		Setter Allows:
			FIXED | INCREMENTAL | RANDOM | AUTO | IMIX | CUSTOM_IMIX | QUAD_GAUSSIAN

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('length-type')
	@LengthType.setter
	def LengthType(self, value):
		return self._set_value('length-type', value)

	@property
	def Fixed(self):
		"""Fixed value for frame length

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('fixed')
	@Fixed.setter
	def Fixed(self, value):
		return self._set_value('fixed', value)

	@property
	def Imix(self):
		"""TBD

		Getter Returns:
			CISCO | IMIX | IPSEC_IMIX | IPV6_IMIX | RPR_QUAR | RPR_TRI | STANDARD_IMIX | TCP_IMIX | TOLLY

		Setter Allows:
			CISCO | IMIX | IPSEC_IMIX | IPV6_IMIX | RPR_QUAR | RPR_TRI | STANDARD_IMIX | TCP_IMIX | TOLLY

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('imix')
	@Imix.setter
	def Imix(self, value):
		return self._set_value('imix', value)

	def update(self, LengthType=None, Fixed=None, Imix=None):
		"""Update the current instance of the `frame-length` resource

		Args:
			LengthType (enumeration): TBD
			Fixed (int32): Fixed value for frame length
			Imix (enumeration): TBD
		"""
		return self._update(locals())

