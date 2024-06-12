from typing import List, Literal, Tuple, cast, Optional, Callable, Dict

try:
    from sema4ai.actions import action
except:
    action = lambda a: a
from enum import Enum


class Piece(Enum):
    PAWN_WHITE = "P"
    KNIGHT_WHITE = "N"
    BISHOP_WHITE = "B"
    ROOK_WHITE = "R"
    QUEEN_WHITE = "Q"
    KING_WHITE = "K"
    PAWN_BLACK = "p"
    KNIGHT_BLACK = "n"
    BISHOP_BLACK = "b"
    ROOK_BLACK = "r"
    QUEEN_BLACK = "q"
    KING_BLACK = "k"
    EMPTY = "1"


Board = List[List[Piece]]
Turn = Literal["w", "b"]
Castling = str  # 'KQkq', '-', etc.
EnPassant = str  # '-', 'e3', etc.
HalfmoveClock = int
FullmoveNumber = int

OPPONENT_PIECES: Dict[Turn, List[Piece]] = {
    "w": [
        Piece.PAWN_BLACK,
        Piece.KNIGHT_BLACK,
        Piece.BISHOP_BLACK,
        Piece.ROOK_BLACK,
        Piece.QUEEN_BLACK,
        Piece.KING_BLACK,
    ],
    "b": [
        Piece.PAWN_WHITE,
        Piece.KNIGHT_WHITE,
        Piece.BISHOP_WHITE,
        Piece.ROOK_WHITE,
        Piece.QUEEN_WHITE,
        Piece.KING_WHITE,
    ],
}


def parse_fen(
    fen: str,
) -> Tuple[Board, Turn, set, EnPassant, HalfmoveClock, FullmoveNumber]:
    """Parse FEN string into board matrix and other components."""
    parts = fen.split()
    raw_board = parts[0].split("/")
    board: Board = []

    piece_map = {
        "p": Piece.PAWN_BLACK,
        "r": Piece.ROOK_BLACK,
        "n": Piece.KNIGHT_BLACK,
        "b": Piece.BISHOP_BLACK,
        "q": Piece.QUEEN_BLACK,
        "k": Piece.KING_BLACK,
        "P": Piece.PAWN_WHITE,
        "R": Piece.ROOK_WHITE,
        "N": Piece.KNIGHT_WHITE,
        "B": Piece.BISHOP_WHITE,
        "Q": Piece.QUEEN_WHITE,
        "K": Piece.KING_WHITE,
    }

    for row in raw_board:
        expanded_row = []
        for char in row:
            if char.isdigit():
                expanded_row.extend([Piece.EMPTY] * int(char))
            else:
                expanded_row.append(piece_map[char])
        board.append(expanded_row)

    turn: Turn = cast(Turn, parts[1])
    castling: set = set(parts[2]) if parts[2] != "-" else set()
    en_passant: EnPassant = parts[3]
    halfmove_clock: HalfmoveClock = int(parts[4])
    fullmove_number: FullmoveNumber = int(parts[5])

    return board, turn, castling, en_passant, halfmove_clock, fullmove_number


def board_to_string(board: Board) -> str:
    """Convert board matrix to human-readable string with row and column indicators."""
    piece_symbols = {
        Piece.EMPTY: ".",
        Piece.PAWN_BLACK: "♟",
        Piece.ROOK_BLACK: "♜",
        Piece.KNIGHT_BLACK: "♞",
        Piece.BISHOP_BLACK: "♝",
        Piece.QUEEN_BLACK: "♛",
        Piece.KING_BLACK: "♚",
        Piece.PAWN_WHITE: "♙",
        Piece.ROOK_WHITE: "♖",
        Piece.KNIGHT_WHITE: "♘",
        Piece.BISHOP_WHITE: "♗",
        Piece.QUEEN_WHITE: "♕",
        Piece.KING_WHITE: "♔",
    }
    board_str = "  a b c d e f g h\n"
    for i, row in enumerate(board):
        board_str += str(8 - i) + " "
        for piece in row:
            board_str += piece_symbols.get(piece, piece) + " "
        board_str += str(8 - i) + "\n"
    board_str += "  a b c d e f g h\n"
    return board_str


