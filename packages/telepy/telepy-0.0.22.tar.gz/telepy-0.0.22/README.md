#### Tele
view [readthedocs](https://tele.readthedocs.io)
##### Installation

requires python 3 + to run.

`pip3 install telepy`

```python 
from Tele import *


@bot('text')
def echo(update):
    message_reply(update, update.text)


account('TOKEN')
bot_run()

```
