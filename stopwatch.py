Python 3.12.0 (tags/v3.12.0:0fb18b0, Oct  2 2023, 13:03:39) [MSC v.1935 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QGridLayout, QWidget, QPushButton, QLCDNumber
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer

class Counter(QObject):
    countChanges = pyqtSignal(int)

    def _init_(self, parent=None, step=1):
        super()._init_(parent)
        self.step = step
        self.count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCount)

    def start(self):
        self.timer.start(1000)

    def terminate(self):
        self.timer.stop()

    def reset(self):
        self.count = 0
        self.countChanges.emit(self.count)

    def updateCount(self):
        self.count += self.step
        self.countChanges.emit(self.count)


class MainWindow(QMainWindow):
    def _init_(self, parent=None):
        super()._init_(parent)
        # Counter
        self.hours = Counter(self, 1)
        self.minutes = Counter(self, 1)
        self.seconds = Counter(self, 1)

        # Labels
        hoursLabel = QLabel("Hours")
        minutesLabel = QLabel("Minutes")
        secondsLabel = QLabel("Seconds")
        labels = QHBoxLayout()
        labels.addWidget(hoursLabel)
        labels.addWidget(minutesLabel)
        labels.addWidget(secondsLabel)

        # Screen
        self.hourScreen = QLCDNumber(self)
        self.minuteScreen = QLCDNumber(self)
        self.secondScreen = QLCDNumber(self)
        self.hours.countChanges.connect(self.hourScreenUpdate)
        self.minutes.countChanges.connect(self.minuteScreenUpdate)
        self.seconds.countChanges.connect(self.secondScreenUpdate)
        screen = QHBoxLayout()
        screen.addWidget(self.hourScreen)
        screen.addWidget(self.minuteScreen)
        screen.addWidget(self.secondScreen)

        # Buttons
        self.startButton = QPushButton("Start", self)
        self.startButton.clicked.connect(self.start)
        self.stopButton = QPushButton("Stop", self)
        self.stopButton.clicked.connect(self.terminate)
        self.resetButton = QPushButton("Reset", self)
        self.resetButton.clicked.connect(self.reset)
...         buttons = QHBoxLayout()
...         buttons.addWidget(self.startButton)
...         buttons.addWidget(self.stopButton)
...         buttons.addWidget(self.resetButton)
... 
...         # Main Layout
...         mainLayout = QGridLayout()
...         mainLayout.addLayout(labels, 0, 0, 1, 1)
...         mainLayout.addLayout(screen, 1, 0, 1, 1)
...         mainLayout.addLayout(buttons, 2, 0, 1, 1)
...         
...         widget = QWidget()
...         widget.setLayout(mainLayout)
...         self.setCentralWidget(widget)
... 
...     def start(self):
...         self.seconds.start()
...         self.minutes.start()
...         self.hours.start()
... 
...     def terminate(self):
...         self.seconds.terminate()
...         self.minutes.terminate()
...         self.hours.terminate()
... 
...     def reset(self):
...         self.seconds.reset()
...         self.minutes.reset()
...         self.hours.reset()
... 
...     @pyqtSlot(int)
...     def hourScreenUpdate(self, count):
...         self.hourScreen.display(count // 3600)
... 
...     @pyqtSlot(int)
...     def minuteScreenUpdate(self, count):
...         self.minuteScreen.display((count // 60) % 60)
... 
...     @pyqtSlot(int)
...     def secondScreenUpdate(self, count):
...         self.secondScreen.display(count % 60)
... 
... if _name_ == "_main_":
...     app = QApplication(sys.argv)
...     window = MainWindow()
...     window.show()
