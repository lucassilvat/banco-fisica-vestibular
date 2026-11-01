"""Verbatim extraction of exam questions with light markup.
Usage: python3 -I extract2.py exam.pdf segments.json "57,58,59" outdir
Writes outdir/<n>.json  {body:[paragraphs], alts:[...], figs:[png paths], shared:str|None}
Figures (vector drawings / images) and fraction-style equations are cropped as PNG
and referenced in the text as [[figura k]] at their position.
"""
import json, re, sys, os  # noqa: E401
import pymupdf

TAGS = ["b", "u", "i", "sub", "sup"]
ALT = re.compile(r"^([a-d])\)\s*")
SHARED = re.compile(r"^Texto (?:comum )?(?:para|às) as questões\b", re.I)

def clusters(rects, gap=6):
    boxes = [pymupdf.Rect(r) for r in rects]
    merged = True
    while merged:
        merged = False
        out = []
        for r in boxes:
            for o in out:
                if (o + (-gap, -gap, gap, gap)).intersects(r):
                    o |= r; merged = True; break
            else:
                out.append(pymupdf.Rect(r))
        boxes = out
    return boxes

def page_info(page):
    W = page.rect.width
    thin, other = [], []
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.width > 0.8 * W or r.height > 700:
            continue
        if r.height < 1.6 and r.width > 2:
            thin.append(r)
        elif r.width > 0.5 or r.height > 0.5:
            other.append(r)
    for im in page.get_image_info():
        other.append(pymupdf.Rect(im["bbox"]))
    figs = [b for b in clusters(other + [t for t in thin if t.width > 160]) if b.width > 25 and b.height > 18]
    return thin, figs

def text_lines(page, rect):
    d = page.get_text("rawdict", clip=rect)
    out = []
    for b in d["blocks"]:
        for l in b.get("lines", []):
            if abs(l["dir"][0] - 1) > 0.01:
                continue
            spans = [s for s in l["spans"] if s["chars"]]
            if spans:
                out.append(pymupdf.Rect(l["bbox"]), spans)
    return out

def build_lines(page, rect, thin, figs):
    raw = page.get_text("rawdict", clip=rect)
    items = []
    for b in raw["blocks"]:
        for l in b.get("lines", []):
            if abs(l["dir"][0] - 1) > 0.01:
                continue
            lb = pymupdf.Rect(l["bbox"])
            c = ((lb.x0 + lb.x1) / 2, (lb.y0 + lb.y1) / 2)
            if any(f.contains(pymupdf.Point(c)) for f in figs):
                continue
            spans = [s for s in l["spans"] if s["chars"] and s["size"] < 13]
            if not spans:
                continue
            items.append((lb, spans))
    return items

def style_chars(spans, rect, thin):
    body = [s for s in spans if s["size"] > 8]
    base = max(body, key=lambda s: len(s["chars"]))["origin"][1] if body else spans[0]["origin"][1]
    chars = []
    for s in spans:
        small = s["size"] < 8
        oy = s["origin"][1]
        sup = bool(s["flags"] & 1) or (small and oy < base - 1)
        sub = small and not sup and oy > base + 0.5
        italic = bool(s["flags"] & 2) or "Ital" in s["font"] or "Ita" in s["font"] or s["font"].endswith("-I")
        bold = bool(s["flags"] & 16) or "Bold" in s["font"]
        for ch in s["chars"]:
            bx = ch["bbox"]; cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
            if not (rect.x0 <= cx <= rect.x1 and rect.y0 <= cy <= rect.y1):
                continue
            c = ch["c"]
            punct = c in ".,;:()"
            under = any(t.x0 - .5 <= cx <= t.x1 + .5 and bx[3] - 3 <= t.y0 <= bx[3] + 3 for t in thin)
            chars.append((c, dict(i=italic and c.strip() != "" and not punct and not c.isdigit(),
                                  sub=sub and not punct, sup=sup and not punct, b=bold,
                                  u=under and c.strip() != ""), bx))
    chars.sort(key=lambda t: t[2][0])
    return chars

