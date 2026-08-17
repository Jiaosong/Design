from pathlib import Path
root=Path(__file__).resolve().parent
chapters=sorted((root/"chapters").glob("*.html"))
out=(root/"page_top.html").read_text(encoding="utf-8")
out+="".join(p.read_text(encoding="utf-8") for p in chapters)
out+=(root/"page_bottom.html").read_text(encoding="utf-8")
(root.parent/"index.rebuilt.html").write_text(out,encoding="utf-8")
print(root.parent/"index.rebuilt.html")
