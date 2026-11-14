r"""Vídeo (Manim) de uma resolução animada, gerado a partir do mesmo roteiro do app.

  ROTEIRO=unesp-2025-q78 manim -qh videos/manim_roteiro.py Roteiro
  (o MP4 sai em media/videos/manim_roteiro/1080p60/Roteiro.mp4; renomeie para <id>.mp4)

Requer manim (pip install manim) e LaTeX. O roteiro é data/animacoes/<id>.json; os passos
(conceito, texto, equações, pergunta) e a cena ("mostrar", "ocultar", "destacar", "estado")
são os mesmos que o player do app usa. Cada modelo de cena tem aqui uma versão em Manim
(MODELOS); por enquanto só "plano-inclinado". A geometria segue a do app (coordenadas do
SVG de 640 × 430 convertidas para a tela do Manim).
"""
import json
import math
import os
import re
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UL, UP, Arc, Arrow, Create, DashedLine, FadeIn, FadeOut, Indicate,
                   Line, MathTex, Polygon, Rectangle, Scene, Tex, TexTemplate, Text, ValueTracker, VGroup,
                   Circle, Dot, Write, config, linear, always_redraw)

RAIZ = Path(__file__).resolve().parent.parent
config.background_color = "#ffffff"

TINTA, MUDO, LINHA = "#18202b", "#5b6676", "#d5dbe3"
COR = {"peso": "#d4583f", "normal": "#1f4fbf", "atrito": "#1d7a4a", "acel": "#7a45c9", "madeira": "#c98a5a", "caixa": "#f07a2a"}

TEMPLATE = TexTemplate(documentclass=r"\documentclass[preview]{standalone}", preamble=r"""\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xcolor}
\usepackage{icomma}
\DeclareMathOperator{\sen}{sen}""")


def tex_math(s: str) -> str:
    """LaTeX do app -> LaTeX do Manim (vírgula decimal, \text com acento)."""
    s = s.replace("\\dfrac", "\\dfrac").replace("°", "^{\\circ}")
    return s


def tex_texto(s: str) -> str:
    """Texto do roteiro (marcação do app) -> texto LaTeX."""
    partes = re.split(r"(\\\(.+?\\\))", s)
    out = []
    for p in partes:
        if p.startswith("\\("):
            out.append("$" + tex_math(p[2:-2]) + "$")
            continue
        p = p.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")
        p = p.replace("²", "$^{2}$").replace("¾", "$\\tfrac{3}{4}$").replace("≈", "$\\approx$").replace("θ", "$\\theta$").replace("·", "$\\cdot$")
        p = re.sub(r"<b>(.+?)</b>", r"\\textbf{\1}", p)
        p = re.sub(r"<i>(.+?)</i>", r"\\textit{\1}", p)
        p = re.sub(r"<sub>(.+?)</sub>", r"$_{\\text{\1}}$", p)
        p = re.sub(r"<sup>(.+?)</sup>", r"$^{\\text{\1}}$", p)
        p = re.sub(r"</?u>", "", p)
        out.append(p)
    return "".join(out)


def paragrafo(s: str, largura_cm=7.6, tamanho=26, cor=TINTA):
    return Tex(r"\parbox{%scm}{\raggedright %s}" % (largura_cm, tex_texto(s)), tex_template=TEMPLATE, font_size=tamanho, color=cor)