def render(chars):
    out, cur = [], {t: False for t in TAGS}
    for c, st, _ in chars:
        if c in " \t ":
            want = dict(cur); want.update(i=False, sub=False, sup=False)
        else:
            want = {t: st[t] for t in TAGS}
        if want != cur:
            for t in reversed(TAGS):
                if cur[t]: out.append(f"</{t}>")
            for t in TAGS:
                if want[t]: out.append(f"<{t}>")
            cur = want
        out.append(c)
    for t in reversed(TAGS):
        if cur[t]: out.append(f"</{t}>")
    s = "".join(out).replace("\t", " ")
    s = re.sub(r"[  ]{2,}", " ", s)
    for _ in range(3):
        s = re.sub(r" (</(?:b|u|i|sub|sup)>)", r"\1 ", s)
        s = re.sub(r"(<(?:b|u|i|sub|sup)>) ", r" \1", s)
    s = re.sub(r"<(b|u|i|sub|sup)></\1>", "", s)
    s = re.sub(r"</(b|u|i|sub|sup)><\1>", "", s)
    return s.strip()

def join(parts):
    s = ""
    for t in parts:
        if not s: s = t
        elif s.endswith("­"): s = s[:-1] + t
        elif re.search(r"­(</[a-z]+>)+$", s): s = re.sub(r"­((</[a-z]+>)+)$", r"\1", s) + t
        else: s = s + " " + t
    s = s.replace("­", "")
    s = re.sub(r"</(b|u|i|sub|sup)><\1>", "", s)
    s = re.sub(r"(</sub>(?:</i>)?) ([.,])", r"\1\2", s)
    return s

def is_fraction_bar(t, lines):
    above = any(lb.x0 <= (t.x0 + t.x1) / 2 <= lb.x1 and -1 <= t.y0 - lb.y1 <= 4 for lb, _ in lines)
    below = any(lb.x0 - 2 <= (t.x0 + t.x1) / 2 <= lb.x1 + 2 and -1 <= lb.y0 - t.y1 <= 4 for lb, _ in lines)
    return above and below and t.width < 200

