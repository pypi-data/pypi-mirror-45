from openhltest_client.base import Base


class AuthValue2(Base):
	"""Authentication Value 2.
	"""
	YANG_NAME = 'auth-value2'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Single": "single", "PatternType": "pattern-type", "PatternFormat": "pattern-format", "ValueList": "value-list"}

	def __init__(self, parent):
		super(AuthValue2, self).__init__(parent)

	@property
	def Increment(self):
		"""The values that make up the increment pattern

		Get an instance of the Increment class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.porttraffic.frames.ospfv2hello.authvalue2.increment.increment.Increment)
		"""
		from openhltest_client.openhltest.sessions.config.porttraffic.frames.ospfv2hello.authvalue2.increment.increment import Increment
		return Increment(self)._read()

	@property
	def Decrement(self):
		"""TBD

		Get an instance of the Decrement class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.porttraffic.frames.ospfv2hello.authvalue2.decrement.decrement.Decrement)
		"""
		from openhltest_client.openhltest.sessions.config.porttraffic.frames.ospfv2hello.authvalue2.decrement.decrement import Decrement
		return Decrement(self)._read()

	@property
	def Random(self):
		"""The repeatable random pattern.

		Get an instance of the Random class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.porttraffic.frames.ospfv2hello.authvalue2.random.random.Random)
		"""
		from openhltest_client.openhltest.sessions.config.porttraffic.frames.ospfv2hello.authvalue2.random.random import Random
		return Random(self)._read()

	@property
	def PatternType(self):
		"""The selected pattern from the possible pattern types.

		Getter Returns:
			SINGLE | INCREMENT | DECREMENT | RANDOM | VALUE_LIST

		Setter Allows:
			SINGLE | INCREMENT | DECREMENT | RANDOM | VALUE_LIST

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('pattern-type')
	@PatternType.setter
	def PatternType(self, value):
		return self._set_value('pattern-type', value)

	@property
	def PatternFormat(self):
		"""The format of the pattern.
		This will almost always be a regular expression.
		It is used to determine the validity of the values being set in the child leaf nodes of the pattern.

		Getter Returns:
			string
		"""
		return self._get_value('pattern-format')
	@PatternFormat.setter
	def PatternFormat(self, value):
		return self._set_value('pattern-format', value)

	@property
	def Single(self):
		"""The value of the single pattern

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('single')
	@Single.setter
	def Single(self, value):
		return self._set_value('single', value)

	@property
	def ValueList(self):
		"""The value list pattern takes a list of values that will be repeated if they do not meet or exceed the count

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('value-list')
	@ValueList.setter
	def ValueList(self, value):
		return self._set_value('value-list', value)

	def update(self, PatternType=None, PatternFormat=None, Single=None, ValueList=None):
		"""Update the current instance of the `auth-value2` resource

		Args:
			PatternType (enumeration): The selected pattern from the possible pattern types.
			PatternFormat (string): The format of the pattern.This will almost always be a regular expression.It is used to determine the validity of the values being set in the child leaf nodes of the pattern.
			Single (string): The value of the single pattern
			ValueList (string): The value list pattern takes a list of values that will be repeated if they do not meet or exceed the count
		"""
		return self._update(locals())

