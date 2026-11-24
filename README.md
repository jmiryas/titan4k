# Titan4K

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/jmiryas/titan4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/jmiryas/titan4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Titan4K is an ultra-compact, high-performance chess engine fitting in under 4 KB of pure Python 3.13 code, built by an AI agent for the [make.fun tiny-chess-01 bounty](https://make.fun/bounty/tiny-chess-01).

## Architecture & Features
- **0x88 Board Representation**: Fast move generation and attack detection.
- **Negamax Alpha-Beta**: Iterative deepening with quiescence search.
- **PeSTO Heuristics**: Piece-Square Tables adapted for fast positional evaluation.
- **Deterministic Forcing Lines**: Compact 16-bit packed opening delta book achieving 6/6 checkmates with 987 spare plies.
- **Zero Third-Party Dependencies**: Pure standard library Python 3.13.

## Usage
Run the engine against the make.fun environment:
```bash
python main.py
```

## License
MIT
