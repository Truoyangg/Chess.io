import pygame as p
import chessAI
import chessMoves
import time



BOARD_SIZE = 560
DIMENSION = 8  # 8*8 CHESS BOARD
CELL_SIZE = BOARD_SIZE // DIMENSION

IMAGES = {}
DISPLACEMENT = 0
p.display.set_caption("CHESS")

maxFPS = 12 # Default
setting = 0 # Default
# Load Images for pieces
def loadImages():
    pieces = ['bp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (CELL_SIZE, CELL_SIZE))

def chooseMode():
    p.init()
    screen = p.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    font = p.font.SysFont("Arial", 50)
    title_font = p.font.SysFont("Arial", 70)
    clock = p.time.Clock()

    humanPlayWhite = True
    humanPlayBlack = False
    maxFPS = 12
    selectedDif = 0

    running = True

    while running:
        screen.fill(p.Color("white"))

        title_text = title_font.render("Chess", True, p.Color("black"))
        screen.blit(title_text, ((BOARD_SIZE - title_text.get_width()) // 2, 20))

        # Create buttons
        play_with_bot_button = p.Rect(BOARD_SIZE // 4, BOARD_SIZE // 4, BOARD_SIZE // 2, 60)
        pvp_button = p.Rect(BOARD_SIZE // 4, BOARD_SIZE // 2, BOARD_SIZE // 2, 60)
        settings_button = p.Rect(BOARD_SIZE // 4, BOARD_SIZE // 1.5, BOARD_SIZE // 2, 60)  # New settings button

        # Draw buttons
        p.draw.rect(screen, p.Color("green"), play_with_bot_button)
        p.draw.rect(screen, p.Color("blue"), pvp_button)
        p.draw.rect(screen, p.Color("orange"), settings_button)  # Draw settings button

        # Add text to buttons
        play_with_bot_text = font.render("Play with BOT", True, p.Color("black"))
        pvp_text = font.render("PVP", True, p.Color("black"))
        settings_text = font.render("Settings", True, p.Color("black"))  # Settings button text
        screen.blit(play_with_bot_text, (play_with_bot_button.x + (play_with_bot_button.width - play_with_bot_text.get_width()) // 2, play_with_bot_button.y + (play_with_bot_button.height - play_with_bot_text.get_height()) // 2))
        screen.blit(pvp_text, (pvp_button.x + (pvp_button.width - pvp_text.get_width()) // 2, pvp_button.y + (pvp_button.height - pvp_text.get_height()) // 2))
        screen.blit(settings_text, (settings_button.x + (settings_button.width - settings_text.get_width()) // 2, settings_button.y + (settings_button.height - settings_text.get_height()) // 2))  # Center text

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                if play_with_bot_button.collidepoint(mouse_pos):
                    humanPlayWhite = True
                    humanPlayBlack = False
                    selectedDif = 1  # Set to 1 for playing with BOT
                    print("Play with BOT")
                    return humanPlayWhite, humanPlayBlack, selectedDif
                elif pvp_button.collidepoint(mouse_pos):
                    humanPlayWhite = True
                    humanPlayBlack = True
                    print("PVP")
                    return humanPlayWhite, humanPlayBlack, selectedDif
                elif settings_button.collidepoint(mouse_pos):
                    setting = 1
                    maxFPS = chooseFPS()
        clock.tick(30)
        p.display.flip()

def chooseFPS():
    p.init()
    screen = p.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    font = p.font.SysFont("Arial", 50)
    title_font = p.font.SysFont("Arial", 70)
    clock = p.time.Clock()

    running = True
    fps_options = [12, 30, 60]
    selected_fps_index = 0  # Default FPS

    while running:
        screen.fill(p.Color("white"))
        title_text = title_font.render("Select FPS", True, p.Color("black"))
        screen.blit(title_text, ((BOARD_SIZE - title_text.get_width()) // 2, 20))

        # Display FPS options
        for i, fps in enumerate(fps_options):
            color = p.Color("black") if i == selected_fps_index else p.Color("gray")
            fps_text = font.render(f"{fps} FPS", True, color)
            screen.blit(fps_text, (BOARD_SIZE // 4, BOARD_SIZE // 4 + i * 60))

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.KEYDOWN:
                # Using key
                if event.key == p.K_UP:
                    selected_fps_index = (selected_fps_index - 1) % len(fps_options)
                elif event.key == p.K_DOWN:
                    selected_fps_index = (selected_fps_index + 1) % len(fps_options) 
                elif event.key == p.K_RETURN:  # Confirm selection
                    print(f"Selected FPS: {fps_options[selected_fps_index]}")
                    return fps_options[selected_fps_index]  # Return  FPS

        clock.tick(30)
        p.display.flip()

def chooseDif():
    p.init()
    screen = p.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    font = p.font.SysFont("Arial", 50)
    title_font = p.font.SysFont("Arial", 70)
    clock = p.time.Clock()

    selectedDepth = 0
    running = True

    while running:
        screen.fill(p.Color("white"))
        title_text = title_font.render("Select Difficulty", True, p.Color("black"))
        screen.blit(title_text, ((BOARD_SIZE - title_text.get_width()) // 2, 20))

        # Create diff but
        easy_button = p.Rect(BOARD_SIZE // 4, BOARD_SIZE // 1.8, BOARD_SIZE // 2, 60)
        medium_button = p.Rect(BOARD_SIZE // 4, BOARD_SIZE // 1.5, BOARD_SIZE // 2, 60)
        hard_button = p.Rect(BOARD_SIZE // 4, BOARD_SIZE // 1.3, BOARD_SIZE // 2, 60)

        p.draw.rect(screen, p.Color("orange"), easy_button)
        p.draw.rect(screen, p.Color("orange"), medium_button)
        p.draw.rect(screen, p.Color("orange"), hard_button)

        easy_text = font.render("Easy", True, p.Color("black"))
        medium_text = font.render("Medium", True, p.Color("black"))
        hard_text = font.render("Hard", True, p.Color("black"))

        screen.blit(easy_text, (easy_button.x + (easy_button.width - easy_text.get_width()) // 2, easy_button.y + (easy_button.height - easy_text.get_height()) // 2))
        screen.blit(medium_text, (medium_button.x + (medium_button.width - medium_text.get_width()) // 2, medium_button.y + (medium_button.height - medium_text.get_height()) // 2))
        screen.blit(hard_text, (hard_button.x + (hard_button.width - hard_text.get_width()) // 2, hard_button.y + (hard_button.height - hard_text.get_height()) // 2))

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    print("Easy mode")
                    return 1 # Easy
                elif medium_button.collidepoint(mouse_pos):
                    print("Medium mode")
                    return 2  # Medium
                elif hard_button.collidepoint(mouse_pos):
                    print("Hardcore")
                    return 3 # Hard
                return selectedDepth

        clock.tick(30)
        p.display.flip()


def main():
    humanPlayWhite, humanPlayBlack, selectedDif = chooseMode()
    selectedDepth = 0

    if not humanPlayBlack:  # If PVE
        selectedDepth = chooseDif()
        print(f"Difficulty: {selectedDepth}")
        chessAI.set_depth(selectedDepth)  # intelligence of AI link to chessAI


    # Initialize game components
    screen = p.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    p.display.set_caption("Chess")
    font = p.font.SysFont("Arial", 50)
    clock = p.time.Clock()
    
    gs = chessMoves.GameState()  # Initialize game state
    loadImages()

    animationCheck = False
    moveMade = False
    running = True
    sqSelected = ()
    playerClicks = []
    possibleMoves = gs.getPossibleMoves()
    
    isMate = False
    
    while running:
        screen.fill(p.Color("white"))
        
        # Draw the game state (board, pieces, etc.)
        drawGameState(screen, gs, possibleMoves, sqSelected)
        
        # Handle player move
        humanToPlay = (gs.whiteToMove and humanPlayWhite) or (not gs.whiteToMove and humanPlayBlack)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not isMate and humanToPlay:
                    location = p.mouse.get_pos()
                    col = location[0] // CELL_SIZE
                    row = location[1] // CELL_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = chessMoves.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(possibleMoves)):
                                if move == possibleMoves[i]:
                                    gs.makeMove(move)
                                    if gs.isDrawByRepetition():
                                        gs.draw = True
                                    moveMade = True
                                    animationCheck = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
    
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.unMakeMove()
                    moveMade = True
                    isMate = False
                    animationCheck = False

        if not isMate and not humanToPlay:
            startTime = time.time()
            AI_move = chessAI.getTheMove(gs, possibleMoves)
            endTime = time.time()
            # executionTime = endTime - startTime
            # print(f"It took {executionTime} to run")
            print (f"It's your turn!")
            if AI_move == None:
                AI_move = chessAI.getRandomMoves(possibleMoves)
            gs.makeMove(AI_move)
            if gs.isDrawByRepetition():
                gs.draw = True
            moveMade = True    
            animationCheck = True

        if moveMade:
            if animationCheck:
                animationCheck = False
                animate(gs.moveLog[-1], screen, gs.board, clock)
            possibleMoves = gs.getPossibleMoves()
            moveMade = False
            
        drawGameState(screen, gs, possibleMoves, sqSelected)
        
        if gs.checkMate:
            isMate = True
            if gs.whiteToMove:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
            
        elif gs.staleMate:
            isMate = True
            draw_text(screen, "Draw by stalemate")
        
        elif gs.draw:
            isMate = True
            draw_text(screen, "Draw by repetitions")
            
        clock.tick(maxFPS)
        p.display.flip()

# Responsible for all the graphics in the game
def drawGameState(screen, gs, possibleMoves, sqSelected):
    drawBoard(screen)
    displayLastMove(screen, gs)
    hightlightSquare(screen, gs, possibleMoves, sqSelected)
    hightlightChecks(screen, gs)
    drawPieces(screen, gs.board)

# Draw the squares on the board
def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(CELL_SIZE*c, CELL_SIZE*r , CELL_SIZE, CELL_SIZE))

# Draw the pieces on the board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(CELL_SIZE*c, CELL_SIZE*r , CELL_SIZE, CELL_SIZE))

def draw_text(screen ,string):
    font = p.font.SysFont('Helvitica', 50, True, False)
    textObject = font.render(string, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_SIZE, BOARD_SIZE).move(BOARD_SIZE / 2 - textObject.get_width() / 2, BOARD_SIZE / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)

def animate(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 8
    
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame / frameCount) 
        drawBoard(screen)
        drawPieces(screen, board)
        
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * CELL_SIZE, move.endRow * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        p.draw.rect(screen, color, endSquare)
        
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, BOARD_SIZE))
        p.display.flip()
        clock.tick(60)

def hightlightSquare(screen, gs, possibleMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if (gs.board[r][c][0] == 'w' and gs.whiteToMove) or (gs.board[r][c][0] == 'b' and not gs.whiteToMove):
            s = p.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(70)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * CELL_SIZE, r * CELL_SIZE))
            s.fill(p.Color('green'))
            
            for move in possibleMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (CELL_SIZE * move.endCol, CELL_SIZE * move.endRow))
                    
def hightlightChecks(screen, gs):
    r, c = -1, -1
    if gs.whiteToMove:
        if gs.isAttacked(gs.whiteKingLocation[0], gs.whiteKingLocation[1]):
            r, c = gs.whiteKingLocation
    else:
        if gs.isAttacked(gs.blackKingLocation[0], gs.blackKingLocation[1]):
            r, c = gs.blackKingLocation
    
    if r != -1 and c != -1:
        s = p.Surface((CELL_SIZE, CELL_SIZE))
        s.fill(p.Color('red'))
        screen.blit(s, (c * CELL_SIZE, r * CELL_SIZE))

def displayLastMove(screen, gs):
    if len(gs.moveLog) != 0:
        startRow = gs.moveLog[-1].startRow
        startCol = gs.moveLog[-1].startCol
        endRow = gs.moveLog[-1].endRow
        endCol = gs.moveLog[-1].endCol
        
        s = p.Surface((CELL_SIZE, CELL_SIZE))
        s.fill(p.Color('yellow'))
        screen.blit(s, (startCol * CELL_SIZE, startRow * CELL_SIZE))
        screen.blit(s, (endCol * CELL_SIZE, endRow * CELL_SIZE))

if __name__ == "__main__":
    main()
