from openhltest_client.base import Base


class Ospfv2(Base):
	"""TBD
	"""
	YANG_NAME = 'ospfv2'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {}

	def __init__(self, parent):
		super(Ospfv2, self).__init__(parent)

	@property
	def RouterId(self):
		"""Router ID.

		Get an instance of the RouterId class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.routerid.routerid.RouterId)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.routerid.routerid import RouterId
		return RouterId(self)._read()

	@property
	def AreaId(self):
		"""IP address indicating the area to which the emulated router belongs.

		Get an instance of the AreaId class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.areaid.areaid.AreaId)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.areaid.areaid import AreaId
		return AreaId(self)._read()

	@property
	def NetworkType(self):
		"""This setting to override the physical link type to emulate a broadcast
		           adjacency over POS, or a point-to-point adjacency over Ethernet
		           NATIVE    : use the adjacency implied by the port-type
		           BROADCAST : Broadcast adjacency
		           P2P       : P2P (point-to-point) adjacency

		Get an instance of the NetworkType class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.networktype.networktype.NetworkType)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.networktype.networktype import NetworkType
		return NetworkType(self)._read()

	@property
	def RouterPriority(self):
		"""Router priority of the emulated router. Set the router priority to a higher
		           or lower value to influence the DR and BDR selection process.

		Get an instance of the RouterPriority class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.routerpriority.routerpriority.RouterPriority)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.routerpriority.routerpriority import RouterPriority
		return RouterPriority(self)._read()

	@property
	def InterfaceCost(self):
		"""Cost of the interface connecting the emulated router to the neighbor DUT router.

		Get an instance of the InterfaceCost class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.interfacecost.interfacecost.InterfaceCost)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.interfacecost.interfacecost import InterfaceCost
		return InterfaceCost(self)._read()

	@property
	def HelloInterval(self):
		"""Time interval (in seconds) used by the emulated routers to pace Hello packet
		           transmissions.

		Get an instance of the HelloInterval class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.hellointerval.hellointerval.HelloInterval)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.hellointerval.hellointerval import HelloInterval
		return HelloInterval(self)._read()

	@property
	def RouterDeadInterval(self):
		"""Time interval (in seconds) that the emulated router waits to receive packets
		           from the neighbor DUT router before deleting that neighbor from its topology

		Get an instance of the RouterDeadInterval class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.routerdeadinterval.routerdeadinterval.RouterDeadInterval)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.routerdeadinterval.routerdeadinterval import RouterDeadInterval
		return RouterDeadInterval(self)._read()

	@property
	def RetransmitInterval(self):
		"""If an LSA transmission fails, Spirent TestCenter waits the duration of the
		           retransmit interval (in seconds) before re-transmitting the packet

		Get an instance of the RetransmitInterval class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.retransmitinterval.retransmitinterval.RetransmitInterval)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.retransmitinterval.retransmitinterval import RetransmitInterval
		return RetransmitInterval(self)._read()

	@property
	def Authentication(self):
		"""TBD

		Get an instance of the Authentication class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.authentication.authentication.Authentication)
		"""
		from openhltest_client.openhltest.sessions.config.devicegroups.devices.protocols.ospfv2.authentication.authentication import Authentication
		return Authentication(self)._read()

