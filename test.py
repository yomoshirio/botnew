from asyncio import run
from payok_handler import get_last_pay
from rich.console import Console
c = Console()

s = run(get_last_pay())

c.print(s)
