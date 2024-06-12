# ChessActions

The `ChessActions` package provides a comprehensive set of actions for parsing, displaying, and managing chess games using FEN (Forsyth-Edwards Notation) strings. This package includes functionalities to parse FEN strings, display chess boards, generate legal moves, and apply moves using standard algebraic notation (SAN).

## Features

- **Display Board**: Render a human-readable representation of the chess board.
- **Generate Legal Moves**: Calculate all legal moves for a given board state.
- **Apply Move**: Apply a move to the board and return the resulting FEN string.

## What are FEN and SAN?

### FEN (Forsyth-Edwards Notation)

FEN is a standard notation for describing a particular board position of a chess game. It provides all the necessary information to reconstruct a game position. A FEN string consists of six fields separated by spaces:
1. **Piece placement (from top to bottom, left to right)**
2. **Active color (whose turn it is to move)**
3. **Castling availability**
4. **En passant target square**
5. **Halfmove clock**
6. **Fullmove number**

Example:
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

### SAN (Standard Algebraic Notation)

SAN is the most commonly used notation for recording chess moves. It concisely describes each move using a combination of piece abbreviations, file (column), rank (row), and sometimes additional symbols for captures, checks, and promotions. 

- **Pawn moves**: `e4`, `d5`
- **Piece moves**: `Nf3` (knight to f3), `Bb5` (bishop to b5)
- **Captures**: `exd5` (pawn on e file captures on d5)
- **Castling**: `O-O` (kingside), `O-O-O` (queenside)
- **Promotion**: `e8=Q` (pawn moves to e8 and promotes to a queen)
- **Check**: `+` (e.g., `Qe5+`)
- **Checkmate**: `#` (e.g., `Qe5#`)
