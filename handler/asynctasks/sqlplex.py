# sqlplex.py. This file automatically created by PLY (version 3.4). Don't edit!
_tabversion   = '3.4'
_lextokens    = {'ENGINE': 1, 'TRANSACTION': 1, 'MIN': 1, 'TEXT': 1, 'BETWEEN': 1, 'DUPLICATE': 1, 'BIGINT': 1, 'LIMIT': 1, 'DUAL': 1, 'TRUE': 1, 'MINUS': 1, 'COMMENT': 1, 'FORCE': 1, 'DELIM': 1, 'VIEW': 1, 'NUMERIC': 1, 'NEXT': 1, 'SESSION': 1, 'PLUS': 1, 'FIRST': 1, 'GT': 1, 'NATURAL': 1, 'ORDER': 1, 'ENUM': 1, 'COMMIT': 1, 'DATETIME': 1, 'GE': 1, 'TRIGGER': 1, 'SET_VAR': 1, 'ESCAPE': 1, 'FALSE': 1, 'UNIQUE': 1, 'WHERE': 1, 'DECLARE': 1, 'BEFORE': 1, 'BITWISE_XOR': 1, 'ON': 1, 'LOGICAL_NOT': 1, 'MAX': 1, 'AFTER': 1, 'PRIMARY': 1, 'COMMENTS': 1, 'VALUES': 1, 'ELSEIF': 1, 'OR': 1, 'LOOP': 1, 'TINYBLOB': 1, 'INDEX': 1, 'CONVERT': 1, 'RETURN': 1, 'MEDIUMINT': 1, 'SOME': 1, 'DELAYED': 1, 'RESTRICT': 1, 'CURRENT_TIMESTAMP': 1, 'BITWISE_AND': 1, 'QUICK': 1, 'ROLLBACK': 1, 'SOUNDS': 1, 'SELECT': 1, 'MEDIUMBLOB': 1, 'CHAIN': 1, 'DISTINCT': 1, 'WITH': 1, 'SHARE': 1, 'UNSIGNED': 1, 'ALTER': 1, 'SNAPSHOT': 1, 'NULL_SAFE': 1, 'INTEGER': 1, 'INTO': 1, 'ROW': 1, 'COUNT': 1, 'SHR': 1, 'IDENT': 1, 'END': 1, 'FOR': 1, 'UNION': 1, 'CONSISTENT': 1, 'UPDATE': 1, 'ELSE': 1, 'HIGH_PRIORITY': 1, 'OFFSET': 1, 'RELEASE': 1, 'REGEXP': 1, 'EQ': 1, 'UNTIL': 1, 'AND': 1, 'INT': 1, 'TIMESTAMP': 1, 'SIGNED': 1, 'ROLLUP': 1, 'BLOB': 1, 'LOW_PRIORITY': 1, 'NOT': 1, 'DELETE': 1, 'ANY': 1, 'MOD': 1, 'THEN': 1, 'DROP': 1, 'BIT_OR': 1, 'DEFAULT': 1, 'UNKNOWN': 1, 'SUM': 1, 'GLOBAL': 1, 'CROSS': 1, 'CHAR': 1, 'WHILE': 1, 'REPEAT': 1, 'GROUP': 1, 'OPEN': 1, 'FETCH': 1, 'CASE': 1, 'SET': 1, 'NO': 1, 'COLUMN': 1, 'SHL': 1, 'WORK': 1, 'NE': 1, 'REPLACE': 1, 'ASC': 1, 'CAST': 1, 'TABLE': 1, 'IF': 1, 'LEFT': 1, 'OUTER': 1, 'BIT_AND': 1, 'LOCK': 1, 'DECIMAL': 1, 'CASCADE': 1, 'ADD': 1, 'CLOSE': 1, 'BY': 1, 'CONSTRAINT': 1, 'LEAVE': 1, 'ALL': 1, 'JOIN': 1, 'LIKE': 1, 'DATABASE': 1, 'TINYTEXT': 1, 'FLOAT_LIT': 1, 'IGNORE': 1, 'BITWISE_OR': 1, 'MEDIUMTEXT': 1, 'KEY': 1, 'EACH': 1, 'USING': 1, 'LONGBLOB': 1, 'RENAME': 1, 'DO': 1, 'USE': 1, 'CHARSET': 1, 'CHARACTER': 1, 'NUMBER': 1, 'TINYINT': 1, 'DATE': 1, 'DIV': 1, 'NULL': 1, 'BIT_XOR': 1, 'CHANGE': 1, 'SMALLINT': 1, 'INSERT': 1, 'LE': 1, 'VARCHAR': 1, 'AVG': 1, 'AUTO_INCREMENT': 1, 'CREATE': 1, 'WHEN': 1, 'TO': 1, 'LT': 1, 'MODE': 1, 'ITERATE': 1, 'OPTIMIZE': 1, 'ROW_FORMAT': 1, 'CUBE': 1, 'XOR': 1, 'STRING': 1, 'EXISTS': 1, 'IS': 1, 'TIME': 1, 'BEGIN': 1, 'VALUE': 1, 'TIMES': 1, 'START': 1, 'AS': 1, 'INNER': 1, 'IN': 1, 'TEMPORARY': 1, 'DESC': 1, 'RIGHT': 1, 'FROM': 1, 'LONGTEXT': 1, 'FLOAT': 1, 'DELIMITER': 1, 'MODIFY': 1, 'HAVING': 1, 'COLLATE': 1}
_lexreflags   = 0
_lexliterals  = ',();*@`.'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_NEWLINE>\\r?\\n+)|(?P<t_COMMENTS>/\\*(.|[\\r\\n])*?\\*/|--[^\\n]*|\\#[^\\n]*)|(?P<t_FLOAT_LIT>(-?\\d+\\.\\d+([Ee](\\+|-)?\\d+)?|-?\\d+[Ee][+-]?\\d+))|(?P<t_NUMBER>-?\\d+)|(?P<t_STRING>"(\\\\"|""|[^"])*"|\\\'(\\\\\\\'|\\\'\\\'|[^\\\'])*\\\')|(?P<t_DELIMITER>(?i)DELIMITER[ \\t]+(?P<new_delim>[^ \\t\\n]+))|(?P<t_IDENT>[A-Za-z_][\\w_.]*|`(``|[^`])*`)|(?P<t_NE><>|!=)|(?P<t_OR>\\|\\|)|(?P<t_DELIM>[;])|(?P<t_NULL_SAFE><=>)|(?P<t_LE><=)|(?P<t_GE>>=)|(?P<t_AND>&&)|(?P<t_SET_VAR>:=)|(?P<t_BITWISE_OR>\\|)|(?P<t_TIMES>\\*)|(?P<t_PLUS>\\+)|(?P<t_SHR>>>)|(?P<t_SHL><<)|(?P<t_LOGICAL_NOT>!)|(?P<t_MINUS>-)|(?P<t_DIV>/)|(?P<t_BITWISE_AND>&)|(?P<t_GT>>)|(?P<t_BITWISE_XOR>^)|(?P<t_MOD>%)|(?P<t_LT><)|(?P<t_EQ>=)', [None, ('t_NEWLINE', 'NEWLINE'), ('t_COMMENTS', 'COMMENTS'), None, ('t_FLOAT_LIT', 'FLOAT_LIT'), None, None, None, ('t_NUMBER', 'NUMBER'), ('t_STRING', 'STRING'), None, None, ('t_DELIMITER', 'DELIMITER'), None, ('t_IDENT', 'IDENT'), None, (None, 'NE'), (None, 'OR'), (None, 'DELIM'), (None, 'NULL_SAFE'), (None, 'LE'), (None, 'GE'), (None, 'AND'), (None, 'SET_VAR'), (None, 'BITWISE_OR'), (None, 'TIMES'), (None, 'PLUS'), (None, 'SHR'), (None, 'SHL'), (None, 'LOGICAL_NOT'), (None, 'MINUS'), (None, 'DIV'), (None, 'BITWISE_AND'), (None, 'GT'), (None, 'BITWISE_XOR'), (None, 'MOD'), (None, 'LT'), (None, 'EQ')])]}
_lexstateignore = {'INITIAL': ' \t\x0c'}
_lexstateerrorf = {'INITIAL': 't_error'}