@action
def display_board(fen: str) -> str:
    """
    Convert FEN string to a human-readable board representation.

    Args:
        fen (str): FEN string representing the board state.
            Example: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    Returns:
        str: Human-readable board representation.
            Example:
              a b c d e f g h
            8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 8
            7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 7
            6 . . . . . . . . 6
            5 . . . . . . . . 5
            4 . . . . . . . . 4
            3 . . . . . . . . 3
            2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ 2
            1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 1
              a b c d e f g h
    """
    board, turn, castling, en_passant, halfmove_clock, fullmove_number = parse_fen(fen)
    return board_to_string(board)


def generate_fen(
    board: Board,
    turn: str,
    castling: set,
    en_passant: str,
    halfmove_clock: int,
    fullmove_number: int,
) -> str:
    # Collapse board rows
    def collapse_row(row: list[Piece]) -> str:
        collapsed = ""
        count = 0
        for piece in row:
            if piece == Piece.EMPTY:
                count += 1
            else:
                if count > 0:
                    collapsed += str(count)
                    count = 0
                collapsed += piece.value
        if count > 0:
            collapsed += str(count)
        return collapsed

    collapsed_board = "/".join([collapse_row(row) for row in board])

    # Construct castling rights string from set
    castling_str = "".join(sorted(castling)) if castling else "-"

    # Generate new FEN string
    new_fen = f"{collapsed_board} {turn} {castling_str} {en_passant} {halfmove_clock} {fullmove_number}"

    return new_fen


@action
def apply_move(fen: str, reasoning: str, move: str) -> str:
    """
    Apply a move to the board represented by the FEN string and return the resulting FEN string.

    Args:
        fen (str): FEN string representing the board state.
            Example: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        reasoning (str): Text explaining the reasoning behind the move.
            Including but not limited to: Material Evaluation, Piece Activity, King Safety,
            Pawn Structure and evaluation of Control of Key Squares.
            Example: "This move is made to control the center and open lines for the bishop and queen."
        move (str): Move in standard algebraic notation (SAN). Example: "e2e4" (pawn move from e2 to e4)

    Returns:
        str: Resulting FEN string after applying the move.
            Example: "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    """
    board, turn, castling, en_passant, halfmove_clock, fullmove_number = parse_fen(fen)

    # Reasoning is enforced to improve LLM game.
    if len(reasoning) > 0:
        print(reasoning)

    parsed_move, promotion = parse_san_move(board, turn, move)
    if not parsed_move:
        return f"Invalid move: {move}"

    # Convert move to board indices
    start_col = ord(parsed_move[0]) - ord("a")
    start_row = 8 - int(parsed_move[1])
    end_col = ord(parsed_move[2]) - ord("a")
    end_row = 8 - int(parsed_move[3])

    # Apply the move
    piece = board[start_row][start_col]
    if piece == Piece.EMPTY:
        return f"Invalid move: {move}, start position is empty"
    generator = PIECE_MOVE_GENERATORS.get(piece)
    moves = generator(board, start_row, start_col, turn, en_passant, castling)
    if parsed_move not in moves:
        return f"Invalid move: {move}, not in pieces moves: {', '.join(moves)}"

    target_piece = board[end_row][end_col]

    # Handle castling
    if piece in [Piece.KING_WHITE, Piece.KING_BLACK] and abs(start_col - end_col) == 2:
        board = _apply_castling(board, start_row, end_col, turn)

        # Update castling rights
        if turn == "w":
            castling.discard("K")
            castling.discard("Q")
        else:
            castling.discard("k")
            castling.discard("q")
    else:
        board[start_row][start_col] = Piece.EMPTY
        board[end_row][end_col] = piece

        # Handle en passant capture
        board = _handle_en_passant_capture(board, move, en_passant, turn)

        # Update castling rights if rook or king moves
        if piece == Piece.KING_WHITE:
            castling.discard("K")
            castling.discard("Q")
        elif piece == Piece.KING_BLACK:
            castling.discard("k")
            castling.discard("q")
        elif piece == Piece.ROOK_WHITE and start_row == 7 and start_col == 0:
            castling.discard("Q")
        elif piece == Piece.ROOK_WHITE and start_row == 7 and start_col == 7:
            castling.discard("K")
        elif piece == Piece.ROOK_BLACK and start_row == 0 and start_col == 0:
            castling.discard("q")
        elif piece == Piece.ROOK_BLACK and start_row == 0 and start_col == 7:
            castling.discard("k")

    # Update en passant target square
    if piece in [Piece.PAWN_WHITE, Piece.PAWN_BLACK] and abs(start_row - end_row) == 2:
        en_passant = f"{parsed_move[2]}{8 - (start_row + end_row) // 2}"
    else:
        en_passant = "-"

    # Update halfmove clock and fullmove number
    if piece in [Piece.PAWN_WHITE, Piece.PAWN_BLACK] or target_piece != Piece.EMPTY:
        halfmove_clock = 0
    else:
        halfmove_clock += 1

    # Update turn and fullmove number
    if turn == "w":
        turn = "b"
    else:
        turn = "w"
        fullmove_number += 1

    # Generate new FEN string using the extracted function
    return generate_fen(
        board, turn, castling, en_passant, halfmove_clock, fullmove_number
    )


