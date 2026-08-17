from pathlib import Path
import re

root=Path(__file__).resolve().parent
chapters=sorted((root/"chapters").glob("*.html"))
styles=sorted((root/"style_parts").glob("*.css"))

chapter_html=[p.read_text(encoding="utf-8") for p in chapters]
html=(root/"page_top.html").read_text(encoding="utf-8")
html+="".join(chapter_html)
html+=(root/"page_bottom.html").read_text(encoding="utf-8")
css="".join(p.read_text(encoding="utf-8") for p in styles)

# CHAPTER != PAGE.
# section.chapter is only an organisational container.
# article is the current independent page/surface unit inherited from the 52-page baseline.
chapter_count=len(re.findall(r'<section\b[^>]*class="[^"]*\bchapter\b', html, flags=re.I))
article_page_count=len(re.findall(r'<article\b', html, flags=re.I))

# The last fully read-back pre-v3 baseline contained 52 independent article/page surfaces.
# v3.x may add pages, but must never compress below that baseline just to fit chapters.
LEGACY_PAGE_FLOOR=52
if article_page_count < LEGACY_PAGE_FLOOR:
    raise RuntimeError(
        f"NO-COMPRESSION VIOLATION: page_count={article_page_count} < legacy floor {LEGACY_PAGE_FLOOR}. "
        "CHAPTER != PAGE; restore missing independent pages before build."
    )

(root/"index.html").write_text(html,encoding="utf-8")
(root/"styles.css").write_text(css,encoding="utf-8")

print(root/"index.html")
print(root/"styles.css")
print(f"chapter_count={chapter_count}")
print(f"page_count={article_page_count}")
print(f"legacy_page_floor={LEGACY_PAGE_FLOOR}")