class PlanoInclinado:
    """Mesma cena do app (CENAS["plano-inclinado"]), em Manim."""

    def __init__(self, P):
        self.sen, self.cos, self.mu, self.g = P["senTheta"], P["cosTheta"], P["mu"], P["g"]
        self.deg = math.degrees(math.atan2(self.sen, self.cos))
        self.amax = self.mu * self.g * self.cos - self.g * self.sen
        self.O, self.L = (70, 300), 440
        self.u, self.n = (self.cos, -self.sen), (-self.sen, -self.cos)
        self.s = ValueTracker(200)          # posição da caixa ao longo da rampa (px do SVG)
        self.fita = ValueTracker(0)          # deslocamento da esteira
        self.f = ValueTracker(self.mu * self.g * self.cos)   # atrito desenhado (em unidades de m)
        self.el = self._montar()

    # coordenadas do SVG (640 × 430) -> tela do Manim (região à esquerda)
    @staticmethod
    def M(x, y):
        k = 8.2 / 640
        return [-7.0 + x * k, 2.75 - y * k, 0]

    def pt(self, s, h):
        return (self.O[0] + s * self.u[0] + h * self.n[0], self.O[1] + s * self.u[1] + h * self.n[1])

    def _montar(self):
        M, pt, u, n, g = self.M, self.pt, self.u, self.n, self.g
        el = {}
        b0, b1, c1, c0 = pt(0, 0), pt(self.L, 0), pt(self.L, -18), pt(0, -18)
        T = pt(self.L, 0)
        rampa = VGroup(
            Line(M(10, 300), M(630, 300), color=TINTA, stroke_width=3),
            Polygon(M(10, 284), M(70, 284), M(70, 300), M(10, 300), fill_color=COR["madeira"], fill_opacity=.8, stroke_width=0),
            Polygon(M(T[0], T[1] - 2), M(T[0] + 200, T[1] - 2), M(T[0] + 200, T[1] + 14), M(T[0], T[1] + 14), fill_color=COR["madeira"], fill_opacity=.8, stroke_width=0),
            *[Polygon(M(x, T[1] + 14), M(x + 7, T[1] + 14), M(x + 7, 300), M(x, 300), fill_color="#a8692e", fill_opacity=1, stroke_width=0) for x in (530, 600)],
            Polygon(M(*b0), M(*b1), M(*c1), M(*c0), color=TINTA, stroke_width=3, fill_color="#ffffff", fill_opacity=1),
            *[VGroup(Circle(radius=11 * 8.2 / 640, color=TINTA, stroke_width=2, fill_color="#f2c230", fill_opacity=1).move_to(M(*pt(s, -9))),
                     Dot(M(*pt(s, -9)), radius=0.03, color=TINTA)) for s in (9, self.L - 9)],
        )
        fita = always_redraw(lambda: VGroup(*[
            Line(M(*pt(a, -3)), M(*pt(min(a + 10, self.L - 14), -3)), color=MUDO, stroke_width=2)
            for a in [14 + ((k * 19 + self.fita.get_value()) % (self.L - 28)) for k in range(int((self.L - 28) / 19))] if a < self.L - 16]))
        el["rampa"] = VGroup(rampa, fita)
        el["angulo"] = VGroup(Arc(radius=56 * 8.2 / 640, start_angle=0, angle=math.radians(self.deg), arc_center=M(*self.O), color=TINTA, stroke_width=2),
                              MathTex(r"\theta", color=TINTA, font_size=30).move_to(M(self.O[0] + 76 * math.cos(math.radians(self.deg / 2)), self.O[1] - 76 * math.sin(math.radians(self.deg / 2)))))

        def caixa():
            s = self.s.get_value()
            cs = [pt(s - 28, 0), pt(s + 28, 0), pt(s + 28, 46), pt(s - 28, 46)]
            return Polygon(*[M(*p) for p in cs], color=TINTA, stroke_width=3, fill_color=COR["caixa"], fill_opacity=1)
        el["caixa"] = always_redraw(caixa)

        def C():
            return pt(self.s.get_value(), 23)

        def add(p, v, k):
            return (p[0] + v[0] * k, p[1] + v[1] * k)

        def seta(cor, fim, larg=6, dash=False):
            def f():
                c = C(); e = fim(c)
                cls = DashedLine if dash else Line
                a = Arrow(M(*c), M(*e), buff=0, color=cor, stroke_width=larg, max_tip_length_to_length_ratio=0.18, tip_length=0.2)
                if dash:
                    return VGroup(DashedLine(M(*c), M(*e), color=cor, stroke_width=4, dash_length=0.1), a.tip.copy())
                return a
            return always_redraw(f)

        def rot(txt, cor, onde, fs=32):
            return always_redraw(lambda: MathTex(txt, color=cor, font_size=fs).move_to(M(*onde(C()))))

        K = 10
        el["peso"] = VGroup(seta(COR["peso"], lambda c: (c[0], c[1] + g * K)), rot(r"\vec P", COR["peso"], lambda c: (c[0] + 18, c[1] + g * K - 6)))
        el["normal"] = VGroup(seta(COR["normal"], lambda c: add(c, n, g * self.cos * K)), rot(r"\vec N", COR["normal"], lambda c: add(c, n, g * self.cos * K + 16)))
        el["atrito"] = VGroup(seta(COR["atrito"], lambda c: add(c, u, self.f.get_value() * K)), rot(r"\vec f", COR["atrito"], lambda c: add(add(c, u, self.f.get_value() * K + 16), n, 8)))
        el["componentes"] = VGroup(
            seta(COR["peso"], lambda c: add(c, u, -g * self.sen * K), 4, True), seta(COR["peso"], lambda c: add(c, n, -g * self.cos * K), 4, True),
            rot(r"P_x", COR["peso"], lambda c: add(add(c, u, -g * self.sen * K - 18), n, 6), 28), rot(r"P_y", COR["peso"], lambda c: (add(c, n, -g * self.cos * K)[0] + 20, add(c, n, -g * self.cos * K)[1] + 6), 28),
            always_redraw(lambda: VGroup(
                DashedLine(M(C()[0], C()[1] + g * K), M(*add(C(), u, -g * self.sen * K)), color=MUDO, stroke_width=2, dash_length=0.06),
                DashedLine(M(C()[0], C()[1] + g * K), M(*add(C(), n, -g * self.cos * K)), color=MUDO, stroke_width=2, dash_length=0.06))))
        a1 = math.degrees(math.atan2(-n[1], -n[0]))   # direção de -n na tela do SVG
        el["angulo-peso"] = always_redraw(lambda: VGroup(
            Arc(radius=36 * 8.2 / 640, start_angle=-math.radians(90), angle=math.radians(90 - a1), arc_center=M(*C()), color=TINTA, stroke_width=2),
            MathTex(r"\theta", color=TINTA, font_size=28).move_to(M(C()[0] + 52 * math.cos(math.radians((a1 + 90) / 2)), C()[1] + 52 * math.sin(math.radians((a1 + 90) / 2))))))
        el["eixos"] = always_redraw(lambda: VGroup(
            DashedLine(M(*add(C(), u, -150)), M(*add(C(), u, 170)), color=MUDO, stroke_width=2, dash_length=0.08),
            DashedLine(M(*add(C(), n, -60)), M(*add(C(), n, 130)), color=MUDO, stroke_width=2, dash_length=0.08),
            MathTex("x", color=MUDO, font_size=28).move_to(M(*add(C(), u, 184))), MathTex("y", color=MUDO, font_size=28).move_to(M(*add(C(), n, 144)))))
        el["aceleracao"] = always_redraw(lambda: VGroup(
            Arrow(M(*add(add(C(), n, 72), u, -10)), M(*add(add(C(), n, 72), u, 36)), buff=0, color=COR["acel"], stroke_width=6, tip_length=0.18),
            MathTex(r"\vec a", color=COR["acel"], font_size=30).move_to(M(*add(add(add(C(), n, 72), u, 36), n, 16)))))
        # balanço ao longo da rampa
        BX, BK = 240, 40
        fm, ps = self.mu * g * self.cos, g * self.sen
        barra = lambda y, w, cor, op=.85: Polygon(M(BX, y), M(BX + w, y), M(BX + w, y + 22), M(BX, y + 22), stroke_width=0, fill_color=cor, fill_opacity=op)
        el["balanco"] = VGroup(
            barra(331, fm * BK, COR["atrito"]), barra(369, ps * BK, COR["peso"]),
            Tex(r"atrito máximo: $6{,}4m$", tex_template=TEMPLATE, font_size=24, color=TINTA).next_to(M(BX - 8, 342), LEFT, buff=0),
            Tex(r"$P_x = mg\sen\theta$: $6m$", tex_template=TEMPLATE, font_size=24, color=TINTA).next_to(M(BX - 8, 380), LEFT, buff=0),
            Polygon(M(BX + ps * BK, 326), M(BX + fm * BK, 326), M(BX + fm * BK, 396), M(BX + ps * BK, 396), stroke_width=0, fill_color=COR["acel"], fill_opacity=.25),
            Tex(r"sobra $0{,}4m = m\,a$", tex_template=TEMPLATE, font_size=24, color=COR["acel"]).move_to(M(BX + fm * BK + 70, 412)),
        )
        return el

    def estado(self, scene, est):
        """Animações de estado (movimento da esteira, varredura da aceleração)."""
        if est.get("movimento") == "acelerando":
            self.s.set_value(110); self.fita.set_value(0)
            scene.play(self.s.animate.set_value(110 + 30 * 0.5 * self.amax * 16), self.fita.animate.set_value(30 * 0.5 * self.amax * 16), run_time=4, rate_func=lambda t: t * t)
            scene.play(self.s.animate.set_value(200), run_time=0.8)
        if est.get("controle") == "aceleracao":
            a = ValueTracker(0.2)
            leitura = always_redraw(lambda: Tex(
                r"\parbox{9cm}{\raggedright aceleração da esteira: $a = %s$ m/s$^2$\\ atrito necessário: $%sm$ (máximo: $6{,}4m$)\\ %s}" % (
                    f"{a.get_value():.2f}".replace(".", "{,}"), f"{self.g * self.sen + a.get_value():.2f}".replace(".", "{,}"),
                    r"\textcolor[HTML]{1D7A4A}{a caixa acompanha a esteira}" if a.get_value() <= self.amax + 1e-6 else r"\textcolor[HTML]{B3261E}{a caixa escorrega}"),
                tex_template=TEMPLATE, font_size=26, color=TINTA).move_to([-2.9, -3.55, 0]))
            self.f.add_updater(lambda m: m.set_value(min(self.g * self.sen + a.get_value(), self.mu * self.g * self.cos)))
            scene.add(leitura)
            for alvo in (self.amax, 0.8, self.amax):
                scene.play(a.animate.set_value(alvo), run_time=2.5, rate_func=linear)
                scene.wait(1.2)
            self.f.clear_updaters()
            scene.play(FadeOut(leitura))