def extract(doc, regions, outdir, n):
    events = []  # (page, y, kind, payload)
    figpaths = []
    for ri, (pno, x0, y0, x1, y1) in enumerate(regions):
        page = doc[pno - 1]
        rect = pymupdf.Rect(x0, y0, x1, y1)
        thin, figs = page_info(page)
        lines = build_lines(page, rect, thin, figs)
        # fraction bars -> equation crops
        eq = [t for t in thin if rect.contains(t) and is_fraction_bar(t, lines)]
        eqzones = clusters([t + (-2, -12, 2, 12) for t in eq], gap=4)
        # expand eq zones horizontally to the full visual row of touching lines
        zones = []
        for z in eqzones:
            row = [lb for lb, _ in lines if lb.y0 < z.y1 and lb.y1 > z.y0 and abs((lb.y0 + lb.y1) / 2 - (z.y0 + z.y1) / 2) < 14]
            zz = pymupdf.Rect(z)
            for lb in row: zz |= lb
            zones.append(zz)
        zones = clusters(zones, gap=1)
        regfigs = [f for f in figs if rect.intersects(f) and (f & rect).get_area() > 0.6 * f.get_area()]
        # absorb short labels next to figures (axis numbers, component names)
        for _ in range(3):
            for lb, spans in lines:
                t = "".join(c["c"] for s_ in spans for c in s_["chars"]).strip()
                if len(t) > 28 or ALT.match(t):
                    continue
                for fi, f in enumerate(regfigs):
                    if (f + (-22, -22, 22, 22)).intersects(lb) and not f.contains(lb):
                        regfigs[fi] = f | lb
            regfigs = clusters(regfigs, gap=12)
        for k, box in enumerate(regfigs + zones):
            p = os.path.join(outdir, f"{n}_p{pno}_{k}.png")
            page.get_pixmap(dpi=200, clip=box + (-3, -3, 3, 3)).save(p)
            events.append((ri, box.y0, box.x0, "fig", p))
        for lb, spans in lines:
            c = pymupdf.Point((lb.x0 + lb.x1) / 2, (lb.y0 + lb.y1) / 2)
            if any(z.contains(c) for z in zones) or any(f.contains(c) for f in regfigs):
                continue
            chars = style_chars(spans, rect, thin)
            txt = render(chars)
            if not txt or re.fullmatch(r"QUESTÃO\s+\d+", re.sub(r"<[^>]+>", "", txt)):
                continue
            events.append((ri, lb.y0, lb.x0, "txt", txt))
    events.sort(key=lambda e: (e[0], round(e[1] / 3), e[2]))
    # assemble
    paras, alts, order = [], {}, []
    prev, cur_alt = None, None
    shared, in_shared = [], False
    for pno, y, x, kind, val in events:
        plain = re.sub(r"<[^>]+>", "", val) if kind == "txt" else ""
        if kind == "txt" and SHARED.match(plain):
            in_shared = True
        if in_shared:
            shared.append((pno, y, kind, val)); continue
        if kind == "fig":
            figpaths.append(val)
            tok = f"[[figura {len(figpaths)}]]"
            if cur_alt:
                alts[cur_alt].append((pno, y, tok)); prev = (pno, y + 0)
            else:
                paras.append([tok]); prev = None
            continue
        m = ALT.match(re.sub(r"^<[^>]+>", "", val))
        if m:
            cur_alt = m.group(1); alts[cur_alt] = [(pno, y, val)]; continue
        if cur_alt and alts[cur_alt][-1][0] == pno and 0 <= y - alts[cur_alt][-1][1] < 14:
            alts[cur_alt].append((pno, y, val)); continue
        if cur_alt and alts[cur_alt][-1][2].startswith("[[figura"):
            alts[cur_alt].append((pno, y, val)); continue
        cur_alt = None
        same_flow = prev and prev[0] == pno and 0 <= y - prev[1] < 13
        cross = prev and prev[0] != pno and not re.search(r"[.:?!”)]\s*(</[a-z]+>)*$", paras[-1][-1])
        if paras and (same_flow or cross) and not paras[-1][-1].startswith("[[figura"):
            paras[-1].append(val)
        else:
            paras.append([val])
        prev = (pno, y)
    body = [join(p) for p in paras]
    def altjoin(parts):
        out = []
        for _, _, t in parts:
            if t.startswith("[[figura"): out.append("\n" + t + "\n")
            else: out.append(t)
        s = join([o for o in out])
        return re.sub(r" ?\n ?", "\n", s).strip()
    alt = [altjoin(alts[k]) for k in sorted(alts)]
    # shared text: paragraphs (no alternatives)
    sh, sp = [], None
    for pno, y, kind, val in shared:
        if kind == "fig":
            figpaths.append(val); sh.append([f"[[figura {len(figpaths)}]]"]); sp = None; continue
        if sh and sp and sp[0] == pno and 0 <= y - sp[1] < 13: sh[-1].append(val)
        else: sh.append([val])
        sp = (pno, y)
    return body, alt, figpaths, [join(p) for p in sh]

if __name__ == "__main__":
    pdf, segf, nums, outdir = sys.argv[1:5]
    os.makedirs(outdir, exist_ok=True)
    doc = pymupdf.open(pdf); S = json.load(open(segf))
    for n in [int(x) for x in nums.split(",")]:
        body, alt, figs, shared = extract(doc, S[str(n)], outdir, n)
        json.dump({"body": body, "alts": alt, "figs": figs, "shared_after": shared}, open(os.path.join(outdir, f"{n}.json"), "w"), ensure_ascii=False, indent=1)
        print(f"##### {n}  figs={len(figs)}")
        print("\n\n".join(body)); print(); print("\n".join(alt)); print()
        if shared: print("[SHARED-AFTER]", "\n\n".join(shared)); print()
