\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{physlab}
\ProcessOptions

\LoadClass[12pt, a4paper, titlepage]{article}
\RequirePackage[T2A, T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[english, russian]{babel}

% Беспредел
\let\NOLIMITS\nolimits
\let\nolimits\limits
\let\displaylimits\limits
% Математика
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{bigints}
\RequirePackage{cancel}
\RequirePackage{mathrsfs}
\RequirePackage{iunits}
\RequirePackage{siunitx}

% Разметка
\RequirePackage [hcentering,
	bindingoffset = 10mm, 
	right = 15 mm, 
	left = 15 mm, 
	top=20mm, 
	bottom = 20 mm] {geometry}
\RequirePackage[unicode]{hyperref}
\setlength{\parskip}{0.5em}
\setlength{\parindent}{0em}
\renewcommand{\baselinestretch}{1.15}
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
\RequirePackage{titlesec}
\titlelabel{\thetitle.\quad}
\usepackage{multirow}
\newcommand\val{~\hspace{15mm}~}
\newcommand\valt{\hspace{9mm}}
\renewcommand\arraystretch{1.2}

% Графика
\RequirePackage{graphicx}
\RequirePackage{subcaption}
\graphicspath{{img/}}
\RequirePackage{color}
\RequirePackage{float}
\RequirePackage{wrapfig}
\newcommand{\tw}{\textwidth}
\newcommand{\lw}{\linewidth}
\newenvironment{bottompar}{\par\vspace*{\fill}}{\clearpage}
\newcommand\tline[2]{$\underset{\text{#1}}{\text{\underline{\hspace{#2}}}}$}


% Нумерация страниц
\RequirePackage{fancyref}
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyfoot[C]{\texttt{-~\thepage~-}}
%\fancyfoot[R]{\text{Трясогузов Павел, 653 гр}\tline{(подпись)}{20mm}}


% Для формул
\newcommand{\rskip}{\vspace{-1em}}
\newcommand{\aftermath}{\vspace{-2.1em}}
\newcommand{\const}{\text{const}}
\newcommand{\then}{\quad\Rightarrow\quad}
\newcommand{\ef}{\mathscr{E}}
\newcommand{\angstrom}{\textup{\AA}}
\newcommand{\RomanNumeralCaps}[1]
    {\MakeUppercase{\romannumeral #1}}