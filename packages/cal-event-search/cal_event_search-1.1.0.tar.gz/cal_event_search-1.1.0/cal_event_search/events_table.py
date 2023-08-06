from PyQt5 import QtCore, QtWidgets, QtGui
from cal_event_search.api_utils import connect, get_list
import datetime
import numpy as np


class EventsTable(QtWidgets.QTableWidget):

    send_entries = QtCore.pyqtSignal(int)
    send_duration = QtCore.pyqtSignal(str)
    SIMILAR_RANGE = 3

    def __init__(self, parent=None):
        QtWidgets.QTableWidget.__init__(self, parent=parent)
        self.service = None
        self.color = None
        self.max_entries = None
        self.end_time = datetime.datetime.utcnow()
        self.start_time = self.end_time - datetime.timedelta(days=7)
        self.search_entry = None
        self.count = 0
        self.color_reference = [(125, 125, 125), (116, 134, 197), (10, 176, 124),
                                (148, 40, 165), (236, 121, 126), (248, 190, 64),
                                (248, 73, 43), (0, 162, 220), (97, 97, 97),
                                (51, 86, 185), (4, 130, 79), (221, 7, 27)]

        self.color_names = ["unknown", "lavander", "esmerald green",
                            "intense purple", "Pink", "egg yellow",
                            "mandarin orange", "Turqouise", "graphite",
                            "blueberry blue", "moss green", "tomato"]

    def set_max_entries(self, entries):
        try:
            self.max_entries = int(entries)
        except ValueError:
            self.max_entries = None

    def empty_list(self):
        while self.rowCount() > 0:
            self.removeRow(0)
        self.count = 0
        self.setSortingEnabled(False)

    def empty_table(self):
        self.empty_list()

    def set_search_entry(self, s):
        self.search_entry = s.lower()
        if len(s) == 0:
            self.search_entry = None

    def set_end_time(self, time):
        self.end_time = time.toPyDateTime()

    def set_start_time(self, time):
        self.start_time = time.toPyDateTime()

    def set_last_week(self):
        self.end_time = datetime.datetime.utcnow()
        self.start_time = self.end_time - datetime.timedelta(days=7)

    def set_last_month(self):
        self.end_time = datetime.datetime.utcnow()
        self.start_time = self.end_time - datetime.timedelta(days=30)

    def set_last_year(self):
        self.end_time = datetime.datetime.utcnow()
        self.start_time = self.end_time - datetime.timedelta(days=365)

    def similar(self, bag):
        words = bag.split()
        for word in words:
            if EventsTable.levenshtein(self.search_entry, word) < self.SIMILAR_RANGE:
                return True
        return False

    def add_row(self, summary, duration, start_date, color, color_name):
        self.insertRow(self.count)
        self.setItem(self.count, 0, QtWidgets.QTableWidgetItem(summary))
        self.setItem(self.count, 1, QtWidgets.QTableWidgetItem(duration))
        self.setItem(self.count, 2, QtWidgets.QTableWidgetItem(start_date))
        self.setItem(self.count, 3, QtWidgets.QTableWidgetItem(color_name))
        self.item(self.count, 3).setBackground(QtGui.QColor(color[0], color[1], color[2]))
        self.item(self.count, 3).setForeground(QtGui.QColor(color[0], color[1], color[2]))

    def add_list_elements(self):
        print("Events: ")
        elements = get_list(self.service, self.start_time,
                            self.end_time)
        self.empty_list()
        print(len(elements))
        total_duration = 0
        for e in elements:
            if 'summary' in e and 'dateTime' in e['start']:
                summary = e['summary']
                color = self.color_reference[0]
                color_name = self.color_names[0]
                start_time = e['start']['dateTime']
                start_time = datetime.datetime.strptime(start_time[:-6], "%Y-%m-%dT%H:%M:%S")
                end_time = e['end']['dateTime']
                end_time = datetime.datetime.strptime(end_time[:-6], "%Y-%m-%dT%H:%M:%S")
                duration = end_time - start_time
                if 'colorId' in e:
                    color = self.color_reference[int(e['colorId'])]
                    color_name = self.color_names[int(e['colorId'])]
                if self.color is None:
                    if self.search_entry is None or self.similar(summary.lower()):
                        self.add_row(summary, str(duration.seconds),
                                     str(start_time.hour) + ":" + str(start_time.minute),
                                     color, color_name)
                        self.count += 1
                        total_duration += int(duration.seconds)
                elif 'colorId' in e and int(e['colorId']) == self.color:
                    if self.search_entry is None or self.similar(summary.lower()):
                        self.add_row(summary, str(duration.seconds),
                                     str(start_time.hour) + ":" + str(start_time.minute),
                                     color, color_name)
                        self.count += 1
                        total_duration += int(duration.seconds)
                if self.max_entries and self.count >= self.max_entries:
                    break

        # emit signals
        self.send_entries.emit(self.count)
        self.send_duration.emit(str(total_duration) + " seconds")
        self.setSortingEnabled(True)

    def save_data(self):
        data = np.array([])
        n_cols = 3
        for i in range(self.count):
            for j in range(n_cols):
                data = np.append(data, self.item(i, j).text())
        data = data.reshape(self.count, n_cols)
        np.savetxt("data.csv", data, delimiter=",", fmt='%s')

    def connect_api(self):
        self.service = connect()

    def filter_color(self, color):
        if color != 0:
            self.color = color
        else:
            self.color = None

    @staticmethod
    def levenshtein(s1, s2):
        if len(s1) < len(s2):
            return EventsTable.levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

