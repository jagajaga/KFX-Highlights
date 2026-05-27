# KFX Input — vendored copy of the Calibre KFX Input plugin

**I did not write any of the code in this directory.** Everything here is the
work of **John Howell** ("jhowell"), released as the [KFX Input plugin for
Calibre](https://www.mobileread.com/forums/showthread.php?t=291290).

- **Author:** John Howell &lt;jhowell@acm.org&gt;
- **License:** GPL v3
- **Copyright:** 2017–2025, John Howell
- **Upstream:** [MobileRead — KFX Input plugin](https://www.mobileread.com/forums/showthread.php?t=291290)

This is the contents of the `KFX Input.zip` plugin file as published by the
author, extracted into a directory so it can be browsed and audited without
having to unzip first. **The code here is unmodified from upstream** — this
fork does not change any of jhowell's code. Git may normalize line endings to
LF on commit (the repo-wide default), but the source is otherwise identical
to what's in the published `.zip`.

## Why is it here?

The `KFX-Highlights` tool in the parent directory needs `kfxlib` (the Python
package nested at `kfxlib/` inside this folder) to:

1. Decode Amazon's proprietary KFX container format.
2. Resolve highlight position references (`AaQLAAACAAAA:156164`) into actual
   text positions inside the book.
3. Read book metadata (title, author, publication date).
4. Walk the book's navigation table to label each highlight with its chapter
   and page number.

`kfxlib` is not on PyPI. It is only distributed as part of this Calibre plugin.
Bundling the plugin in the repository keeps the highlight extractor
self-contained — no separate Calibre install required.

## How it's loaded

The extractor inserts this directory onto `sys.path`, then `import kfxlib`
works as if the plugin were installed:

```python
sys.path.insert(0, str(Path(__file__).parent / "KFX Input"))
from kfxlib import yj_book
```

## If you want the original `.zip`

It's the published Calibre plugin file. Either download it directly from the
MobileRead thread linked above, or run `zip -r "KFX Input.zip" .` from inside
this directory to rebuild it.

## License notice

Since this code is GPL v3, anything that links against it is subject to the
GPL's copyleft requirements. If you redistribute the `KFX-Highlights` tool you
must comply with GPL v3 for the `kfxlib` portion. The full text of the GPL v3
is available at [gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).
