#!/usr/bin/env python

import time
from game.models import Field

if __name__ == '__main__':
    field = Field(800, 800)

    while True:
        print(field._ball._body.position)
        field.update(1.0 / 60)
        time.sleep(1)