def parse_san_move(
    board: Board, turn: Turn, san_move: str
) -> Tuple[Optional[str], Optional[str]]:
    piece_map = {
        "P": Piece.PAWN_WHITE,
        "R": Piece.ROOK_WHITE,
        "N": Piece.KNIGHT_WHITE,
        "B": Piece.BISHOP_WHITE,
        "Q": Piece.QUEEN_WHITE,
        "K": Piece.KING_WHITE,
        "p": Piece.PAWN_BLACK,
        "r": Piece.ROOK_BLACK,
        "n": Piece.KNIGHT_BLACK,
        "b": Piece.BISHOP_BLACK,
        "q": Piece.QUEEN_BLACK,
        "k": Piece.KING_BLACK,
    }

    # Check if the move is already in [start position][end position] format
    if (
        len(san_move) == 4
        and san_move[0].isalpha()
        and san_move[1].isdigit()
        and san_move[2].isalpha()
        and san_move[3].isdigit()
    ):
        return san_move, None

    piece = "P"  # Default to pawn
    if san_move[0] in "RNBQK":
        piece = san_move[0]
        san_move = san_move[1:]

    capture = "x" in san_move
    promotion = None
    if "=" in san_move:
        san_move, promotion = san_move.split("=")

    end_square = san_move[-2:]
    san_move = san_move[:-2]

    start_file = None
    start_rank = None
    if len(san_move) == 1:
        if san_move.isdigit():
            start_rank = int(san_move)
        else:
            start_file = san_move
    elif len(san_move) == 2:
        start_file, start_rank = san_move

    piece_enum = piece_map[piece.upper()] if turn == "w" else piece_map[piece.lower()]
    possible_moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece_enum:
                move_generator = PIECE_MOVE_GENERATORS.get(piece_enum)
                if move_generator:
                    piece_moves = move_generator(board, row, col, turn, "", set())
                    for move in piece_moves:
                        if move[2:4] == end_square:
                            if (start_file is None or start_file == move[0]) and (
                                start_rank is None or start_rank == move[1]
                            ):
                                possible_moves.append(move)

    for move in possible_moves:
        start_col = ord(move[0]) - ord("a")
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord("a")
        end_row = 8 - int(move[3])

        if board[end_row][end_col] in [Piece.EMPTY, *OPPONENT_PIECES[turn]]:
            return move, promotion

    return None, None


