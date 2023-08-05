from openhltest_client.base import Base


class IsisStatistics(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/isis-statistics resource.
	"""
	YANG_NAME = 'isis-statistics'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'device-name'
	YANG_PROPERTY_MAP = {"NeighborExtendedCircuitId": "neighbor-extended-circuit-id", "TxL1LanHelloCount": "tx-l1-lan-hello-count", "TxL1CsnpCount": "tx-l1-csnp-count", "TxL2LspCount": "tx-l2-lsp-count", "TxL1PsnpCount": "tx-l1-psnp-count", "RxL2CsnpCount": "rx-l2-csnp-count", "RxL2LspCount": "rx-l2-lsp-count", "DeviceName": "device-name", "TxL1LspCount": "tx-l1-lsp-count", "RxPtpHelloCount": "rx-ptp-hello-count", "ThreeWayP2pAdjacencyState": "three-way-p2p-adjacency-state", "TxPtpHelloCount": "tx-ptp-hello-count", "L2BroadcastAdjacencyState": "l2-broadcast-adjacency-state", "L1BroadcastAdjacencyState": "l1-broadcast-adjacency-state", "TxL2PsnpCount": "tx-l2-psnp-count", "TxL2CsnpCount": "tx-l2-csnp-count", "NeighborSystemId": "neighbor-system-id", "TxL2LanHelloCount": "tx-l2-lan-hello-count", "RxL1CsnpCount": "rx-l1-csnp-count", "RxL2PsnpCount": "rx-l2-psnp-count", "RxL1LspCount": "rx-l1-lsp-count", "RouterState": "router-state", "RxL2LanHelloCount": "rx-l2-lan-hello-count", "RxL1PsnpCount": "rx-l1-psnp-count", "RxL1LanHelloCount": "rx-l1-lan-hello-count", "PortName": "port-name"}

	def __init__(self, parent):
		super(IsisStatistics, self).__init__(parent)

	@property
	def DeviceName(self):
		"""Device Name

		Getter Returns:
			string
		"""
		return self._get_value('device-name')

	@property
	def PortName(self):
		"""An abstract test port name

		Getter Returns:
			string
		"""
		return self._get_value('port-name')
	@PortName.setter
	def PortName(self, value):
		return self._set_value('port-name', value)

	@property
	def RxL1LanHelloCount(self):
		"""Number of LAN Hello packets received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l1-lan-hello-count')
	@RxL1LanHelloCount.setter
	def RxL1LanHelloCount(self, value):
		return self._set_value('rx-l1-lan-hello-count', value)

	@property
	def TxL1LanHelloCount(self):
		"""Number of LAN Hello packets transmitted by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l1-lan-hello-count')
	@TxL1LanHelloCount.setter
	def TxL1LanHelloCount(self, value):
		return self._set_value('tx-l1-lan-hello-count', value)

	@property
	def RxL2LanHelloCount(self):
		"""Number of LAN Hello packets received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l2-lan-hello-count')
	@RxL2LanHelloCount.setter
	def RxL2LanHelloCount(self, value):
		return self._set_value('rx-l2-lan-hello-count', value)

	@property
	def TxL2LanHelloCount(self):
		"""Number of LAN Hello packets transmitted by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l2-lan-hello-count')
	@TxL2LanHelloCount.setter
	def TxL2LanHelloCount(self, value):
		return self._set_value('tx-l2-lan-hello-count', value)

	@property
	def TxL1CsnpCount(self):
		"""Number of Tx CSNPs sent to the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l1-csnp-count')
	@TxL1CsnpCount.setter
	def TxL1CsnpCount(self, value):
		return self._set_value('tx-l1-csnp-count', value)

	@property
	def TxL1LspCount(self):
		"""Number of Tx LSPs sent to the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l1-lsp-count')
	@TxL1LspCount.setter
	def TxL1LspCount(self, value):
		return self._set_value('tx-l1-lsp-count', value)

	@property
	def TxL1PsnpCount(self):
		"""Number of Tx PSNPs sent to the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l1-psnp-count')
	@TxL1PsnpCount.setter
	def TxL1PsnpCount(self, value):
		return self._set_value('tx-l1-psnp-count', value)

	@property
	def RxL1CsnpCount(self):
		"""Number of Rx CSNPs received from the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l1-csnp-count')
	@RxL1CsnpCount.setter
	def RxL1CsnpCount(self, value):
		return self._set_value('rx-l1-csnp-count', value)

	@property
	def RxL1LspCount(self):
		"""Number of Rx LSPs received from the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l1-lsp-count')
	@RxL1LspCount.setter
	def RxL1LspCount(self, value):
		return self._set_value('rx-l1-lsp-count', value)

	@property
	def RxL1PsnpCount(self):
		"""Number of Rx PSNPs received from the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l1-psnp-count')
	@RxL1PsnpCount.setter
	def RxL1PsnpCount(self, value):
		return self._set_value('rx-l1-psnp-count', value)

	@property
	def TxL2CsnpCount(self):
		"""Number of Tx CSNPs sent to the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l2-csnp-count')
	@TxL2CsnpCount.setter
	def TxL2CsnpCount(self, value):
		return self._set_value('tx-l2-csnp-count', value)

	@property
	def TxL2LspCount(self):
		"""Number of Tx LSPs sent to the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l2-lsp-count')
	@TxL2LspCount.setter
	def TxL2LspCount(self, value):
		return self._set_value('tx-l2-lsp-count', value)

	@property
	def TxL2PsnpCount(self):
		"""Number of Tx PSNPs sent to the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-l2-psnp-count')
	@TxL2PsnpCount.setter
	def TxL2PsnpCount(self, value):
		return self._set_value('tx-l2-psnp-count', value)

	@property
	def RxL2CsnpCount(self):
		"""Number of Rx CSNPs received from the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l2-csnp-count')
	@RxL2CsnpCount.setter
	def RxL2CsnpCount(self, value):
		return self._set_value('rx-l2-csnp-count', value)

	@property
	def RxL2LspCount(self):
		"""Number of Rx LSPs received from the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l2-lsp-count')
	@RxL2LspCount.setter
	def RxL2LspCount(self, value):
		return self._set_value('rx-l2-lsp-count', value)

	@property
	def RxL2PsnpCount(self):
		"""Number of Rx PSNPs received from the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-l2-psnp-count')
	@RxL2PsnpCount.setter
	def RxL2PsnpCount(self, value):
		return self._set_value('rx-l2-psnp-count', value)

	@property
	def RouterState(self):
		"""State of adjacency with the SUT

		Getter Returns:
			IDLE | INIT | UP | GR | GRHELPER
		"""
		return self._get_value('router-state')
	@RouterState.setter
	def RouterState(self, value):
		return self._set_value('router-state', value)

	@property
	def NeighborExtendedCircuitId(self):
		"""Learned the extended circuit ID of the adjacent neighbor after a three-way Hello exchange.

		Getter Returns:
			string
		"""
		return self._get_value('neighbor-extended-circuit-id')
	@NeighborExtendedCircuitId.setter
	def NeighborExtendedCircuitId(self, value):
		return self._set_value('neighbor-extended-circuit-id', value)

	@property
	def RxPtpHelloCount(self):
		"""Number of Rx point-to-point hellos received from the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-ptp-hello-count')
	@RxPtpHelloCount.setter
	def RxPtpHelloCount(self, value):
		return self._set_value('rx-ptp-hello-count', value)

	@property
	def TxPtpHelloCount(self):
		"""Number of Tx point-to-point hellos sent to the SUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-ptp-hello-count')
	@TxPtpHelloCount.setter
	def TxPtpHelloCount(self, value):
		return self._set_value('tx-ptp-hello-count', value)

	@property
	def NeighborSystemId(self):
		"""Learned System ID of the adjacent neighbor after three-way Helloexchange.

		Getter Returns:
			string
		"""
		return self._get_value('neighbor-system-id')
	@NeighborSystemId.setter
	def NeighborSystemId(self, value):
		return self._set_value('neighbor-system-id', value)

	@property
	def ThreeWayP2pAdjacencyState(self):
		"""Adjacency state of three-way Hello in point-to-pointnetwork.

		Getter Returns:
			UP | INIT | DOWN | NOT_STARTED | NA
		"""
		return self._get_value('three-way-p2p-adjacency-state')
	@ThreeWayP2pAdjacencyState.setter
	def ThreeWayP2pAdjacencyState(self, value):
		return self._set_value('three-way-p2p-adjacency-state', value)

	@property
	def L1BroadcastAdjacencyState(self):
		"""Adjacency state of broadcast router.

		Getter Returns:
			NOT_STARTED | IDLE | INIT | DIS_OTHER | DIS | GR | GRHELPER | NA
		"""
		return self._get_value('l1-broadcast-adjacency-state')
	@L1BroadcastAdjacencyState.setter
	def L1BroadcastAdjacencyState(self, value):
		return self._set_value('l1-broadcast-adjacency-state', value)

	@property
	def L2BroadcastAdjacencyState(self):
		"""Adjacency state of broadcast router.

		Getter Returns:
			NOT_STARTED | IDLE | INIT | DIS_OTHER | DIS | GR | GRHELPER | NA
		"""
		return self._get_value('l2-broadcast-adjacency-state')
	@L2BroadcastAdjacencyState.setter
	def L2BroadcastAdjacencyState(self, value):
		return self._set_value('l2-broadcast-adjacency-state', value)

	def create(self, DeviceName, PortName=None, RxL1LanHelloCount=None, TxL1LanHelloCount=None, RxL2LanHelloCount=None, TxL2LanHelloCount=None, TxL1CsnpCount=None, TxL1LspCount=None, TxL1PsnpCount=None, RxL1CsnpCount=None, RxL1LspCount=None, RxL1PsnpCount=None, TxL2CsnpCount=None, TxL2LspCount=None, TxL2PsnpCount=None, RxL2CsnpCount=None, RxL2LspCount=None, RxL2PsnpCount=None, RouterState=None, NeighborExtendedCircuitId=None, RxPtpHelloCount=None, TxPtpHelloCount=None, NeighborSystemId=None, ThreeWayP2pAdjacencyState=None, L1BroadcastAdjacencyState=None, L2BroadcastAdjacencyState=None):
		"""Create an instance of the `isis-statistics` resource

		Args:
			DeviceName (string): Device Name
			PortName (string): An abstract test port name
			RxL1LanHelloCount (uint64): Number of LAN Hello packets received by the emulated router.
			TxL1LanHelloCount (uint64): Number of LAN Hello packets transmitted by the emulated router.
			RxL2LanHelloCount (uint64): Number of LAN Hello packets received by the emulated router.
			TxL2LanHelloCount (uint64): Number of LAN Hello packets transmitted by the emulated router.
			TxL1CsnpCount (uint64): Number of Tx CSNPs sent to the SUT.
			TxL1LspCount (uint64): Number of Tx LSPs sent to the SUT.
			TxL1PsnpCount (uint64): Number of Tx PSNPs sent to the SUT.
			RxL1CsnpCount (uint64): Number of Rx CSNPs received from the SUT.
			RxL1LspCount (uint64): Number of Rx LSPs received from the SUT.
			RxL1PsnpCount (uint64): Number of Rx PSNPs received from the SUT.
			TxL2CsnpCount (uint64): Number of Tx CSNPs sent to the SUT.
			TxL2LspCount (uint64): Number of Tx LSPs sent to the SUT.
			TxL2PsnpCount (uint64): Number of Tx PSNPs sent to the SUT.
			RxL2CsnpCount (uint64): Number of Rx CSNPs received from the SUT.
			RxL2LspCount (uint64): Number of Rx LSPs received from the SUT.
			RxL2PsnpCount (uint64): Number of Rx PSNPs received from the SUT.
			RouterState (enumeration): State of adjacency with the SUT
			NeighborExtendedCircuitId (string): Learned the extended circuit ID of the adjacent neighbor after a three-way Hello exchange.
			RxPtpHelloCount (uint64): Number of Rx point-to-point hellos received from the SUT.
			TxPtpHelloCount (uint64): Number of Tx point-to-point hellos sent to the SUT.
			NeighborSystemId (string): Learned System ID of the adjacent neighbor after three-way Helloexchange.
			ThreeWayP2pAdjacencyState (enumeration): Adjacency state of three-way Hello in point-to-pointnetwork.
			L1BroadcastAdjacencyState (enumeration): Adjacency state of broadcast router.
			L2BroadcastAdjacencyState (enumeration): Adjacency state of broadcast router.
		"""
		return self._create(locals())

	def read(self, DeviceName=None):
		"""Get `isis-statistics` resource(s). Returns all resources from the server if `DeviceName` is not specified

		"""
		return self._read(DeviceName)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `isis-statistics` resource

		"""
		return self._delete()

	def update(self, PortName=None, RxL1LanHelloCount=None, TxL1LanHelloCount=None, RxL2LanHelloCount=None, TxL2LanHelloCount=None, TxL1CsnpCount=None, TxL1LspCount=None, TxL1PsnpCount=None, RxL1CsnpCount=None, RxL1LspCount=None, RxL1PsnpCount=None, TxL2CsnpCount=None, TxL2LspCount=None, TxL2PsnpCount=None, RxL2CsnpCount=None, RxL2LspCount=None, RxL2PsnpCount=None, RouterState=None, NeighborExtendedCircuitId=None, RxPtpHelloCount=None, TxPtpHelloCount=None, NeighborSystemId=None, ThreeWayP2pAdjacencyState=None, L1BroadcastAdjacencyState=None, L2BroadcastAdjacencyState=None):
		"""Update the current instance of the `isis-statistics` resource

		Args:
			PortName (string): An abstract test port name
			RxL1LanHelloCount (uint64): Number of LAN Hello packets received by the emulated router.
			TxL1LanHelloCount (uint64): Number of LAN Hello packets transmitted by the emulated router.
			RxL2LanHelloCount (uint64): Number of LAN Hello packets received by the emulated router.
			TxL2LanHelloCount (uint64): Number of LAN Hello packets transmitted by the emulated router.
			TxL1CsnpCount (uint64): Number of Tx CSNPs sent to the SUT.
			TxL1LspCount (uint64): Number of Tx LSPs sent to the SUT.
			TxL1PsnpCount (uint64): Number of Tx PSNPs sent to the SUT.
			RxL1CsnpCount (uint64): Number of Rx CSNPs received from the SUT.
			RxL1LspCount (uint64): Number of Rx LSPs received from the SUT.
			RxL1PsnpCount (uint64): Number of Rx PSNPs received from the SUT.
			TxL2CsnpCount (uint64): Number of Tx CSNPs sent to the SUT.
			TxL2LspCount (uint64): Number of Tx LSPs sent to the SUT.
			TxL2PsnpCount (uint64): Number of Tx PSNPs sent to the SUT.
			RxL2CsnpCount (uint64): Number of Rx CSNPs received from the SUT.
			RxL2LspCount (uint64): Number of Rx LSPs received from the SUT.
			RxL2PsnpCount (uint64): Number of Rx PSNPs received from the SUT.
			RouterState (enumeration): State of adjacency with the SUT
			NeighborExtendedCircuitId (string): Learned the extended circuit ID of the adjacent neighbor after a three-way Hello exchange.
			RxPtpHelloCount (uint64): Number of Rx point-to-point hellos received from the SUT.
			TxPtpHelloCount (uint64): Number of Tx point-to-point hellos sent to the SUT.
			NeighborSystemId (string): Learned System ID of the adjacent neighbor after three-way Helloexchange.
			ThreeWayP2pAdjacencyState (enumeration): Adjacency state of three-way Hello in point-to-pointnetwork.
			L1BroadcastAdjacencyState (enumeration): Adjacency state of broadcast router.
			L2BroadcastAdjacencyState (enumeration): Adjacency state of broadcast router.
		"""
		return self._update(locals())

