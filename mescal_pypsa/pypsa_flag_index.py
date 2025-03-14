from mescal.enums import ItemTypeEnum, VisualizationTypeEnum, TopologyTypeEnum
from mescal.flag.flag_index import FlagIndex
from mescal.units import Units
from mescal.utils.logging import get_logger
from mescal.utils.string_inflections import to_plural, to_singular

logger = get_logger(__name__)


class PyPSAFlagIndex(FlagIndex):

    @classmethod
    def get_flag_type(cls) -> type[str]:
        return str

    def get_flag_from_string(self, flag_string: str) -> str:
        return flag_string

    def _get_linked_model_flag(self, flag: str) -> str:
        if self._get_item_type(flag) != ItemTypeEnum.TimeSeries:
            raise ValueError
        return flag.replace('_t', '')

    def _get_item_type(self, flag: str) -> ItemTypeEnum:
        if flag.endswith('_t'):
            return ItemTypeEnum.TimeSeries
        return ItemTypeEnum.Model

    def _get_visualization_type(self, flag: str) -> VisualizationTypeEnum:
        f = flag.lower()
        types = {
            'bus': VisualizationTypeEnum.Point,
            'generator': VisualizationTypeEnum.Point,
            'load': VisualizationTypeEnum.Point,
            'transformer': VisualizationTypeEnum.Point,
            'line': VisualizationTypeEnum.Line,
            'link': VisualizationTypeEnum.Line,
            # TODO: add storage units, other object types
        }
        for k, t in types.items():
            if k in f:
                return t
        logger.warning(f'No VisualizationTypeEnum registered for {flag}. Falling back to "Other".')
        return VisualizationTypeEnum.Other

    def _get_topology_type(self, flag: str) -> TopologyTypeEnum:
        f = flag.lower()
        types = {
            'bus': TopologyTypeEnum.Node,
            'load': TopologyTypeEnum.NodeConnectedElement,
            'generator': TopologyTypeEnum.NodeConnectedElement,
            'transformer': TopologyTypeEnum.Edge,
            'line': TopologyTypeEnum.Edge,
            'link': TopologyTypeEnum.Edge,
            # TODO: add storage units, other object types
        }
        for k, t in types.items():
            if k in f:
                return t
        logger.warning(f'No TopologyTypeEnum registered for {flag}. Falling back to "Other".')
        return TopologyTypeEnum.Other

    def _get_unit(self, flag: str) -> Units.Unit:
        pass

    def _get_linked_model_flag_for_membership_column(self, membership_column_name: str) -> str:
        return to_plural(membership_column_name)

    def _get_membership_column_name_for_model_flag(self, flag: str) -> str:
        return to_singular(flag.lower())
