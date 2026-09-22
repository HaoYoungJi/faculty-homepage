"""Arrange 24作业.tex by teaching week, preserving source and attribution."""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path


SOURCE = Path(sys.argv[1])
DESTINATION = Path(sys.argv[2])
SUPPLEMENT = Path(sys.argv[3])
lines = SOURCE.read_text(encoding="utf-8").splitlines()


def source_part(first: int, last: int) -> str:
    value = "\n".join(lines[first - 1 : last])
    value = re.sub(r"(?m)^\s*\\newpage\s*$", "", value)
    value = re.sub(r"(?m)^\s*\\(?:begin|end)\{center\}\s*$", "", value)
    value = re.sub(r"(?m)^\s*\\Large\{选做(?:题)?\}\s*$", r"\\paragraph{选做题}", value)
    value = re.sub(r"(?m)^\s*(?:\{)?\\Large\{[^\n]*?(?:作业|参考答案|选做|集合的势)[^\n]*?\}(?:\})?\s*$", "", value)
    # The source has a mathematically false Cauchy-product identity.
    value = value.replace(r"\sum_{n=1}^{\infty} q^n \right)^2", r"\sum_{n=0}^{\infty} q^n \right)^2")
    # Clear notation and hypothesis corrections, applied only to the assembled copy.
    value = value.replace(r"\sum_{k=1}^{\infty} |a_n - a_{n+1}|", r"\sum_{n=1}^{\infty} |a_n - a_{n+1}|")
    value = value.replace(r"\frac{a_1}{b_1} = \frac{a_2}{b_2} = \cdots = \frac{a_k}{b_k} $ 或者$a_i, b_i, i = 1, 2, \ldots, k$中至少有一方全为0", r"\text{存在}\lambda \in \mathbb R$使得$a_i=\lambda b_i$($i=1,\ldots,n$)，或$b_1=\cdots=b_n=0$")
    value = value.replace(r"设$f \in R([a, b])$, 令", r"设$f \in R([0, 1])$, 令")
    value = value.replace(r"证明: 级数$\sum_{n=1}^{\infty} a_n$收敛.", r"讨论级数$\sum_{n=1}^{\infty} a_n$关于$p$的敛散性.")
    value = value.replace(r"x_2, x_2 \in E", r"x_1, x_2 \in E")
    value = value.replace(r"h : \mathcal S \to (1, 2 ]", r"h : \mathcal S \to [-2, 2]")
    value = value.replace(r"s_{n-1} \sqrt{2 + s_n}", r"s_{n-1} \sqrt{2 + s_n \sqrt2}")
    value = value.replace(r"\tilde g_n(x) = \begin{cases}", r"\tilde g(x) = \begin{cases}")
    value = value.replace(r"开区间上单调函数的反函数", r"开区间上严格单调函数的反函数")
    return value.strip()


def no_proofs(value: str) -> str:
    return re.sub(r"\\begin\{proof\}(?:\[[^]]*\])?.*?\\end\{proof\}", "", value, flags=re.S)


def balanced(value: str) -> str:
    for kind in ("enumerate", "itemize"):
        opens = len(re.findall(r"\\begin\{" + kind + r"\}", value))
        closes = len(re.findall(r"\\end\{" + kind + r"\}", value))
        if opens > closes:
            value += ("\n" + rf"\end{{{kind}}}") * (opens - closes)
        elif closes > opens:
            value = ((rf"\begin{{{kind}}}" + "\n") * (closes - opens)) + value
    if value.lstrip().startswith(r"\item") and not value.lstrip().startswith(r"\begin"):
        value = r"\begin{enumerate}" + "\n" + value + "\n" + r"\end{enumerate}"
    return value


def heading(start: dt.date, first_week: int, last_week: int | None = None) -> str:
    last_week = last_week or first_week
    a = start + dt.timedelta(weeks=first_week - 1)
    b = start + dt.timedelta(weeks=last_week - 1, days=6)
    if a.month == b.month:
        date = f"{a.month}月{a.day}--{b.day}日"
    else:
        date = f"{a.month}月{a.day}日--{b.month}月{b.day}日"
    week = str(first_week) if first_week == last_week else f"{first_week}--{last_week}"
    return f"{date} · Week {week}"


FALL = dt.date(2024, 9, 9)
SPRING = dt.date(2025, 2, 17)

