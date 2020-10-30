import sys
import os

if os.name == "nt":
    sys.path.append(os.path.abspath(".") + "\\tic_tac_toe")


print(f"test\\__init__.py ran")

print(f"test\\ __init__ updated sys.path to:")
for entry in sys.path:
    print(f"\t{entry}")

sys.path.insert(0, "TEST")
