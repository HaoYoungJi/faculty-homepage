"""Rearrange the teacher's 2023-2024 TeX homework by teaching week."""

from __future__ import annotations

import re
import sys
from pathlib import Path


SOURCE = Path(sys.argv[1])
DESTINATION = Path(sys.argv[2])
lines = SOURCE.read_text(encoding="utf-8").splitlines()


def part(first: int, last: int) -> str:
    """Return an inclusive, one-based source excerpt without page breaks."""
    value = "\n".join(lines[first - 1 : last])
    value = re.sub(r"(?m)^\s*\\newpage\s*$", "", value)
    value = re.sub(r"(?m)^\s*\\(?:begin|end)\{center\}\s*$", "", value)
    # Correct two unambiguous notation errors in the source's
    # Cauchy--Schwarz exercise while leaving the original file untouched.
    value = value.replace(
        r"$\frac{a_1}{b_1} = \frac{a_2}{b_2} = \cdots = \frac{a_k}{b_k} $ 或者$a_i, b_i, i = 1, 2, \ldots, k$中至少有一方全为0.",
        r"存在$\lambda\in\mathbb R$使得$a_i=\lambda b_i$（$1\leq i\leq n$），或者$b_1=\cdots=b_n=0$.",
    )
    value = value.replace(
        r"\sum\limits_{j=i+1}^n (|a_k||b_i| - |a_i||b_k|)^2",
        r"\sum\limits_{j=k+1}^n (|a_k||b_j| - |a_j||b_k|)^2",
    )
    return value.strip()


def without_proofs(value: str) -> str:
    # The source does not nest proof environments. Their text belongs below
    # the assignment under the corresponding week's answer heading.
    value = re.sub(
        r"\\begin\{proof\}(?:\[[^]]*\])?.*?\\end\{proof\}",
        "",
        value,
        flags=re.S,
    )
    return re.sub(r"\n{3,}", "\n\n", value)


def list_excerpt(first: int, last: int, kind: str) -> str:
    value = part(first, last)
    opens = len(re.findall(r"\\begin\{" + kind + r"\}", value))
    closes = len(re.findall(r"\\end\{" + kind + r"\}", value))
    if opens == closes and value.lstrip().startswith(r"\item"):
        value = rf"\begin{{{kind}}}" + "\n" + value + "\n" + rf"\end{{{kind}}}"
    elif opens > closes:
        value += ("\n" + rf"\end{{{kind}}}") * (opens - closes)
    elif closes > opens:
        value = ((rf"\begin{{{kind}}}" + "\n") * (closes - opens)) + value
    return value


# Dates remain as written in the source: its first autumn entry is named
# "first week", while later autumn entries have dates but no week numbers.
weeks = [
    ("秋季", "第一周", (48, 63), [(70, 117, "itemize")]),
    ("秋季", "10月7—8日这一周", (126, 163), [(169, 262, "itemize")]),
    ("秋季", "10月12—13日这一周", (269, 311), []),
    ("秋季", "10月19—20日这一周", (317, 378), [(548, 652, "itemize")]),
    ("秋季", "10月26—27日这一周", (383, 440), [(653, 809, "itemize")]),
    ("秋季", "11月2—3日这一周", (445, 477), [(974, 1066, "itemize")]),
    ("秋季", "11月9—10日这一周", (484, 540), [(1068, 1205, "itemize")]),
    ("秋季", "11月16—17日这一周", (938, 966), [(1207, 1337, "itemize")]),
    ("秋季", "12月7—8日这一周", (1597, 1624), [(1754, 1781, "enumerate")]),
    ("秋季", "12月14—15日这一周", (1629, 1676), [(1782, 1852, "enumerate")]),
    ("秋季", "12月21—22日这一周", (1681, 1714), [(1853, 2002, "enumerate")]),
    ("秋季", "12月28—29日这一周", (1719, 1743), []),
    ("春季", "3月25--31日 · Week 5", (2010, 2065), [(2120, 2303, "enumerate")]),
    ("春季", "4月1--7日 · Week 6", (2071, 2110), [(2309, 2507, "enumerate")]),
    ("春季", "4月22--28日 · Week 9", (2919, 3650), [(2512, 2911, "enumerate")]),
    ("春季", "5月13--19日 · Week 12", (4052, 4094), [(4102, 4238, "enumerate")]),
    ("春季", "5月27日--6月2日 · Week 14", (4243, 4278), []),
    ("春季", "6月3--9日 · Week 15", (4282, 4485), []),
]


preamble_lines = lines[:33]
preamble_lines[2] = preamble_lines[2].replace("oneside", "oneside, fontset=none")
preamble_lines[13] = r"\title{数学分析习题课作业\\2023--2024学年按周整理}"
preamble = "\n".join(preamble_lines)
preamble = preamble.replace(r"\usepackage{ctex}", r"\usepackage{ctex}" + "\n" + r"\setCJKmainfont{Songti SC}" + "\n" + r"\setCJKsansfont{Hiragino Sans GB}")
preamble = preamble.replace(r"\date{\today}", r"\date{}")
document = [
    preamble,
    r"\begin{document}",
    r"\maketitle",
    r"\noindent\textbf{编排说明：}本册按原稿标出的周次或日期整理，逐周先列作业，再列对应的部分参考答案。原稿未附对应答案的周次已明确标注。春季日期依郑州大学校历推算，表示整周范围，并非具体上课日。期中考试与春季小测验未收入本册；除两处明确的符号笔误外，题目与解答保持原稿写法。",
    r"\vspace{1em}",
    r"\tableofcontents",
    r"\clearpage",
    r"\chapter{秋季学期}",
]

term = "秋季"
for semester, label, question, solutions in weeks:
    if semester != term:
        term = semester
        document += [r"\clearpage", rf"\chapter{{{term}学期}}"]
    title = label.replace("—", "--")
    question_text = part(*question)
    question_only = without_proofs(question_text)
    has_inline_proofs = question_text != question_only
    document += [
        r"\clearpage",
        rf"\section{{{title}}}",
        r"\subsection*{作业}",
        question_only,
        r"\subsection*{参考答案}",
    ]
    if not solutions and not has_inline_proofs:
        document.append(r"\noindent\emph{原稿未附这一周对应的参考答案。}")
    else:
        if solutions:
            document.append(r"\noindent\emph{以下为按题干归入本周的原稿部分参考答案。}")
            for first, last, kind in solutions:
                document.append(list_excerpt(first, last, kind))
        if has_inline_proofs:
            document += [
                r"\paragraph{原稿中随题附有的解答}",
                question_text,
            ]

document += [r"\end{document}", ""]
DESTINATION.parent.mkdir(parents=True, exist_ok=True)
DESTINATION.write_text("\n\n".join(document), encoding="utf-8")