# Ranges are inclusive, one-based lines of the original TeX. The source's
# standalone final-review set and examination are excluded from weekly work.
weeks = [
    ("秋季", "f1", heading(FALL, 1), [(49, 177)], [(894, 1074)]),
    ("秋季", "f2", heading(FALL, 2), [(184, 451)], [(1077, 1267)]),
    ("秋季", "f3", heading(FALL, 3), [(458, 592)], [(1276, 1446)]),
    ("秋季", "f4", heading(FALL, 4), [(599, 654)], [(1447, 1639)]),
    ("秋季", "f5", heading(FALL, 5), [(661, 830)], [(1640, 1776)]),
    ("秋季", "f6", heading(FALL, 6), [(837, 885)], []),
    ("秋季", "f8", heading(FALL, 8), [(1783, 1913)], [(1922, 2105)]),
    ("秋季", "f9", heading(FALL, 9), [(2112, 2165)], []),
    ("秋季", "f10", heading(FALL, 10), [(2171, 2239)], []),
    ("秋季", "f12", heading(FALL, 12), [(2245, 2286)], []),
    ("春季", "s1", heading(SPRING, 1), [(3024, 3050)], []),
    ("春季", "s2", heading(SPRING, 2), [(3056, 3086)], []),
    ("春季", "s3", heading(SPRING, 3), [(3092, 3201)], []),
    ("春季", "s4", heading(SPRING, 4), [(3208, 3246)], []),
    ("春季", "s5", heading(SPRING, 5), [(3253, 3306)], []),
    ("春季", "s6", heading(SPRING, 6), [(3312, 3352)], []),
    ("春季", "s9", heading(SPRING, 9), [(3358, 3412)], [(3948, 4089)]),
    ("春季", "s1011", heading(SPRING, 10, 11), [(3752, 3804)], [(3813, 3947)]),
    ("春季", "s12", heading(SPRING, 12), [(4096, 4120)], []),
    ("春季", "s13", heading(SPRING, 13), [(4127, 4135), (4141, 4181), (4188, 4224)], []),
    ("春季", "s14", heading(SPRING, 14), [(4231, 4256), (4263, 4300)], []),
]


def supplements() -> dict[str, str]:
    value = SUPPLEMENT.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^% ANSWERS: ([a-z0-9]+)\s*$", value))
    results = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(value)
        results[match.group(1)] = value[match.end() : end].strip()
    return results


answers = supplements()
missing = {key for _, key, _, _, _ in weeks} - answers.keys()
if missing:
    raise SystemExit(f"Missing GPT answer sections: {sorted(missing)}")

preamble = "\n".join(lines[:35])
preamble = preamble.replace("oneside", "oneside, fontset=none")
preamble = preamble.replace(r"\usepackage{ctex}", r"\usepackage{ctex}" + "\n" + r"\setCJKmainfont{Songti SC}" + "\n" + r"\setCJKsansfont{Hiragino Sans GB}")
preamble = re.sub(r"\\title\{.*", r"\\title{数学分析习题课作业\\\\2024--2025学年按周整理}", preamble)
preamble = preamble.replace(r"\date{\today}", r"\date{}")
output = [preamble, r"\begin{document}", r"\maketitle",
          r"\noindent\textbf{编排说明：}本册按郑州大学教学周整理，每周先列作业，再列答案。日期表示整周，并非具体上课日。原稿答案保留并单列；新增答案标注“GPT 补充参考答案”，须由任课教师进一步审阅。原稿中的期末试题、春季期中测验及单独的“数学分析300题”未收入本册。已修正发现的明确符号笔误，并在相关答案处说明原题条件不足之处。",
          r"\tableofcontents", r"\clearpage", r"\chapter{秋季学期}"]
term = "秋季"
for semester, key, title, questions, originals in weeks:
    if semester != term:
        term = semester
        output.extend([r"\clearpage", rf"\chapter{{{term}学期}}"])
    raw_questions = "\n\n".join(source_part(*span) for span in questions)
    question_text = no_proofs(raw_questions)
    original_answers = [balanced(source_part(*span)) for span in originals]
    if raw_questions != question_text:
        original_answers.append(raw_questions)
    output += [r"\clearpage", rf"\section{{{title}}}", r"\subsection*{作业}", question_text,
               r"\subsection*{原稿参考答案}"]
    output.extend(original_answers or [r"\noindent 原稿未附这一周的参考答案。"])
    output += [r"\subsection*{GPT 补充参考答案}", answers[key]]
output += [r"\end{document}", ""]
DESTINATION.parent.mkdir(parents=True, exist_ok=True)
DESTINATION.write_text("\n\n".join(output), encoding="utf-8")
