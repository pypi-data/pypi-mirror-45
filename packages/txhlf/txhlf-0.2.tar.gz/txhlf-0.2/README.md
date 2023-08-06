# Traxion HLF

Traxion HLF is a Python SDK for Traxion Blockchain

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install txhlf
```

## Usage

```python
from txhlf import TraxionHLF

hlf = TraxionHLF("username", "password")
transaction = hlf.create_transaction(customer_ref_ID, customer_name, transaction, transactionDate, field1)

query = hlf.get_transactions(customer_ref_ID='ABC1203')
query = hlf.get_transactions(customer_name='BigMama')

```
### Args:

**customer_ref_ID**: is the customer or individual Id (Primary Key) from our customer. Example. QR123TXN or 123456789

**customer_name**: is the company from our DB. Example: NCCC, CISP, PBCOM, PNB etc. I suggest this should only be an acronym of the on boarded organization.

**transaction**: is the amount rendered

**transactionDate**: date and time of the transaction

**field1**: Generic field. We can agree later which data we store (I am thinking this will serve as product entry field). Example: KAPARTNER, CREDX, PAYWISE, BAIYARIN etc

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
