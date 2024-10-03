from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget
from pyqtgraph import GraphicsLayoutWidget


class TimeSeriesView(QWidget):
    def __init__(self, timeseries_model, parent=None):
        super().__init__(parent)
        self.timeseries_model = timeseries_model

        # Components
        self.plot_window = GraphicsLayoutWidget()
        self.plot_window.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.plot_window.ci.layout.setSpacing(0)
        self.plot_window.setBackground(None)
        self.setMouseTracking(False)

        self.plot_widget = self.plot_window.addPlot(0, 0)
        self.plot_widget.setLabel("bottom", "Time (s)")
        self.plot_widget.setXRange(-0.5, 0.5)
        self.plot_widget.hideAxis("left")
        self.plot_widget.hideButtons()
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.setMenuEnabled(False)
