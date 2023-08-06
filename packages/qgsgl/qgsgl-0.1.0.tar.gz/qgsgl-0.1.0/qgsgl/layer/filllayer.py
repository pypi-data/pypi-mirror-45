from .base import BaseLayer


class FillLayer(BaseLayer):
    def __init__(self, qgis_symbol_layer, **kwargs):
        self.opacity = kwargs.get('opacity', 1)
        super().__init__(qgis_symbol_layer)

    def get_paint_properties(self):
        return {
            'fill-color': self.qgis_symbol_layer.color().name(),
            'fill-opacity': self.opacity
        }

    def get_layout_properties(self):
        pass

    def get_type(self):
        return 'fill'
