from PyQt5 import QtChart, QtGui, QtCore


class ChartView(QtChart.QChartView):

    def __init__(self, parent):
        QtChart.QChartView.__init__(self, parent)
        self.color_names = ["unknown", "lavander", "esmerald green",
                           "intense purple", "Pink", "egg yellow",
                           "mandarin orange", "Turqouise", "graphite",
                           "blueberry blue", "moss green", "tomato"]

        self.color_reference = [(125, 125, 125), (116, 134, 197), (10, 176, 124),
                                (148, 40, 165), (236, 121, 126), (248, 190, 64),
                                (248, 73, 43), (0, 162, 220), (97, 97, 97),
                                (51, 86, 185), (4, 130, 79), (221, 7, 27)]

    def display_color_data(self, arr):
        series = QtChart.QBarSeries()
        for name, c, col in zip(self.color_names, self.color_reference, arr):
            s = QtChart.QBarSet(name)
            s << col
            s.setColor(QtGui.QColor(c[0], c[1], c[2]))
            series.append(s)

        chart = QtChart.QChart()
        chart.addSeries(series)
        chart.setTitle("Color distribution")
        chart.legend()
        axis = QtChart.QValueAxis()
        axis.setRange(0, max(arr))
        chart.addAxis(axis, QtCore.Qt.AlignLeft)

        series.attachAxis(axis)
        self.setChart(chart)
