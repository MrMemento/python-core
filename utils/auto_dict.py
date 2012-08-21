# encoding: utf-8
# vendor:   Rubin DMS Inc.
# package:  @{NAME}-@{VERSION}
# author:   BARNA <barna@rubindms.hu>
# version:  @{REVISION}

#----------
# AUTODICT
#----------

class AutoDict( dict ):
    '''
    Class for dictionaries automatically creating keys when called with dot syntax.
    '''

    pass
    # do not ask me how this works, in my
    # opinion, __getattr__ should be used...
