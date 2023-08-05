from typing import Any, Optional

class DjangoUnicodeDecodeError(UnicodeDecodeError):
    obj: bytes = ...
    def __init__(self, obj: bytes, *args: Any) -> None: ...

python_2_unicode_compatible: Any

def smart_text(s: Any, encoding: str = ..., strings_only: bool = ..., errors: str = ...) -> str: ...
def is_protected_type(obj: Any) -> bool: ...
def force_text(s: Any, encoding: str = ..., strings_only: bool = ..., errors: str = ...) -> Optional[str]: ...
def smart_bytes(s: Any, encoding: str = ..., strings_only: bool = ..., errors: str = ...) -> bytes: ...
def force_bytes(s: Any, encoding: str = ..., strings_only: bool = ..., errors: str = ...) -> bytes: ...

smart_str = smart_text
force_str = force_text

def iri_to_uri(iri: Optional[str]) -> Optional[str]: ...
def uri_to_iri(uri: Optional[str]) -> Optional[str]: ...
def escape_uri_path(path: str) -> str: ...
def repercent_broken_unicode(path: bytes) -> bytes: ...
def filepath_to_uri(path: Optional[str]) -> Optional[str]: ...
def get_system_encoding() -> str: ...

DEFAULT_LOCALE_ENCODING: Any
