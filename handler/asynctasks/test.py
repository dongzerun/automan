#!/bin/env python


#sql = ('>', 'id', 0)
sql = ('and', ('and', ('>', 'is_auth_highrisk', 1), ('>', 'id', 0)), ('=', 'is_status', 0))

pkname = "id"
pkequal = True

def mustequal(op, s1, s2):
    if not isinstance(s1, tuple) and not isinstance(s2, tuple):
        if s1 == pkname:
            print "sql print: ", s1, op, s2
            if op != "=":
                print op
    elif  isinstance(s1, tuple) and isinstance(s2, tuple):
        return '{} {} {}'.format(mustequal(*s1), op , mustequal(*s2))
    elif isinstance(s1, tuple): 
        return '{} {} {}'.format( mustequal(*s1) , op , s2)
    else:
        return '{} {} {}'.format( s1, op , mustequal(*s2))

mustequal(*sql)
print pkequal 
    
