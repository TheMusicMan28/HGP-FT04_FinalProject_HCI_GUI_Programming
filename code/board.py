from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtTest import QTest
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location

    boardWidth  = 8     # board is 8 squares wide
    boardHeight = 8     # board is 8 squares tall
    timerSpeed  = 1000     # the timer updates every 1 second
    counter     = 100    # the number the counter will count down from

    times_reset = -1

    current_player = 1

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started

        self.boardArray = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]

        self.start()                # start the game which will start the timer
        self.setStyleSheet("background-color: black;")
        self.printBoardArray()

    def make_connection(self, score_board):
        score_board.resetSignal.connect(self.resetGame)

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # set the boolean which determines if the game has started to TRUE
        self.resetGame(1)                            # reset the game
        self.timer.start(self.timerSpeed, self)     # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            Board.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)      # if we do not handle an event we should pass it to the super
                                                        # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "["+str(event.position().x())+","+str(event.position().y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)

        closest_x = int((event.position().x() - self.squareWidth() / 2) / self.squareWidth())
        if(closest_x >= 7):
            closest_x = 6
        print(closest_x)
        closest_y = int((event.position().y() - self.squareHeight() / 2)/ self.squareHeight())
        if (closest_y >= 7):
            closest_y = 6
        print(closest_y)

        print("testing board array")
        self.boardArray[closest_y][closest_x] = self.current_player
        print(self.boardArray)

        painter = QPainter(self)
        self.drawPieces(painter)

        self.update()

        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self, signal):
        '''clears pieces from the board'''
        # add times reset
        self.times_reset += signal
        # reset array to full transparent:
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                self.boardArray[row][col] = 0

        #call piece drawing function
        painter = QPainter(self)
        self.drawPieces(painter)


    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.brush = QBrush(Qt.BrushStyle.SolidPattern)
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                # If outside row, make box dark brown to contrast with board and pieces
                if (col == 0 or col == 7 or row == 0 or row == 7):
                    self.brush.setColor(QColor(100, 69, 12))
                    painter.setBrush(self.brush)
                else:
                    if(col % 2 == 0):
                        if(row % 2 == 0):
                            self.brush.setColor(QColor(138, 109, 49))
                            painter.setBrush(self.brush)
                        else:
                            self.brush.setColor(QColor(191, 162, 77))
                            painter.setBrush(self.brush)
                    else:
                        if (row % 2 == 0):
                            self.brush.setColor(QColor(191, 162, 77))
                            painter.setBrush(self.brush)
                        else:
                            self.brush.setColor(QColor(138, 109, 49))
                            painter.setBrush(self.brush)

                if((row == 0 and col == 0) or (row == 0 and col == 7)):
                    painter.fillRect(col, row, self.squareWidth() - 2, self.squareHeight() + 2, painter.brush())
                if(row == 0 or row == 7):
                    painter.fillRect(col, row, self.squareWidth() + 2, self.squareHeight() - 2, painter.brush())
                elif(col == 0 or col == 7):
                    painter.fillRect(col, row, self.squareWidth() - 2, self.squareHeight() + 2, painter.brush())
                else:
                    painter.fillRect(col, row, self.squareWidth() - 2, self.squareHeight() - 2, painter.brush())

                painter.restore()

    def drawPieces(self, painter):
        '''draw the prices on the board'''

        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()

                if(self.boardArray[row][col] == 0):
                    colour = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
                    brush = QBrush(Qt.BrushStyle.SolidPattern)
                    brush.setColor(colour)
                elif(self.boardArray[row][col] == 1):
                    colour = Qt.GlobalColor.black  # empty square could be modeled with transparent pieces
                    brush = QBrush(Qt.BrushStyle.SolidPattern)
                    brush.setColor(colour)
                elif (self.boardArray[row][col] == 2):
                    colour = Qt.GlobalColor.white  # empty square could be modeled with transparent pieces
                    brush = QBrush(Qt.BrushStyle.SolidPattern)
                    brush.setColor(colour)
                else:
                    colour = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
                    brush = QBrush(Qt.BrushStyle.SolidPattern)
                    brush.setColor(colour)
                # set transformation so that each piece is on an intersection
                colTransformation = self.squareWidth() * col + (self.squareWidth() * .75)
                rowTransformation = self.squareHeight() * row + (self.squareHeight() * .75)
                painter.translate(colTransformation, rowTransformation)
                # set color
                painter.setBrush(brush)
                # set piece size & draw
                radius = self.squareWidth() / 4
                center = QPointF(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
