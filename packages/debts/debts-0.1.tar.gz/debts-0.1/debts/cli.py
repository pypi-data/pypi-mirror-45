import argparse

from .parser import parse_inline_text
from .solver import settle
from .humanize import verbose_results


def main():
    parser = argparse.ArgumentParser(description="Settle debts.")
    parser.add_argument(
        "--settle",
        dest="settle",
        help="the identifiers and amounts to be solved"
        ' (ex. --settle "alice +200, marc -100, henri -100")',
        required=True,
    )
    args = parser.parse_args()
    try:
        balance = parse_inline_text(args.settle)
        print(verbose_results(settle(balance)))
    except Exception as e:
        print(f"Sorry, an error occured. {e}")
