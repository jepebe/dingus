##Lexical Grammar
```
NUMBER     → DIGIT+ ( "." DIGIT+ )? 
STRING     → "(\"|[^\"])*" | '(\'|[^\'])*' 
IDENTIFIER → ALPHA ( ALPHA | DIGIT )*
ALPHA      → [a-z] | [A-Z] | [_]
DIGIT      → [0-9]
```

##Expressions
```
expression → literal | unary | binary | grouping
literal    → NUMBER | STRING | "True" | "False" | "None" | "Undefined"
grouping   → "(" expression ")"
unary      → ( "-" | "not" ) expression
binary     → expression operator expression
operator   → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+"  | "-"  | "*" | "/"

```