import chess
import chess.svg
import pygame
from io import BytesIO
import random
import cairosvg

def evaluate(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    score = 0
    for piece_type in piece_values:
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    return score if board.turn == chess.WHITE else -score


def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate(board) + random.randint(-10, 10), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, False, alpha, beta)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, True, alpha, beta)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def ai_move(board):
    _, best_move = minimax(board, 5, False, float('-inf'), float('inf'))  # Change depth to 3 or higher
    return best_move



def render_board(screen, board):
    board_svg = chess.svg.board(board=board, size=400)
    png_file = BytesIO()
    cairosvg.svg2png(bytestring=board_svg.encode("utf-8"), write_to=png_file)
    png_file.seek(0)
    png_surface = pygame.image.load(png_file, "PNG")
    screen.blit(png_surface, (0, 0))

def main():
    pygame.init()
    pygame.display.set_caption("Chess AI")
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    board = chess.Board()
    user_turn = True
    running = True
    selected_piece = None
    while running and not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and user_turn:
                # Convert the screen coordinates to chess board coordinates
                x, y = pygame.mouse.get_pos()
                file, rank = x // 50, (7 - y // 50)
                square = chess.square(file, rank)

                # Toggle the selected piece or make a move
                if board.piece_at(square) and board.piece_at(square).color == board.turn:
                    selected_piece = square
                elif selected_piece is not None:
                    move = chess.Move(selected_piece, square)
                    if move in board.legal_moves:
                        board.push(move)
                        user_turn = False
                        selected_piece = None

        if not user_turn and not board.is_game_over():
            move = ai_move(board)
            if move is not None:
                board.push(move)
                user_turn = True

        render_board(screen, board)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