class Move:
    def __init__(self, piece, start_square, end_square, promotion=None, castling=None):
        self.piece = piece
        self.start_square = start_square
        self.end_square = end_square
        self.promotion = promotion
        self.castling = castling

    def __str__(self):
        return f"{self.piece}{self.start_square}{self.end_square}{self.promotion or ''}{self.castling or ''}"


def parse_move_string(move_str: str, fen: str) -> Move:
    """
    Parse a move string in standard algebraic notation and return a Move object.

    Args:
        move_str (str): Move in standard algebraic notation.
        fen (str): FEN string representing the current board state.

    Returns:
        Move: Move object with parsed information.
    """
    board, turn, _, _, _, _ = parse_fen(fen)

    # Handle castling
    if move_str in ["O-O", "O-O-O"]:
        return Move(piece="K", start_square=None, end_square=None, castling=move_str)

    # Determine piece type
    piece = "P"  # Default to pawn
    if move_str[0] in "RNBQK":
        piece = move_str[0]
        move_str = move_str[1:]

    # Handle promotion
    promotion = None
    if "=" in move_str:
        move_str, promotion = move_str.split("=")
        promotion = promotion.upper()

    # Parse the end square
    end_square = move_str[-2:]
    move_str = move_str[:-2]

    # Determine the start square
    if len(move_str) == 2:
        start_square = move_str
    else:
        start_square = (
            None  # This would be determined by board state and disambiguation logic
        )

    return Move(
        piece=piece,
        start_square=start_square,
        end_square=end_square,
        promotion=promotion,
    )


def _handle_en_passant_capture(
    board: Board, move: str, en_passant: str, turn: str
) -> Board:
    if en_passant != "-" and move[2:4] == en_passant:
        end_col = ord(move[2]) - ord("a")
        capture_row = (8 - int(en_passant[1])) + (1 if turn == "w" else -1)

        board[capture_row][end_col] = Piece.EMPTY

    return board


def _apply_castling(board: Board, start_row: int, end_col: int, turn: Turn) -> Board:
    if end_col > 4:  # Kingside castling
        # Move king to g1/g8 and rook to f1/f8
        board[start_row][4] = Piece.EMPTY
        board[start_row][7] = Piece.EMPTY
        board[start_row][6] = Piece.KING_WHITE if turn == "w" else Piece.KING_BLACK
        board[start_row][5] = Piece.ROOK_WHITE if turn == "w" else Piece.ROOK_BLACK
    else:  # Queenside castling
        # Move king to c1/c8 and rook to d1/d8
        board[start_row][4] = Piece.EMPTY
        board[start_row][0] = Piece.EMPTY
        board[start_row][2] = Piece.KING_WHITE if turn == "w" else Piece.KING_BLACK
        board[start_row][3] = Piece.ROOK_WHITE if turn == "w" else Piece.ROOK_BLACK

    return board


def _generate_pawn_moves(
    board: Board, row: int, col: int, turn: Turn, en_passant: str, castling: set
) -> List[str]:
    """Generate all legal pawn moves for a given position."""
    moves = []
    direction = -1 if turn == "w" else 1
    start_row = 6 if turn == "w" else 1
    opponent_pieces = OPPONENT_PIECES[turn]

    # Move forward
    if board[row + direction][col] == Piece.EMPTY:
        moves.append(
            f"{chr(col + ord('a'))}{8 - row}{chr(col + ord('a'))}{8 - (row + direction)}"
        )
        if row == start_row and board[row + 2 * direction][col] == Piece.EMPTY:
            moves.append(
                f"{chr(col + ord('a'))}{8 - row}{chr(col + ord('a'))}{8 - (row + 2 * direction)}"
            )

    # Capture diagonally to the left
    if col > 0 and board[row + direction][col - 1] in opponent_pieces:
        moves.append(
            f"{chr(col + ord('a'))}{8 - row}{chr(col - 1 + ord('a'))}{8 - (row + direction)}"
        )
    # Capture diagonally to the right
    if col < 7 and board[row + direction][col + 1] in opponent_pieces:
        moves.append(
            f"{chr(col + ord('a'))}{8 - row}{chr(col + 1 + ord('a'))}{8 - (row + direction)}"
        )

    # En passant
    if en_passant != "-" and int(en_passant[1]) == 8 - (row + direction):
        en_passant_col = ord(en_passant[0]) - ord("a")
        if col in [en_passant_col - 1, en_passant_col + 1]:
            moves.append(f"{chr(col + ord('a'))}{8 - row}{en_passant}")

    return moves


