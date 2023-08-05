#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from datafaker.cli import main

if __name__ == "__main__":


    # cmd = 'datafaker file . hello.txt 10 --meta data/student.txt --withheader --outprint --batch 2'
    # cmd = 'datafaker file . hello.txt 10 --meta data/student.txt --withheader --batch 2'
    # # cmd = 'datafaker mysql mysql+mysqldb://root:root@localhost:3600/test student 10 --batch 3'
    # sys.argv = cmd.strip().split(' ')
    sys.exit(main())

