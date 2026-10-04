class BankAccount:
  def __init__(self, initial_balance):
    self._balance = initial_balance
    # Stack of (type, amount) tuples representing standing transactions

    self._history: list[tuple[str, int]] = []

  def deposit(self, amount):
    self._balance += amount
    self._history.append(("deposit", amount))

  def withdraw(self, amount):
    if amount > self._balance:
      raise ValueError("Insufficient funds")
    self._balance -= amount
    self._history.append(("withdraw", amount))

  def undo(self):
    if not self._history:
      return  # nothing to reverse
    kind, amount = self._history.pop()
    if kind == "deposit":
      self._balance -= amount
    else:  # withdraw
      self._balance += amount

  @property
  def balance(self):
    return self._balance


def bank_account_simulator(initial_balance, ops):
  account = BankAccount(initial_balance)
  for op in ops:
    action = op[0]
    if action == "deposit":
      account.deposit(op[1])
    elif action == "withdraw":
      try:
        account.withdraw(op[1])
      except ValueError:
        return "ValueError"
    elif action == "undo":
      account.undo()
    elif action == "balance":
      _ = account.balance  # read, no state change
  return account.balance
