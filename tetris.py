import numpy as np
import copy
import time
import random
import sys
import readchar




class Tetris:
    def __init__(self,seed=None):
        if seed:
            random.seed(seed)
        self.width = 10
        self.height = 20
        self.score = 0
        self.finished = False
        self.board = np.zeros(
                (self.height + 4, self.width + 4), dtype="int")

        for x in range(self.width + 4):
            for y in range(self.height + 4):
                if x == 0 or x == 1 or x == self.width + 2 or x == self.width + 3 or y == 0 or y == 1 or y == self.height + 2 or y == self.height + 3:
                    self.board[y][x] = 3
        self.blocks = [
            np.array([[1, 1, 1, 0],
                      [0, 1, 0, 0]], dtype="int"),
            np.array([[1, 1, 0, 0],
                      [0, 1, 1, 0]], dtype="int"),
            np.array([[0, 0, 1, 1],
                      [0, 1, 1, 0]], dtype="int"),
            np.array([[0, 1, 0, 0],
                      [0, 1, 1, 1]], dtype="int"),
            np.array([[0, 0, 1, 0],
                      [1, 1, 1, 0]], dtype="int"),
            np.array([[1, 1, 1, 1],
                      [0, 0, 0, 0]], dtype="int"),
            np.array([[0, 1, 1, 0],
                      [0, 1, 1, 0]], dtype="int")
        ]
        self.createNewBlock(2)

        self.randomNumber=[int(c) for c in open("randomNumber.txt","r").read()]

    def __repr__(self):
        retval = ""
        for line in self.board:
            for block in line:
                if block == 2:
                    retval += "◆"
                elif block == 1:
                    retval += "■"
                elif block == 0:
                    retval += "□"
            retval += "\n"
        retval += "score: {}".format(self.score)
        return retval

    def whetherCollision(self, newBoard):
        beforeBlockNum = np.sum(self.board > 0)
        afterBlockNum = np.sum(newBoard > 0)
        if afterBlockNum < beforeBlockNum:
            return True
        else:
            return False

    def down(self):
        activeBlock = (self.board == 2)
        newBoard = copy.deepcopy(self.board)
        newBoard -= activeBlock * 2
        activeBlockDowned = np.delete(activeBlock, axis=0, obj=-3)
        activeBlockDowned = np.vstack(
            (np.zeros(self.width + 4, dtype="int").reshape(1, -1), activeBlockDowned))

        newBoard += activeBlockDowned * 2
        if self.whetherCollision(newBoard) == False:
            self.board = newBoard
            return True
        else:
            self.board[self.board == 2] = 1
            self.clearLine()
            if np.sum(self.board[2]) + np.sum(self.board[3]) + np.sum(self.board[4]) > 36:
                self.finished = True
            else:
                self.score += 1
                self.createNewBlock(self.getRandomNumber())
                return False

    def right(self):
        activeBlock = (self.board == 2)
        newBoard = copy.deepcopy(self.board)
        newBoard -= activeBlock * 2
        activeBlockRighted = np.delete(activeBlock, axis=1, obj=-3)
        activeBlockRighted = np.hstack(
            (np.zeros(self.height + 4, dtype="int").reshape(-1, 1), activeBlockRighted))

        newBoard += activeBlockRighted * 2
        if self.whetherCollision(newBoard) == False:
            self.board = newBoard
            return True
        else:
            return False

    def left(self):
        activeBlock = (self.board == 2)
        newBoard = copy.deepcopy(self.board)
        newBoard -= activeBlock * 2
        activeBlockLefted = np.delete(activeBlock, axis=1, obj=2)
        activeBlockLefted = np.hstack(
            (activeBlockLefted, np.zeros(self.height + 4, dtype="int").reshape(-1, 1)))

        newBoard += activeBlockLefted * 2
        if self.whetherCollision(newBoard) == False:
            self.board = newBoard
            return True
        else:
            return False

    def rotate(self):
        activeBlock = (self.board == 2)
        newBoard = copy.deepcopy(self.board)
        newBoard -= activeBlock * 2
        Ax, Ay = self._getCenterOfGravity(activeBlock)

        Ax = max(int(Ax) - 1, 0)
        Ax = min(Ax, self.width - 4)
        Ay = max(int(Ay) - 1, 0)
        Ay = min(Ay, self.height - 4)

        piece = activeBlock[Ay:Ay + 4, Ax:Ax + 4]
        piece = piece.transpose(1, 0)[::-1]
        activeBlockRotated = np.zeros_like(self.board)
        activeBlockRotated[Ay:Ay + 4, Ax:Ax + 4] = piece
        newBoard += activeBlockRotated * 2
        if self.whetherCollision(newBoard) == False:
            self.board = newBoard
            return True
        else:
            return False

    def selectNewBlock(self, i=None):
        if i:
            return self.blocks[i]
        else:
            return random.choice(self.blocks)

    def createNewBlock(self, i=None):
        newBlock = self.selectNewBlock(i)
        newBlockBoard = np.zeros_like(self.board)
        newBlockBoard[3:5, 5:9] = newBlock
        self.board += newBlockBoard * 2

    def _getCenterOfGravity(self, array):
        sumension = np.sum(array)
        if sumension == 0:
            return 0, 0
        Ax = np.sum(np.sum(array, axis=0)
                    * np.arange(array.shape[1])) / sumension
        Ay = np.sum(np.sum(array, axis=1)
                    * np.arange(array.shape[0])) / sumension
        return Ax, Ay

    def clearLine(self):
        rows = np.sum(self.board, axis=1)
        for i, v in enumerate(rows):
            if v >= 22 and i != 0 and i != 1 and i != self.height + 2 and i != self.height + 3:
                self.board = np.delete(self.board, axis=0, obj=i)
                self.board = np.insert(self.board, 2, np.array(
                    [3, 3] + [0 for i in range(self.width)] + [3, 3]), axis=0)
                self.score += 100

    def getRandomNumber(self):
        return self.randomNumber.pop(0)


def _getBestScore(board):
    retval=[]
    score=0

    t_rotate = Tetris(copy.deepcopy(board))
    if t_rotate.rotate():
        retval.append(t_rotate.board)
        score=max(score,t_rotate.score)

    t_left=Tetris(board)
    if t_left.left():
        retval.append(t_left.board)
        score=max(score,t_left.score)

    t_right=Tetris(board)
    if t_right.right():
        retval.append(t_right.board)
        score=max(score,t_right.score)

    t_down=Tetris(board)
    if t_down.down():
        retval.append(t_down.board)
        score=max(score,t_down.score)

    return retval,score



def phenotype(chromosome):
    t = Tetris(0)
    for c in chromosome:
        if c == 0:
            t.rotate()
        elif c == 1:
            t.left()
        elif c == 2:
            t.right()
        elif c == 3:
            t.down()
        print(t)
        time.sleep(0.1)
        if t.finished:
            return t.score
    return t.score






if __name__ == "__main__":
    tetris = Tetris()
    print(tetris)
    while tetris.finished == False:
        c = readchar.readchar()
        if c == "q":
            sys.exit()
        elif c == "w":
            tetris.rotate()
        elif c == "a":
            tetris.left()
        elif c == "s":
            tetris.right()
        elif c == "z":
            tetris.down()
        print(tetris)
    print("game over")