MODELOS = {"plano-inclinado": PlanoInclinado}


class Roteiro(Scene):
    def construct(self):
        rid = os.environ.get("ROTEIRO", "unesp-2025-q78")
        rot = json.loads((RAIZ / "data" / "animacoes" / f"{rid}.json").read_text(encoding="utf-8"))
        cena = MODELOS[rot["cena"]["modelo"]](rot["cena"].get("parametros", {}))
        # abertura
        titulo = Tex(tex_texto(rot["titulo"]), tex_template=TEMPLATE, font_size=44, color=TINTA)
        sub = Text(rid, font="Monospace", font_size=20, color=MUDO).next_to(titulo, DOWN)
        conc = Tex(r" \textbullet{} ".join(rot["conceitos"]), tex_template=TEMPLATE, font_size=26, color="#1f4fbf").next_to(sub, DOWN, buff=0.4)
        self.play(Write(titulo), FadeIn(sub), FadeIn(conc)); self.wait(2)
        self.play(FadeOut(titulo), FadeOut(sub), FadeOut(conc))
        vis, painel = set(), VGroup()
        X0 = 1.75
        for i, p in enumerate(rot["passos"], 1):
            c = p.get("cena", {})
            entram = [e for e in c.get("mostrar", []) if e not in vis]
            saem = [e for e in c.get("ocultar", []) if e in vis]
            # painel de texto
            cab = VGroup(paragrafo("Conceito: " + p["conceito"] if p.get("conceito") else "", 7.2, 22, "#1f4fbf"),
                         paragrafo("<b>%d. %s</b>" % (i, p["titulo"]), 7.2, 32)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            corpo = paragrafo(p["texto"], 7.2, 25)
            novo = VGroup(cab, corpo).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL).shift(RIGHT * (X0 + 7.1 - 0.5))
            novo.align_to([X0, 0, 0], LEFT).align_to([0, 3.7, 0], UP)
            self.play(FadeOut(painel), *[FadeOut(cena.el[e]) for e in saem], run_time=0.6)
            vis.difference_update(saem)
            self.play(FadeIn(novo, shift=UP * 0.1), *[Create(cena.el[e]) if e in ("rampa", "angulo") else FadeIn(cena.el[e]) for e in entram], run_time=1.2)
            vis.update(entram)
            painel = VGroup(novo)
            for d in c.get("destacar", []):
                if d in cena.el: self.play(Indicate(cena.el[d], color=None, scale_factor=1.08), run_time=0.9)
            self.wait(min(9, 2 + len(re.sub(r"<[^>]+>|\\\(.+?\\\)", "x", p["texto"])) / 22))
            if p.get("equacoes"):
                eqs = VGroup(*[MathTex(tex_math(e), tex_template=TEMPLATE, font_size=34, color=TINTA) for e in p["equacoes"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
                eqs.next_to(novo, DOWN, aligned_edge=LEFT, buff=0.35)
                for e in eqs:
                    self.play(Write(e), run_time=1.2); self.wait(1.2)
                painel.add(eqs)
            cena.estado(self, c.get("estado", {}))
            if p.get("pergunta"):
                q = VGroup(Text("PENSE ANTES DE AVANÇAR", font_size=16, color=COR["peso"], weight="BOLD"), paragrafo(p["pergunta"]["texto"], 7.2, 24))
                q.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(painel, DOWN, aligned_edge=LEFT, buff=0.35)
                self.play(FadeIn(q)); self.wait(4)
                r = paragrafo(p["pergunta"]["resposta"], 7.2, 24, "#7a2b1e").next_to(q, DOWN, aligned_edge=LEFT, buff=0.15)
                self.play(FadeIn(r)); self.wait(4.5)
                painel.add(q, r)
            self.wait(1.5)
        self.wait(2)
