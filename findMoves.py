from settings import *

# functions to find the possible moves for each piece based on game state, pos and colour, along with other useful functions

def removeIllegalMoves(board, row, col, colour, pieceMoves):
    legalMoves = []

    piece = board[row][col]

    # perform each move and check if it is legal or not, if so append to legalMoves
    for move in pieceMoves:
        # track original board so it can be reverted later
        originalPiece = board[move[0]][move[1]]
        
        # perform move
        board[move[0]][move[1]] = piece
        board[row][col] = ''
        
        # check if the move puts the king in check
        kingPos = findKing(board, colour)
        if not checkSquaresAttacked(board, kingPos[0], kingPos[1]):
            legalMoves.append(move)

        # revert move
        board[row][col] = piece
        board[move[0]][move[1]] = originalPiece

    return legalMoves

def getPawnMoves(board, row, col, colour):
    moves = []

    if colour == 'white':
        startingRow = 6
        dir = -1
    else:
        startingRow = 1
        dir = 1

    # checking if square in front is empty
    if board[row + dir][col] == '':
        moves.append([row + dir, col])
        # checking if pawn can move 2 squares, and its still on starting row, given that first suare infront is empty
        if row == startingRow and board[row + (dir * 2)][col] == '':
            moves.append([row + (dir * 2), col])

    return moves


def getPawnAttackMoves(board, row, col, colour):
    moves = []

    if colour == 'white':
        dir = -1
    else:
        dir = 1

    # check that pawn isnt on edge of board and check if diagonal square on each direrection is empty and of opposite colour
    if 0 < row < 7:
        if col > 0 and board[row + dir][col - 1] and board[row + dir][col - 1].islower() != (colour == 'white'):
            moves.append([row + dir, col - 1])
        if col < 7 and board[row + dir][col + 1] and board[row + dir][col + 1].islower() != (colour == 'white'):
            moves.append([row + dir, col + 1])

    return moves


def getRookMoves(board, row, col, colour):
    moves = []

    # directinos in which rooks can move - left, up, right, down
    dir = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    for dr, dc in dir:
        r = row + dr
        c = col + dc
        # while piece is in boundaries of board 
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == '':
                moves.append([r, c])
            else:
                # check if pieces of same colour are in the way, if not it can be taken
                if board[r][c].islower() == (colour == 'white'):
                    break
                else:
                    moves.append([r, c])
                    break
            r += dr
            c += dc

    return moves


def getBishopMoves(board, row, col, colour):
    moves = []

    # same as rook but different directions in which they can move
    dir = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

    for dr, dc in dir:
        r = row + dr
        c = col + dc
        # while piece is in boundaries of board 
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == '':
                moves.append([r, c])
            else:
                # check if pieces of same colour are in the way, if not it can be taken
                if board[r][c].islower() == (colour == 'white'):
                    break
                else:
                    moves.append([r, c])
                    break
            r += dr
            c += dc

    return moves


def getKnightMoves(board, row, col, colour):
    moves = []

    # possible knight mvoes
    dir = [[2, 1], [1, 2], [-2, 1], [-1, 2], [2, -1], [1, -2], [-2, -1], [-1, -2]]

    for move in dir:
        r = row + move[0]
        c = col + move[1]
        # check if its in boundaries
        if r >= 0 and r < 8 and c >= 0 and c < 8:
            if board[r][c] == '':
                moves.append([r, c])
            else:
                # check if the piece is of opposite colour
                if board[r][c].islower() == (colour == 'black'):
                    moves.append([r, c])

    return moves


def getQueenMoves(board, row, col, colour):
    # combination of rook moves and bishop moves
    moves = []

    moves.extend(getBishopMoves(board, row, col, colour))
    moves.extend(getRookMoves(board, row, col, colour))

    return moves


def getKingMoves(board, row, col, colour):
    moves = []

    # possible moves
    dir = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for move in dir:
        r = row + move[0]
        c = col + move[1]
        # check if its in boundaries
        if r >= 0 and r < 8 and c >= 0 and c < 8:
            if board[r][c] == '':
                moves.append([r, c])
            else:
                # check if the piece is of opposite colour
                if board[r][c].islower() == (colour == 'black'):
                    moves.append([r, c])

    return moves

def checkSquaresAttacked(board, row, col):
    pos = [row, col]

    for a in range(8):
        for b in range(8):
            piece = board[a][b]
            if piece:
                colour = 'white' if piece.islower() else 'black'
                pieceMoves = []
                if piece.lower() == 'p':
                    pieceMoves = getPawnAttackMoves(board, a, b, colour)
                if piece.lower() == 'r':
                    pieceMoves = getRookMoves(board, a, b, colour)
                elif piece.lower() == 'n':
                    pieceMoves = getKnightMoves(board, a, b, colour)
                elif piece.lower() == 'b':
                    pieceMoves = getBishopMoves(board, a, b, colour)
                elif piece.lower() == 'q':
                    pieceMoves = getQueenMoves(board, a, b, colour)
                elif piece.lower() == 'k':
                    pieceMoves = getKingMoves(board, a, b, colour)
                if pos in pieceMoves:
                    return True
    return False


