from openhltest_client.base import Base


class CustomImix(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/config/device-traffic/frame-length/custom-imix resource.
	"""
	YANG_NAME = 'custom-imix'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"Name": "name", "Weight": "weight", "Size": "size"}

	def __init__(self, parent):
		super(CustomImix, self).__init__(parent)

	@property
	def Name(self):
		"""TBD

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('name')

	@property
	def Size(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('size')
	@Size.setter
	def Size(self, value):
		return self._set_value('size', value)

	@property
	def Weight(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('weight')
	@Weight.setter
	def Weight(self, value):
		return self._set_value('weight', value)

	def create(self, Name, Size=None, Weight=None):
		"""Create an instance of the `custom-imix` resource

		Args:
			Name (string): TBD
			Size (int32): TBD
			Weight (int32): TBD
		"""
		return self._create(locals())

	def read(self, Name=None):
		"""Get `custom-imix` resource(s). Returns all resources from the server if `Name` is not specified

		"""
		return self._read(Name)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `custom-imix` resource

		"""
		return self._delete()

	def update(self, Size=None, Weight=None):
		"""Update the current instance of the `custom-imix` resource

		Args:
			Size (int32): TBD
			Weight (int32): TBD
		"""
		return self._update(locals())

