# -*- coding: utf-8 -*-
import os

main_tex_path = r"d:\Code\JupyterNotebook\PSO\latex\The Joural of Finance and Data Science\main.tex"
refs_tex_path = r"d:\Code\JupyterNotebook\PSO\references\all\jfds_harvard_references.tex"

with open(refs_tex_path, "r", encoding="utf-8") as f:
    refs_content = f.read()

with open(main_tex_path, "r", encoding="utf-8") as f:
    main_content = f.read()

custom_bib_env = r"""% References environment matching The Journal of Finance and Data Science (Harvard hanging indent, unnumbered)
\renewenvironment{thebibliography}[1]{%
  \section*{\refname}%
  \list{}{%
    \setlength{\leftmargin}{12pt}%
    \setlength{\itemindent}{-12pt}%
    \setlength{\itemsep}{2.5pt plus 0.5pt minus 0.5pt}%
    \setlength{\parsep}{0pt}%
    \usecounter{enumiv}%
    \let\p@enumiv\@empty
    \renewcommand\theenumiv{\relax}%
  }%
  \fontsize{6.5pt}{8.6pt}\selectfont
  \sloppy\clubpenalty4000\widowpenalty4000%
  \sfcode`\.\@m
}{%
  \endlist
}
\def\@biblabel#1{}% Remove [1], [2] brackets
"""

# Insert custom_bib_env right before \makeatother if not already present
if "Harvard hanging indent" not in main_content:
    target_preamble = r"\makeatother"
    main_content = main_content.replace(target_preamble, custom_bib_env + "\n" + target_preamble, 1)

# Extract bibliography block from refs_content
bib_start = refs_content.find(r"\begin{thebibliography}{99}")
clean_refs = refs_content[bib_start:]

# Replace from \begin{thebibliography}{99} to \end{thebibliography}
bib_start_idx = main_content.find(r"\begin{thebibliography}{99}")
bib_end_tag = r"\end{thebibliography}"
bib_end_idx = main_content.find(bib_end_tag)

if bib_start_idx != -1 and bib_end_idx != -1:
    new_main = main_content[:bib_start_idx] + clean_refs + main_content[bib_end_idx + len(bib_end_tag):]
    with open(main_tex_path, "w", encoding="utf-8") as f:
        f.write(new_main)
    print("Successfully updated 74 JFDS Harvard references in main.tex!")
else:
    print("Could not find thebibliography block in main.tex")