def findKing(board, colour):
    if colour == 'white':
        symbol = 'k'
    else:
        symbol = 'K'
    for row in range(8):
        for col in range(8):
            if board[row][col] == symbol:
                return [row, col]
            

def getPieceMoves(piece, row, col, wKingMoved, wKingRookMoved, wQueenRookMoved):
    if piece.isupper():
        colour = 'black'
    else:
        colour = 'white'

    if piece.lower() == 'p':
        x = removeIllegalMoves(board, row, col, colour, getPawnMoves(board, row, col, colour))
        y = removeIllegalMoves(board, row, col, colour, getPawnAttackMoves(board, row, col, colour))
        return (x + y)
    elif piece.lower() == 'n':
        return removeIllegalMoves(board, row, col, colour, (getKnightMoves(board, row, col, colour)))
    elif piece.lower() == 'b':
        return removeIllegalMoves(board, row, col, colour, (getBishopMoves(board, row, col, colour)))
    elif piece.lower() == 'r':
        return removeIllegalMoves(board, row, col, colour, (getRookMoves(board, row, col, colour)))
    elif piece.lower() == 'q':
        return removeIllegalMoves(board, row, col, colour, (getQueenMoves(board, row, col, colour)))
    elif piece.lower() == 'k':
        x = removeIllegalMoves(board, row, col, colour, (getKingMoves(board, row, col, colour)))
        # castling moves
        if colour == 'white':
            if canCastleKingSide(board, 'white', wKingMoved, wKingRookMoved):
                x.append([row, col + 2])
            if canCastleQueenSide(board, 'white', wKingMoved, wQueenRookMoved):
                x.append([row, col - 2])
        return x


def getColourMoves(board, colour):
    moves = []

    a = 0
    b = 0
    for row in board:
        for piece in row:
            if colour == 'black':
                if piece.isupper():
                    moves.append([[a, b], getPieceMoves(piece, a, b, True, True, True)])
            else:
                if piece.islower():
                    moves.append([[a, b], getPieceMoves(piece, a, b, True, True, True)])
            b += 1
        a += 1
        b = 0

    return moves


def checkmate(board):
    # if a colour has no moves, it means it is checkmate
    y = False
    blackMoves = getColourMoves(board, 'black')
    for x in blackMoves:
        if x[1] != []:
            y = True
    if not y:
        return True
    y = False
    whiteMoves = getColourMoves(board, 'white')
    for x in whiteMoves:
        if x[1] != []:
            y = True
    if not y:
        return True
    

def canCastleKingSide(board, colour, wKingMoved, wKingRookMoved):
    if colour == 'white':
        row = 7
    else:
        row = 0
    # check that there are no pieces in between
    if board[row][5] != '' or board[row][6] != '':
        return False
    # check if king or rook has moved
    if wKingRookMoved or wKingMoved:
        return False
    # check that the king and rook are on the right squares
    if board[7][4] != 'k' or board[7][7] != 'r':
        return False
    if checkSquaresAttacked(board, row, 4): # or checkSquaresAttacked(board, row, 5) or checkSquaresAttacked(board, row, 6):
        return False
    # temporarily fill in the empty squares so that we can check if the square is being attacked
    board[row][5] = 'k'
    board[row][6] = 'k'
    if checkSquaresAttacked(board, row, 5) or checkSquaresAttacked(board, row, 6):
        return False
    board[row][5] = ''
    board[row][6] = ''

    return True


def canCastleQueenSide(board, colour, wKingMoved, wQueenRookMoved):
    if colour == 'white':
        row = 7
    else:
        row = 0
    # check that there are no pieces in between
    if board[row][1] != '' or board[row][2] != '' or board[row][3] != '':
        return False
    # check if king or rook has moved
    if wKingMoved or wQueenRookMoved:
        return False
    # check that the king and rook are on the right squares
    if board[7][4] != 'k' or board[7][0] != 'r':
        return False
    # temporarily fill in squares in between so we can check if square is being attacked
    board[row][4] = 'k'
    board[row][3] = 'k'
    board[row][2] = 'k'
    if checkSquaresAttacked(board, row, 4) or checkSquaresAttacked(board, row, 3) or checkSquaresAttacked(board, row, 2):
        return False
    board[row][4] = ''
    board[row][3] = ''
    board[row][2] = ''
    return True
