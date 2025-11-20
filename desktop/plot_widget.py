# desktop/plot_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import plotly.io as pio
import tempfile

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.view = QWebEngineView()
        self.layout.addWidget(self.view)

    def update_chart(self, data_dict):
        fig = go.Figure([go.Bar(x=list(data_dict.keys()), y=list(data_dict.values()), marker_color='#00ccff')])
        fig.update_layout(
            title='Connection Intents Count',
            plot_bgcolor='#1e1e2f',
            paper_bgcolor='#1e1e2f',
            font_color='#fff'
        )
        html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        pio.write_html(fig, file=html_file.name, auto_open=False)
        self.view.setUrl(f"file:///{html_file.name}")
