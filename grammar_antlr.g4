grammar grammar_antlr;

suite: 'Suite' ID (test | order)*;
test: 'Test' ID flag* 'When' parameter+ result;
flag: '-' ('skip' | 'Skip' | 'Repeat' INT 'times');
parameter: ID '=' datatype | emptyParameters;
result: 'Then' ('result' 'should' 'be')? (datatype | emptyResult);
emptyParameters: 'no' 'parameters' | 'None' | 'none' | 'void' | 'Void';
emptyResult: 'empty' | 'Empty' | 'void' | 'Void' | 'none' | 'None';
order: 'Execution' 'order' ':' ID (',' ID)*;

datatype: STRING | INT | FLOAT | NUMBER | BOOL;
ID: [a-zA-Z_] [a-zA-Z0-9_]*;
STRING: '"' ~'"'* '"';
NUMBER: INT | FLOAT;
INT: [0-9]+;
FLOAT: [0-9]* '.' [0-9]+;
BOOL: 'true' | 'false';

WS: [ \t\r\n]+ -> skip;
