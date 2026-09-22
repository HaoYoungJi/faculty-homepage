"""Arrange the 2025--2026 mathematics-analysis homework from its TeX source."""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path


SOURCE = Path(sys.argv[1])
DESTINATION = Path(sys.argv[2])
SUPPLEMENT = Path(sys.argv[3])
lines = SOURCE.read_text(encoding="utf-8").splitlines()


def excerpt(first: int, last: int) -> str:
    """Take inclusive one-based lines, dropping the source's page heading."""
    value = "\n".join(lines[first - 1:last])
    start = value.find(r"\begin{enumerate}")
    if start < 0:
        raise ValueError(f"No exercise list in {first}--{last}")
    value = value[start:]
    value = re.sub(r"(?m)^\s*\\newpage\s*$", "", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    # Corrections to clear notation errors in the assembled copy only.
    value = value.replace(
        r"$b_k = c a_k, c \neq 0, \forall 1 \leq k \leq n $ 或者$a_k, b_k, k = 1, 2, \ldots, n$中至少有一方全为0",
        r"两向量$(a_k)_{k=1}^n$与$(b_k)_{k=1}^n$线性相关（包括其中一向量为零）",
    )
    value = value.replace(r"\item.", r"\item")
    value = value.replace(r"$O(x^2) = o(x)$", r"$O(x^2) \subset o(x)$")
    value = value.replace(r"\sum_{k=2}^{\infty} \frac{1}{n \ln^p n}", r"\sum_{n=2}^{\infty} \frac{1}{n \ln^p n}")
    value = value.replace(r"\int_2^{+\infty} \frac{dx}{x (\ln x)(\ln \ln x)^p}",
                          r"\int_{e^e}^{+\infty} \frac{dx}{x (\ln x)(\ln \ln x)^p}")
    value = value.replace(r"$I_n = \int \sec^n x dx $, $I_n = \int \tan^n x dx $, $I_n = \int \cos^n x dx $",
                          r"$I_n = \int \sec^n x\,dx$, $J_n = \int \tan^n x\,dx$, $K_n = \int \cos^n x\,dx$")
    value = value.replace(
        r"若$\int_1^{+\infty} f(x) dx = +\infty$, 则$I$发散但$J$收敛, 其中",
        r"若$\int_1^{+\infty} f(x) dx = +\infty$，令唯一的$c>1$满足$F(c)=e$。证明$I$发散但$J$收敛，其中",
    )
    value = value.replace(
        r"I = \int_1^{+\infty} \frac{f(x)}{F(x) \ln F(x)} dx, \ J = \int_2^{+\infty} \frac{f(x)}{F(x) \ln^2 F(x)} dx.",
        r"I = \int_c^{+\infty} \frac{f(x)}{F(x) \ln F(x)} dx, \ J = \int_c^{+\infty} \frac{f(x)}{F(x) \ln^2 F(x)} dx.",
    )
    return value.strip()


def section_answers() -> dict[str, str]:
    value = SUPPLEMENT.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^% ANSWERS: ([a-z0-9]+)\s*$", value))
    answers = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(value)
        answers[match.group(1)] = value[match.end():end].strip()
    return answers


FALL_START = dt.date(2025, 9, 8)
FALL = [
    ("f1", "10月20日交", 7, [(41, 141, None)], (142, 388)),
    ("f2", "10月27日交", 8, [(389, 529, None)], None),
    ("f3", "11月3日交", 9, [(530, 703, "3、4、7、8班"), (802, 901, "1、2、5、6班")], None),
    ("f4", "11月10日交", 10, [(1038, 1195, "1、2、5、6班"), (1196, 1260, "3、4、7、8班")], None),
    ("f5", "11月17日交", 11, [(1261, 1338, "1、2、5、6班"), (1471, 1525, "3、4、7、8班"), (1339, 1470, "共同选做题")], None),
    ("f6", "11月25日交", 12, [(1657, 1707, None)], None),
    ("f7", "12月1日交", 13, [(1708, 1762, None), (1763, 1844, "选做题")], None),
    ("f8", "12月8日交", 14, [(1845, 1915, None)], None),
    ("f9", "12月15日交", 15, [(1916, 1951, None)], None),
    ("f10", "12月22日交", 16, [(1952, 2016, None)], None),
    ("f11", "12月29日交", 17, [(2017, 2049, None)], None),
]

SPRING = [
    ("s1", 1, (2254, 2315)),
    ("s2", 2, (2316, 2366)),
    ("s3", 3, (2367, 2436)),
    ("s4", 4, (2437, 2490)),
    ("s5", 5, (2491, 2549)),
    ("s6", 6, (2550, 2606)),
    ("s7", 7, (2674, 2714)),
    ("s8", 8, (2715, 2763)),
    ("s9", 9, (2764, 2845)),
    ("s10", 10, (2846, 2892)),
]

answers = section_answers()
missing = {entry[0] for entry in FALL + SPRING} - answers.keys()
if missing:
    raise SystemExit(f"Missing answer sections: {sorted(missing)}")

preamble = "\n".join(lines[:40])
preamble = preamble.replace("fontset=mac", "fontset=none")
preamble = preamble.replace(r"\usepackage{ctex}", r"\usepackage{ctex}" + "\n" + r"\setCJKmainfont{Songti SC}" + "\n" + r"\setCJKsansfont{Hiragino Sans GB}")
output = [
    preamble,
    r"\title{数学分析习题课作业\\2025--2026学年按周整理}",
    r"\author{吉浩洋}",
    r"\date{}",
    r"\begin{document}",
    r"\maketitle",
    r"\tableofcontents",
    r"\vspace{1.5em}",
    r"\noindent\textbf{编排说明：}秋季依据原稿交作业日期标注教学周；春季原稿仅列作业次序，故以“第几次作业”排列，不另拟具体日期。每次先列作业，再列原稿参考答案（如有）及注明来源的 GPT 选题参考答案。按班级区分的题目保留班级标记；重复的共同选做题只列一次。教材仅给出章节、页码或题号的题目，答案处写“参见教材”。明确的符号笔误已在本册修正；新增答案须由任课教师进一步审阅。",
    r"\clearpage",
    r"\chapter{秋季学期}",
]

for key, due, week, parts, original in FALL:
    start = FALL_START + dt.timedelta(weeks=week - 1)
    end = start + dt.timedelta(days=6)
    if start.month == end.month:
        period = f"{start.month}月{start.day}--{end.day}日"
    else:
        period = f"{start.month}月{start.day}日--{end.month}月{end.day}日"
    output.extend([r"\clearpage", rf"\section{{{period} · Week {week}（{due}）}}", r"\subsection*{作业}"])
    for first, last, label in parts:
        if label:
            output.append(rf"\subsubsection*{{{label}}}")
        output.append(excerpt(first, last))
    if original:
        original_text = excerpt(*original)
        original_text = re.sub(
            r"\\begin\{proof\}\s*这里我们给出应用Young不等式.*?\\end\{proof\}",
            lambda _: r"\begin{proof}原稿此处的 Young 不等式证明未定义 $p,q$，改用 Lagrange 恒等式：\[\left(\sum_{k=1}^n a_k^2\right)\left(\sum_{k=1}^n b_k^2\right)-\left(\sum_{k=1}^n a_kb_k\right)^2=\sum_{1\le i<j\le n}(a_ib_j-a_jb_i)^2\ge0.\]等号成立当且仅当两向量线性相关。\end{proof}",
            original_text,
            count=1,
            flags=re.S,
        )
        output.extend([r"\subsection*{原稿参考答案（已校正明确笔误）}", original_text])
    output.extend([r"\subsection*{GPT 补充参考答案（选题）}", answers[key]])

output.extend([r"\clearpage", r"\chapter{春季学期}"])
for key, number, span in SPRING:
    output.extend([
        r"\clearpage", rf"\section{{第{number}次作业 / Homework {number}}}",
        r"\subsection*{作业}", excerpt(*span),
        r"\subsection*{GPT 补充参考答案（选题）}", answers[key],
    ])
output.extend([r"\end{document}", ""])
DESTINATION.parent.mkdir(parents=True, exist_ok=True)
DESTINATION.write_text("\n".join(output), encoding="utf-8")