def _generate_knight_moves(
    board: Board, row: int, col: int, turn: Turn, en_passant: str, castling: set
) -> List[str]:
    """Generate all legal knight moves for a given position."""
    moves = []
    knight_moves = [
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
    ]
    opponent_pieces = OPPONENT_PIECES[turn]
    for dr, dc in knight_moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if (
                board[new_row][new_col] == Piece.EMPTY
                or board[new_row][new_col] in opponent_pieces
            ):
                moves.append(
                    f"{chr(col + ord('a'))}{8 - row}{chr(new_col + ord('a'))}{8 - new_row}"
                )
    return moves


def _generate_bishop_moves(
    board: Board, row: int, col: int, turn: Turn, en_passant: str, castling: set
) -> List[str]:
    """Generate all legal bishop moves for a given position."""
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    opponent_pieces = OPPONENT_PIECES[turn]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        while 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == Piece.EMPTY:
                moves.append(
                    f"{chr(col + ord('a'))}{8 - row}{chr(new_col + ord('a'))}{8 - new_row}"
                )
            elif board[new_row][new_col] in opponent_pieces:
                moves.append(
                    f"{chr(col + ord('a'))}{8 - row}{chr(new_col + ord('a'))}{8 - new_row}"
                )
                break
            else:
                break
            new_row += dr
            new_col += dc

    return moves


def _generate_rook_moves(
    board: Board, row: int, col: int, turn: Turn, en_passant: str, castling: set
) -> List[str]:
    """Generate all legal rook moves for a given position."""
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    opponent_pieces = OPPONENT_PIECES[turn]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        while 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == Piece.EMPTY:
                moves.append(
                    f"{chr(col + ord('a'))}{8 - row}{chr(new_col + ord('a'))}{8 - new_row}"
                )
            elif board[new_row][new_col] in opponent_pieces:
                moves.append(
                    f"{chr(col + ord('a'))}{8 - row}{chr(new_col + ord('a'))}{8 - new_row}"
                )
                break
            else:
                break
            new_row += dr
            new_col += dc

    return moves


def _generate_queen_moves(
    board: Board, row: int, col: int, turn: Turn, en_passant: str, castling: set
) -> List[str]:
    """Generate all legal queen moves for a given position."""
    return _generate_bishop_moves(
        board, row, col, turn, en_passant, castling
    ) + _generate_rook_moves(board, row, col, turn, en_passant, castling)


