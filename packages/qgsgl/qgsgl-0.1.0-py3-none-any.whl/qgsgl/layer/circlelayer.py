from .base import BaseLayer
from ..utils import map_unit_to_pixel, convert_outline_width


class CircleLayer(BaseLayer):
    def __init__(self, qgis_symbol_layer, **kwargs):
        self.opacity = kwargs.get('opacity', 1)
        super().__init__(qgis_symbol_layer)

    def get_paint_properties(self, output_dpi=None):
        return {
            'circle-color': self.qgis_symbol_layer.color().name(),
            'circle-radius': map_unit_to_pixel(
                self.qgis_symbol_layer.size() / 2,
                self.qgis_symbol_layer.sizeUnit(),
                output_dpi
            ),
            'circle-stroke-color': self.qgis_symbol_layer.strokeColor().name(),
            'circle-stroke-width': convert_outline_width(
                self.qgis_symbol_layer),
            'circle-opacity': self.opacity
        }

    def get_layout_properties(self):
        pass

    def get_type(self):
        return 'circle'
