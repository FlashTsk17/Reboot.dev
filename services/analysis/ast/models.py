from dataclasses import dataclass, field

@dataclass(frozen=True)
class Symbol:
    name: str
    kind: str
    line: int
    end_line: int

@dataclass(frozen=True)
class Import:
    source: str
    line: int

@dataclass(frozen=True)
class Call:
    name: str
    line: int

@dataclass
class CodeFileAST:
    path: str
    language: str
    imports: list[Import] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    symbols: list[Symbol] = field(default_factory=list)
    calls: list[Call] = field(default_factory=list)
    syntax_errors: list[str] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