def _generate_king_moves(
    board: Board, row: int, col: int, turn: Turn, en_passant: str, castling: set
) -> List[str]:
    """Generate all legal king moves for a given position."""
    moves = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    opponent_pieces = OPPONENT_PIECES[turn]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if (
                board[new_row][new_col] == Piece.EMPTY
                or board[new_row][new_col] in opponent_pieces
            ):
                moves.append(
                    f"{chr(col + ord('a'))}{8 - row}{chr(new_col + ord('a'))}{8 - new_row}"
                )

    def is_square_attacked(
        board: Board, square_row: int, square_col: int, opponent_turn: Turn
    ) -> bool:
        # Check for king attacks directly
        king_piece = Piece.KING_WHITE if opponent_turn == "w" else Piece.KING_BLACK
        for dr, dc in directions:
            row, col = square_row + dr, square_col + dc
            if 0 <= row < 8 and 0 <= col < 8 and board[row][col] == king_piece:
                return True

        # Check for attacks from other pieces
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece in opponent_pieces and piece not in [
                    Piece.KING_WHITE,
                    Piece.KING_BLACK,
                ]:
                    move_generator = PIECE_MOVE_GENERATORS.get(piece)
                    for move in move_generator(board, r, c, opponent_turn, "-", set()):
                        if move[2:4] == f"{chr(square_col + ord('a'))}{8 - square_row}":
                            return True
        return False

    # Castling
    opponent_turn = cast(Turn, "b" if turn == "w" else "w")
    if turn == "w" and row == 7 and col == 4:
        if "K" in castling and board[7][5] == board[7][6] == Piece.EMPTY:
            if (
                not is_square_attacked(board, 7, 4, opponent_turn)
                and not is_square_attacked(board, 7, 5, opponent_turn)
                and not is_square_attacked(board, 7, 6, opponent_turn)
            ):
                moves.append("e1g1")
        if "Q" in castling and board[7][1] == board[7][2] == board[7][3] == Piece.EMPTY:
            if (
                not is_square_attacked(board, 7, 4, opponent_turn)
                and not is_square_attacked(board, 7, 3, opponent_turn)
                and not is_square_attacked(board, 7, 2, opponent_turn)
            ):
                moves.append("e1c1")
    elif turn == "b" and row == 0 and col == 4:
        if "k" in castling and board[0][5] == board[0][6] == Piece.EMPTY:
            if (
                not is_square_attacked(board, 0, 4, opponent_turn)
                and not is_square_attacked(board, 0, 5, opponent_turn)
                and not is_square_attacked(board, 0, 6, opponent_turn)
            ):
                moves.append("e8g8")
        if "q" in castling and board[0][1] == board[0][2] == board[0][3] == Piece.EMPTY:
            if (
                not is_square_attacked(board, 0, 4, opponent_turn)
                and not is_square_attacked(board, 0, 3, opponent_turn)
                and not is_square_attacked(board, 0, 2, opponent_turn)
            ):
                moves.append("e8c8")

    return moves


# Mapping pieces to their corresponding move generation functions
PIECE_MOVE_GENERATORS: Dict[Piece, Callable] = {
    Piece.PAWN_WHITE: _generate_pawn_moves,
    Piece.PAWN_BLACK: _generate_pawn_moves,
    Piece.KNIGHT_WHITE: _generate_knight_moves,
    Piece.KNIGHT_BLACK: _generate_knight_moves,
    Piece.BISHOP_WHITE: _generate_bishop_moves,
    Piece.BISHOP_BLACK: _generate_bishop_moves,
    Piece.ROOK_WHITE: _generate_rook_moves,
    Piece.ROOK_BLACK: _generate_rook_moves,
    Piece.QUEEN_WHITE: _generate_queen_moves,
    Piece.QUEEN_BLACK: _generate_queen_moves,
    Piece.KING_WHITE: _generate_king_moves,
    Piece.KING_BLACK: _generate_king_moves,
}


@action
def generate_legal_moves(fen: str) -> str:
    """
    Generate all legal moves for the board represented by the FEN string.

    Args:
        fen (str): FEN string representing the board state.
            Example: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    Returns:
        str: List of legal moves in standard algebraic notation.
            Example: "e2e4, g1f3, d2d4"
    """
    board, turn, castling, en_passant, halfmove_clock, fullmove_number = parse_fen(fen)
    legal_moves = []

    # Iterate through the board and generate moves for each piece
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != Piece.EMPTY and (
                (turn == "w" and piece.value.isupper())
                or (turn == "b" and piece.value.islower())
            ):
                move_generator = PIECE_MOVE_GENERATORS.get(piece)
                if move_generator:
                    piece_moves = move_generator(
                        board, row, col, turn, en_passant, castling
                    )
                    legal_moves.extend(piece_moves)

    # Filter out moves that leave the king in check
    valid_moves = []
    for move in legal_moves:
        # Apply the move to get a new board state
        test_fen = apply_move(fen, "", move)
        (
            new_board,
            new_turn,
            new_castling,
            new_en_passant,
            new_halfmove_clock,
            new_fullmove_number,
        ) = parse_fen(test_fen)
        if not _is_in_check(new_board, turn):
            valid_moves.append(move)

    if len(valid_moves) == 0:
        return "No legal moves"

    return ", ".join(valid_moves)


