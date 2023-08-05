#!python
# -*- coding:utf-8 -*-
import os

# macros managedd by mercurial keyword extension
CVSAuthor="$Author: noboru $"
CVSDate="$Date: 2019/04/17 07:29:27 $"
CVSRev="$Revision: fbee1320cac7 $"
CVSSource="$Header: /Users/noboru/src/python/VXI11/PyVXI11-Current/cVXI11_revision.py,v fbee1320cac7 2019/04/17 07:29:27 noboru $"
CVSFile="$Source: /Users/noboru/src/python/VXI11/PyVXI11-Current/cVXI11_revision.py,v $"
CVSId="$Id: cVXI11_revision.py,v fbee1320cac7 2019/04/17 07:29:27 noboru $"
#
HGTag="$HGTag: 1.14.3-fbee1320cac7 $"
HGdate="$HGdate: Wed, 17 Apr 2019 16:29:27 +0900 $"
HGTagShort="$HGTagShort: 1.14.3 $"
HGlastlog="$lastlog: removce access to mercurial in cvxi11_revition.py. argments for rpcinfo call are adjusted $"
#

rev=HGTag[HGTag.index(":")+1:HGTag.index("-")].strip()
