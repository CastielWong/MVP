
- [Demonstration](#demonstration)
- [Reference](#reference)


## Demonstration
Class definition:
```py
from functools import total_ordering


@total_ordering
class Account:

    def __init__(self, owner, amount=0):
        self.owner = owner
        self.amount = amount
        self._transactions = []

    def __repr__(self):
        return f"{self.__class__.__name__}({self.owner:!r}, {self.amount:!r})"

    def __str__(self):
        return f"{self.__class__.__name__} of {self.owner} with starting amount: {self.amount})"

    # enable iteration
    def __len__(self):
        return len(self._transactions)

    def __getitem__(self, index):
        return self._transactions[index]

    def __reversed__(self):
        return self[::-1]

    # overload operator for comparison
    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance

    # overload operator for addition
    def __add__(self, other):
        owner = f"{self.owner} & {other.owner}"
        start_amount = self.amount + other.amount

        acc = Account(owner, start_amount)
        for t in list(self) + list(other):
            acc.add_transaction(t)

        return acc

    # invocate method
    def __call__(self):
        print(f"Start amount: {self.amount}")
        print("Transactions: ")
        for transaction in self:
            print(transaction)
        print(f"Balance: {self.balance}")

    # support context manager
    def __enter__(self):
        print("ENTER WITH: Making backup of transactions for rollback")
        self._copy_transactions = list(self._transactions)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("EXIT WITH:", end=" ")
        if exc_type:
            self._transactions = self._copy_transactions
            print("Rolling back to previous transactions")
            print(f"Transaction resulted in {exc_type.__name__}, ({exc_val})")
        else:
            print("Transaction OK")

    @property
    def balance(self):
        return self.amount + sum(self._transactions)

    def add_transaction(self, amount):
        if not isinstance(amount, int):
            raise ValueError("Please use integer for amount")
        self._transactions.append(amount)


def validate_transaction(acc, amount_to_add):
    with acc as a:
        print(f"Adding {amount_to_add} to account")
        a.add_transaction(amount_to_add)
        print(f"New balance would be: {a.balance}")

        if a.balance < 0:
            raise ValueError("Sorry cannot go in debt!")
```

Checking:
```py
SEPARATOR = "-" * 80

if __name__ == "__main__":
    acc_1 = Account("Bob", 10)
    acc_1.add_transaction(20)
    acc_1.add_transaction(-10)
    acc_1.add_transaction(50)
    acc_1.add_transaction(-20)
    acc_1.add_transaction(30)

    acc_2 = Account("Tim", 100)
    acc_2.add_transaction(20)
    acc_2.add_transaction(40)

    # enable iteration
    print(SEPARATOR)
    print(len(acc_1))
    for t in acc_1:
        print(t)
    print(acc_1[1])
    print(list(reversed(acc_1)))

    # overload operator for comparison
    print(SEPARATOR)
    print(acc_2 > acc_1)
    print(acc_2 < acc_1)
    print(acc_2 == acc_1)

    # overload operator for addition
    print(SEPARATOR)
    acc_3 = acc_1 + acc_2
    print(acc_3.amount)
    print(acc_3.balance)
    print(acc_3._transactions)

    # invocate method
    print(SEPARATOR)
    acc_1()

    # support context manager
    print(SEPARATOR)
    print(f"Balance start: {acc_1.balance}")
    validate_transaction(acc_1, 10)
    print(f"Balance end: {acc_1.balance}")

    print(SEPARATOR)
    print(f"Balance start: {acc_1.balance}")
    try:
        validate_transaction(acc_1, -100)
    except ValueError as exc:
        print(exc)
    print(f"Balance end: {acc_1.balance}")
```


## Reference
- Enriching Your Python Classes With Dunder (Magic, Special) Methods: https://dbader.org/blog/python-dunder-methods
