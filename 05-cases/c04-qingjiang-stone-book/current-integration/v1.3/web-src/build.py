from pathlib import Path
root=Path(__file__).resolve().parent
chapters=sorted((root/"chapters").glob("*.html"))
styles=sorted((root/"style_parts").glob("*.css"))
html=(root/"page_top.html").read_text(encoding="utf-8")
html+="".join(p.read_text(encoding="utf-8") for p in chapters)
html+=(root/"page_bottom.html").read_text(encoding="utf-8")
css="".join(p.read_text(encoding="utf-8") for p in styles)
(root/"index.html").write_text(html,encoding="utf-8")
(root/"styles.css").write_text(css,encoding="utf-8")
print(root/"index.html")
print(root/"styles.css")