def get_first_position(board: Board, piece: Piece) -> Optional[Tuple[int, int]]:
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece:
                return row, col
    return None


def is_attacked_by_pawn(
    board: Board, king_pos: Tuple[int, int], pawn_piece: Piece, direction: int
) -> bool:
    king_row, king_col = king_pos
    for dc in [-1, 1]:
        row, col = king_row + direction, king_col + dc
        if 0 <= row < 8 and 0 <= col < 8 and board[row][col] == pawn_piece:
            return True
    return False


def is_attacked_by_knight(
    board: Board, king_pos: Tuple[int, int], knight_piece: Piece
) -> bool:
    king_row, king_col = king_pos
    knight_moves = [
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
    ]
    return any(
        0 <= king_row + dr < 8
        and 0 <= king_col + dc < 8
        and board[king_row + dr][king_col + dc] == knight_piece
        for dr, dc in knight_moves
    )


def is_attacked_by_sliding_piece(
    board: Board,
    king_pos: Tuple[int, int],
    directions: List[Tuple[int, int]],
    attackers: List[Piece],
) -> bool:
    king_row, king_col = king_pos
    for dr, dc in directions:
        row, col = king_row + dr, king_col + dc
        while 0 <= row < 8 and 0 <= col < 8:
            piece = board[row][col]
            if piece != Piece.EMPTY:
                if piece in attackers:
                    return True
                break
            row += dr
            col += dc
    return False


def is_attacked_by_king(
    board: Board, king_pos: Tuple[int, int], enemy_king: Piece
) -> bool:
    king_row, king_col = king_pos
    return any(
        0 <= king_row + dr < 8
        and 0 <= king_col + dc < 8
        and board[king_row + dr][king_col + dc] == enemy_king
        for dr in range(-1, 2)
        for dc in range(-1, 2)
        if dr != 0 or dc != 0
    )


