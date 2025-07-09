# app/services/pdf_generator.py
import logging
import subprocess
import shutil
from pathlib import Path
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)

def escape_latex(text: str) -> str:
    """Escapes special LaTeX characters in a given string."""
    if not isinstance(text, str):
        text = str(text)
    
    # This dictionary covers most common special characters.
    conv = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\^{}', '\\': r'\textbackslash{}',
        '<': r'\textless{}', '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(key) for key in sorted(conv.keys(), key = len, reverse=True)))
    return regex.sub(lambda match: conv[match.group(0)], text)

def generate_pdf_from_json(data: Dict[str, Any], output_path: Path):
    """Generates a LaTeX PDF from the structured learning material JSON."""
    logger.info(f"Starting PDF generation for: {output_path}")

    # LaTeX Document Preamble
    latex_parts = [
        r"\documentclass[UTF8,a4paper,11pt]{ctexart}",
        r"\usepackage{geometry}",
        r"\geometry{a4paper, left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm}",
        r"\usepackage{amsmath, amssymb, amsfonts}",
        r"\usepackage{xcolor}",
        r"\usepackage{hyperref}",
        r"\usepackage{minted}", # For code highlighting
        r"\usepackage{fancyhdr}",
        r"\usepackage{titlesec}",
        r"\usepackage{enumitem}",
        
        r"\definecolor{TitleBlue}{RGB}{0, 82, 155}",
        r"\definecolor{SectionColor}{RGB}{60, 120, 180}",
        r"\definecolor{CodeBg}{RGB}{245, 245, 245}",

        r"\hypersetup{colorlinks=true, linkcolor=TitleBlue, urlcolor=cyan}",
        
        r"\titleformat{\section}{\Large\bfseries\color{SectionColor}}{\thesection}{1em}{}",
        r"\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}",

        r"\linespread{1.3}",
        r"\setminted{bgcolor=CodeBg, fontsize=\small, breaklines, autogobble}",

        r"\begin{document}",
    ]

    # Title and Objectives
    title = escape_latex(data.get("title", "Learning Module"))
    latex_parts.append(f"\\title{{\\bfseries\\Huge {title}}}")
    latex_parts.append(r"\author{Your AI Learning Coach}")
    latex_parts.append(r"\date{\today}")
    latex_parts.append(r"\maketitle")
    
    objectives = data.get("learning_objectives", [])
    if objectives:
        latex_parts.append(r"\begin{abstract}")
        latex_parts.append(r"\textbf{学习目标:}")
        latex_parts.append(r"\begin{itemize}[leftmargin=*]")
        for obj in objectives:
            latex_parts.append(f"\\item {escape_latex(obj)}")
        latex_parts.append(r"\end{itemize}")
        latex_parts.append(r"\end{abstract}")
        latex_parts.append(r"\clearpage")

    # Content Sections
    for i, section in enumerate(data.get("content_sections", [])):
        latex_parts.append(f"\\section{{{escape_latex(section.get('section_title', ''))}}}")
        latex_parts.append(escape_latex(section.get("explanation", "")))
        
        if section.get("visual_analogy"):
            latex_parts.append(r"\vspace{1em}\fcolorbox{gray}{gray!10}{\begin{minipage}{0.95\linewidth}\textbf{场景比喻:} " + escape_latex(section.get("visual_analogy")) + r"\end{minipage}}\vspace{1em}")

        if section.get("code_example"):
            # Assuming Python for now, can be made dynamic later
            code = section.get("code_example", "")
            latex_parts.append(r"\begin{minted}{python}")
            latex_parts.append(code)
            latex_parts.append(r"\end{minted}")

        if section.get("reflection_prompt"):
            latex_parts.append(r"\vspace{1em}\fcolorbox{TitleBlue}{blue!5}{\begin{minipage}{0.95\linewidth}\textbf{反思一下:} " + escape_latex(section.get("reflection_prompt")) + r"\end{minipage}}\vspace{1em}")
        
        latex_parts.append(r"\vspace{1em}")

    # Practice Exercises
    latex_parts.append(r"\clearpage")
    latex_parts.append(r"\section*{课后练习}")
    for i, exercise in enumerate(data.get("practice_exercises", [])):
        latex_parts.append(f"\\subsection*{{练习 {i+1}: {escape_latex(exercise.get('question_type', ''))}}}")
        latex_parts.append(escape_latex(exercise.get("question_text", "")))
        
        if exercise.get("question_type") == "multiple_choice":
            latex_parts.append(r"\begin{itemize}[label=\Alph*.]")
            for opt in exercise.get("options", []):
                latex_parts.append(f"\\item {escape_latex(opt)}")
            latex_parts.append(r"\end{itemize}")
            latex_parts.append(f"\\textbf{{答案:}} {escape_latex(exercise.get('answer'))}\n")
            latex_parts.append(f"\\textbf{{解析:}} {escape_latex(exercise.get('feedback'))}\n")
        
        elif exercise.get("question_type") == "coding_challenge":
            latex_parts.append(f"\\textbf{{预期输出或参考答案:}}\n {escape_latex(exercise.get('expected_output'))}")
        
        latex_parts.append(r"\vspace{2em}")

    # End of document
    latex_parts.append(r"\end{document}")
    
    full_latex_doc = "\n".join(latex_parts)
    
    # --- Compilation ---
    output_dir = output_path.parent
    base_filename = output_path.stem
    tex_filepath = output_dir / f"{base_filename}.tex"
    
    with open(tex_filepath, "w", encoding="utf-8") as f:
        f.write(full_latex_doc)
    logger.info(f"LaTeX source file generated: {tex_filepath}")

    # Check for xelatex
    if not shutil.which("xelatex"):
        logger.error("Command 'xelatex' not found. PDF generation skipped. Please install a LaTeX distribution like TeX Live or MiKTeX.")
        return

    # Compile the document (run twice for references, etc.)
    for i in range(2):
        logger.info(f"--- Running LaTeX compilation pass {i+1}/2 ---")
        try:
            # Use -shell-escape to allow minted to work
            process = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-shell-escape", tex_filepath.name],
                cwd=output_dir,
                capture_output=True, text=True, encoding='utf-8', errors='ignore'
            )
            if process.returncode != 0 and i == 1:
                logger.error(f"LaTeX compilation failed. Check log file: {output_dir / (base_filename + '.log')}")
                logger.error(f"STDOUT: {process.stdout}")
                logger.error(f"STDERR: {process.stderr}")
                return
        except Exception as e:
            logger.critical(f"A critical error occurred during LaTeX compilation: {e}")
            return
    
    if output_path.exists():
        logger.info(f"🎉 Successfully generated PDF: {output_path}")
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.out', '.tex', '.pygstyle', '.vrb', '.listing']:
            (output_dir / f"{base_filename}{ext}").unlink(missing_ok=True)
    else:
        logger.error("PDF generation failed. The PDF file was not created.")