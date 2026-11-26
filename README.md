# LEDGER

A command-line personal finance tracker. It keeps accounts, moves money between them, and records each move as a transaction.

## Design Decisions

### Transaction is a dataclass
`Transaction` only holds data: a source, a destination, and an amount. A dataclass writes `__init__`, `__repr__`, and `__eq__` for me, so two transactions with the same values compare as equal and print clearly when I debug. It checks its own fields in `__post_init__` (empty names and amounts <= 0 are rejected), but it never changes any other object's state.

### Account is a regular class
`Account` has an invariant (a rule that must always stay true): the balance can never go below zero. Its balance changes over time, so every method that changes it, like `spend`, must check the rule first. A regular class lets me guard that rule inside its methods.