def _is_in_check(board: Board, turn: Turn) -> bool:
    king_piece = Piece.KING_WHITE if turn == "w" else Piece.KING_BLACK
    pawn_piece = Piece.PAWN_BLACK if turn == "w" else Piece.PAWN_WHITE
    knight_piece = Piece.KNIGHT_BLACK if turn == "w" else Piece.KNIGHT_WHITE
    bishop_piece = Piece.BISHOP_BLACK if turn == "w" else Piece.BISHOP_WHITE
    rook_piece = Piece.ROOK_BLACK if turn == "w" else Piece.ROOK_WHITE
    queen_piece = Piece.QUEEN_BLACK if turn == "w" else Piece.QUEEN_WHITE
    enemy_king_piece = Piece.KING_BLACK if turn == "w" else Piece.KING_WHITE

    king_pos = get_first_position(board, king_piece)
    if not king_pos:
        return False

    direction = -1 if turn == "w" else 1

    return (
        is_attacked_by_pawn(board, king_pos, pawn_piece, direction)
        or is_attacked_by_knight(board, king_pos, knight_piece)
        or is_attacked_by_sliding_piece(
            board,
            king_pos,
            [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            [bishop_piece, queen_piece],
        )
        or is_attacked_by_sliding_piece(
            board,
            king_pos,
            [(-1, 0), (1, 0), (0, -1), (0, 1)],
            [rook_piece, queen_piece],
        )
        or is_attacked_by_king(board, king_pos, enemy_king_piece)
    )


def test_initial_position():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    legal_moves = generate_legal_moves(fen)
    assert "e2e4" in legal_moves
    assert "g1f3" in legal_moves


def test_pawn_move():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    new_fen = apply_move(fen, "", "e2e4")
    expected_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    assert new_fen == expected_fen, new_fen


def test_knight_move():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    new_fen = apply_move(fen, "", "g1f3")
    expected_fen = "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1"
    assert new_fen == expected_fen, new_fen


def test_pawn_capture():
    fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    new_fen = apply_move(fen, "", "d7d5")
    new_fen = apply_move(new_fen, "", "e4d5")
    expected_fen = "rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2"
    assert new_fen == expected_fen, new_fen


def test_castling():
    # White kingside castling
    fen = "rnbq1rk1/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQK2R w KQ - 0 1"
    new_fen = apply_move(fen, "", "e1g1")
    expected_fen = "rnbq1rk1/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQ1RK1 b - - 1 1"
    assert new_fen == expected_fen, new_fen

    # White queenside castling
    fen = "r3k2r/pppqppbp/2np1np1/4P3/2P1P3/2N2N2/PPQB1PPP/R3K2R w KQkq - 0 1"
    new_fen = apply_move(fen, "", "e1c1")
    expected_fen = "r3k2r/pppqppbp/2np1np1/4P3/2P1P3/2N2N2/PPQB1PPP/2KR3R b kq - 1 1"
    assert new_fen == expected_fen, new_fen

    # Black kingside castling
    fen = "rnbqk2r/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQ1RK1 b kq - 1 1"
    new_fen = apply_move(fen, "", "e8g8")
    expected_fen = "rnbq1rk1/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQ1RK1 w - - 2 2"
    assert new_fen == expected_fen, new_fen

    # Black queenside castling
    fen = "r3k2r/pppqppbp/2np1np1/4P3/2P1P3/2N2N2/PPQB1PPP/R3K2R b KQkq - 6 5"
    new_fen = apply_move(fen, "", "e8c8")
    expected_fen = "2kr3r/pppqppbp/2np1np1/4P3/2P1P3/2N2N2/PPQB1PPP/R3K2R w KQ - 7 6"
    assert new_fen == expected_fen, new_fen


def test_check_validation():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    try:
        apply_move(fen, "", "e2e4")
        apply_move(fen, "", "d7d5")
        apply_move(fen, "", "e4e5")
        apply_move(fen, "", "d5d4")
        apply_move(fen, "", "e5e6")
    except ValueError as e:
        assert str(e) == "Move leaves king in check: e5e6"


def test_en_passant():
    # Initial FEN before any moves
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen = apply_move(fen, "", "e2e4")
    fen = apply_move(fen, "", "f7f5")
    fen = apply_move(fen, "", "e4f5")
    fen = apply_move(fen, "", "e7e5")
    fen = apply_move(fen, "", "f5e6")
    expected_fen = "rnbqkbnr/pppp2pp/4P3/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 3"
    assert fen == expected_fen, fen


def test_invalid_move():
    # Invalid move: Pawn trying to move two squares forward not from the starting position
    fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    result = apply_move(fen, "", "e4e6")
    assert result == "Invalid move: e4e6, not in pieces moves: e4e5", result

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    # Invalid move: Bishop trying to move like a knight
    result = apply_move(fen, "", "Bc3")
    assert result == "Invalid move: Bc3", result


def test_valid_san_move():
    fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2"
    expected_fen = apply_move(fen, "", "d1h5")
    assert "Invalid" not in expected_fen
    assert apply_move(fen, "", "Qd1h5") == expected_fen
    assert apply_move(fen, "", "Qh5") == expected_fen
    assert apply_move(fen, "", "Qd1-h5") == expected_fen


def test_legal_moves():
    fen = "rnbqkbnr/pp1ppppp/2p5/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq d3 0 2"
    moves = generate_legal_moves(fen)
    assert len(moves.split(", ")) == 21


if __name__ == "__main__":
    # Run tests
    test_initial_position()
    test_pawn_move()
    test_knight_move()
    test_pawn_capture()
    test_check_validation()
    test_en_passant()
    test_castling()
    test_invalid_move()
    test_valid_san_move()
    test_legal_moves()

    print("All tests passed.")
