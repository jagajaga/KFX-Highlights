# KFX-Highlights

Extract Kindle highlights from sideloaded KFX books into HTML or Markdown.

This is a fork of [aakar/KFX-Highlights](https://github.com/aakar/KFX-Highlights) with:

- **Markdown output** via `--markdown` (no more piping HTML through pandoc).
- **A parser fix** in `krds.py` for `font.prefs` payloads in current Kindle firmware — the parser crashes on modern `.yjr` files with `Excess values found for structure font.prefs: [0, 0, 1, 0]`. This fork drains the trailing fields and continues. Note that `krds.py` itself is **John Howell's GPL v3 code** (copyright 2019); my patch is just a tolerance loop on top of his parser.

Two thirds of this repository is actually John Howell's work:

- **`krds.py`** — the `.yjr` annotation-format parser. Originally distributed via the [K-R-D-S](https://github.com/K-R-D-S/KRDS) repo. GPL v3.
- **`KFX Input/`** — the full Calibre KFX Input plugin, providing `kfxlib` (KFX container decoding, position resolution, metadata, navigation). GPL v3. See its [attribution README](KFX%20Input/README.md).

Aakar's contribution (and what I forked from) is the glue: `extract_highlights.py` and `extract_highlights_kfxlib.py`, which combine `.yjr` positions with `.kfx` content to reconstruct quoted text and emit HTML.

## Why does this exist?

Kindle highlights for KFX books aren't stored as text. The `.yjr` file in the book's `.sdr/` sidecar folder only contains *position references* — entries like `AaQLAAACAAAA:156164` that point into the book's content tree. To turn those into quoted text you have to:

1. Parse the `.yjr` binary annotation format (handled by `krds.py`).
2. Open the `.kfx` book, decode its container, and resolve the positions against the actual content (handled by `kfxlib`).
3. Cross-reference page numbers and chapter titles from the book's navigation table.

This tool does all three.

## Install

```bash
pip install pillow pypdf lxml beautifulsoup4
```

No other setup — `kfxlib` is vendored in [`KFX Input/`](KFX%20Input/) and imported directly from there. See that folder's README for attribution and license.

## Usage

```bash
python extract_highlights.py <book.kfx> <annotations.yjr> [--markdown]
```

The `.yjr` file lives inside the book's `.sdr/` folder when you connect your Kindle and copy the book out. For example:

```
documents/
└── MyBook_ASIN.kfx
└── MyBook_ASIN.sdr/
    └── MyBook_ASIN<...hash...>.yjr   ← this one
```

### HTML output (default)

```bash
python extract_highlights.py MyBook.kfx MyBook.yjr
```

Writes `MyBook.highlights.html` next to the book, styled like the Amazon "Your Notebook" page.

### Markdown output (`--markdown` / `-m`)

```bash
python extract_highlights.py MyBook.kfx MyBook.yjr --markdown
```

Writes `MyBook.highlights.md` — one section per chapter, each highlight as a Markdown blockquote with chapter/page metadata. Suitable for Obsidian, Roam, plain `grep`, or pasting anywhere.

Example output:

```markdown
# Cat's Cradle
_Kurt Vonnegut_

## 6. The Bug Fights

**Highlight — Page 18**

> When the bomb fell, my father said, "Science has now known sin."
```

## What this tool *can't* do

A few failure modes to be aware of when you run this on a real Kindle library:

- **DRM-protected books.** `kfxlib` refuses to open KFX containers with DRM. You'll need [DeDRM](https://github.com/noDRM/DeDRM_tools) to strip protection from purchased Amazon books before this tool can read them.
- **Empty `.yjr`.** A 50-byte `.yjr` means there are no local highlights. They probably synced to Amazon's cloud only — export from [read.amazon.com/notebook](https://read.amazon.com/notebook) instead.
- **`.mbp` files.** Older `.azw` (Mobipocket) books store annotations in `.mbp` format, not `.yjr`. This tool only handles `.yjr`. You'd need a Mobipocket-aware parser for those.
- **No `.sdr/` folder.** Some books just don't have one — no annotations were ever made or synced locally.

## How it works internally

1. `krds.py` parses the `.yjr` binary into JSON. Includes a tolerance patch for `font.prefs` so it doesn't crash on Kindle firmware ≥ ~2023 which adds trailing fields.
2. `extract_highlights_kfxlib.py` loads the KFX content via `kfxlib`, builds a sorted list of text sections with their start positions and lengths, then slices each annotation's `startPosition`/`endPosition` against that.
3. The book's navigation (`$389` fragment) gives the page list and TOC, used to label each highlight with its chapter and page number.
4. Notes are merged in by matching `note.startPosition` against highlight end positions.
5. Output is written as either HTML (Kindle-Notebook style) or Markdown (chapter-grouped blockquotes).

## Credits

- **John Howell** &lt;jhowell@acm.org&gt; — wrote `krds.py` (the `.yjr` annotation parser, distributed via [K-R-D-S/KRDS](https://github.com/K-R-D-S/KRDS)) **and** `kfxlib` (the KFX container library, distributed as the [Calibre KFX Input plugin](https://www.mobileread.com/forums/showthread.php?t=291290)). Two thirds of this repository is his code.
- **[aakar](https://github.com/aakar)** — wrote `extract_highlights.py` and `extract_highlights_kfxlib.py`, the glue that joins jhowell's `.yjr` parser and `kfxlib` to produce a useful end-to-end highlight extractor. This fork is forked from theirs.
- **[Arseniy Seroka](https://github.com/jagajaga)** (jagajaga) — maintains this fork. Hit the `font.prefs` crash on a real Kindle backup, wrote the tolerance patch, and added the `--markdown` output mode.

## License

`krds.py` and everything under [`KFX Input/`](KFX%20Input/) are **John Howell's, GPL v3**. The wrapper scripts (`extract_highlights.py`, `extract_highlights_kfxlib.py`) come from upstream and inherit their license. Since GPL v3 is copyleft, the combined work is effectively GPL v3.

See [`KFX Input/README.md`](KFX%20Input/README.md) for full attribution and license terms on the vendored plugin.
