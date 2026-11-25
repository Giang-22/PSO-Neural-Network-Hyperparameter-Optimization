# -*- coding: utf-8 -*-
import os
import re

main_tex_path = r"d:\Code\JupyterNotebook\PSO\latex\The Joural of Finance and Data Science\main.tex"
refs_tex_path = r"d:\Code\JupyterNotebook\PSO\references\all\jfds_harvard_references.tex"

with open(main_tex_path, "r", encoding="utf-8") as f:
    text = f.read()

with open(refs_tex_path, "r", encoding="utf-8") as f:
    refs = f.read()

# 1. Update citation keys in main.tex
key_replacements = {
    r"\cite{kennedy1995pso}": r"\cite{kennedy1995particle}",
    r"\cite{clerc2002constriction}": r"\cite{clerc2002particle}",
    r"\cite{pires2010fractional}": r"\cite{pires2010particle}",
    r"\cite{sun2004qpso, sun2012qpso_analysis}": r"\cite{sun2004global, sun2012quantum}",
    r"\cite{sun2004qpso}": r"\cite{sun2004global}",
    r"\cite{sun2012qpso_analysis}": r"\cite{sun2012quantum}",
    r"\cite{tizhoosh2005obl}": r"\cite{tizhoosh2005opposition}",
    r"\cite{moro2014bank}": r"\cite{moro2014data}",
    r"\cite{blackard1999covertype}": r"\cite{blackard1999comparative}"
}

for old_key, new_key in key_replacements.items():
    text = text.replace(old_key, new_key)

# 2. Update custom thebibliography environment in preamble with raggedbottom and strict spacing
old_env_pattern = re.compile(
    r"% References environment matching The Journal of Finance and Data Science.*?\\def\\@biblabel#1\{\}%\s*Remove \[1\], \[2\] brackets",
    re.DOTALL
)

new_env = r"""% References environment matching The Journal of Finance and Data Science (Harvard hanging indent, unnumbered)
\renewenvironment{thebibliography}[1]{%
  \clearpage
  \raggedbottom
  \section*{\refname}%
  \list{}{%
    \setlength{\leftmargin}{12pt}%
    \setlength{\itemindent}{-12pt}%
    \setlength{\itemsep}{2.2pt}%
    \setlength{\parsep}{0pt}%
    \setlength{\parskip}{0pt}%
    \setlength{\topsep}{0pt}%
    \setlength{\partopsep}{0pt}%
    \usecounter{enumiv}%
    \let\p@enumiv\@empty
    \renewcommand\theenumiv{\relax}%
  }%
  \fontsize{6.5pt}{8.5pt}\selectfont
  \sloppy\clubpenalty4000\widowpenalty4000%
  \sfcode`\.\@m
}{%
  \endlist
}
\def\@biblabel#1{}% Remove [1], [2] brackets"""

if old_env_pattern.search(text):
    text = old_env_pattern.sub(lambda m: new_env, text)
else:
    # If not found with pattern, insert before \makeatother
    text = text.replace(r"\makeatother", new_env + "\n\\makeatother", 1)

# 3. Update the bibliography section
bib_start_idx = text.find(r"\begin{thebibliography}{99}")
bib_end_tag = r"\end{thebibliography}"
bib_end_idx = text.find(bib_end_tag)

clean_refs_start = refs.find(r"\begin{thebibliography}{99}")
clean_refs = refs[clean_refs_start:]

if bib_start_idx != -1 and bib_end_idx != -1:
    text = text[:bib_start_idx] + clean_refs + text[bib_end_idx + len(bib_end_tag):]
    print("Replaced bibliography block successfully!")
else:
    print("Warning: Could not find existing thebibliography block!")

# Remove any extra \clearpage before \begin{thebibliography} if multiple
text = text.replace(r"\clearpage" + "\n\n" + r"\clearpage", r"\clearpage")

with open(main_tex_path, "w", encoding="utf-8") as f:
    f.write(text)

print("main.tex successfully remade with clean references and zero empty phantom items!")
