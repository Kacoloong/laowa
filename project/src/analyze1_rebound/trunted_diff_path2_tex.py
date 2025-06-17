import os
from src.analyze1_rebound.ulity import flatten_state, left_rotate


def sol2tex(
    solution,
    cipher,
    rounds,
    begin_round,
    end_round,
    n_inbound,
    inbound_cover_round,
    count,
    current_dir,
):
    arrowlength = 2
    xgap = 0
    ygap = 5
    cipher_state_nr = cipher.cipher_state[0]
    cipher_state_nc = cipher.cipher_state[1]
    half_state_nr = int(cipher.cipher_state[0] / 2)
    half_state_nc = int(cipher.cipher_state[1] / 2)
    style_string=r"""
    \documentclass{standalone}
\ProvidesPackage{diffpath}
\usepackage[usenames,svgnames,dvipsnames]{xcolor}
\usepackage{tikz}
\usepackage{calc}
\usepackage{ifthen}
\usetikzlibrary{arrows}
\usepackage[T1]{fontenc}
\usepackage{courier}

\definecolor{light-gray}{gray}{0.7}
\definecolor{darkgreen}{rgb}{0,0.4,0}

\def\stateSize{8}%default size is 8
\def\stateWidth{\stateSize}%default is a square state
\def\arrowLength{2}
\def\xGap{2}
\def\yGap{4}
\def\stateIndexing{1}
\def\linkRound{0}
\def\blackAndWhite{0}
\def\linkWithPreviousState{0}

\def\currentFeedForward{0}

\newcommand\defineStateSize[1]{%
  \def\stateSize{#1}
}

\newcommand\defineStateWidth[1]{%
  \def\stateWidth{#1}
}

\newcommand\defineArrowLength[1]{%
  \def\arrowLength{#1}
}

\newcommand\defineXGap[1]{%
  \def\xGap{#1}
}

\newcommand\defineYGap[1]{%
  \def\yGap{#1}
}

\newcommand\defineTextSize[1]{%
  \def\textSize{#1}
}

\newcommand\defineTextStateSize[1]{%
  \def\textStateSize{#1}
}

\newcommand\defineTextArrowSize[1]{%
  \def\textArrowSize{#1}
}

\newcommand\defineStateIndex[1]{%
  \def\stateIndexing{#1}
  \setcounter{statecnt}{0}
}

\newcommand\defineStartIndex[1]{%
  \setcounter{statecnt}{#1}
}

\newcommand\defineLinkRound[1]{%
  \def\linkRound{#1}
}


\newcommand\defineblackAndWhite[1]{%
  \def\blackAndWhite{#1}
}

\newcommand\initdiffpath{%
  \setcounter{shiftx}{0}
  \setcounter{maxshiftx}{0}
  \setcounter{shifty}{0}
  \setcounter{prevshiftx}{0}
  \setcounter{prevshifty}{0}
  \setcounter{posx}{0}
  \setcounter{posy}{\stateSize-1}
  \setcounter{statecnt}{0}
  %\setcounter{statecnt}{0}
  %\ifthenelse{\NOT\equal{\value{statecnt}}{0}}
}


%%%%%%%%%%%% Available colors are:
% B black
% y yellow
% r red
% b blue
% G green
% g gray
% c cyan
% p purple
% P pink
% o orange
% l light gray
% m magenta


%% Define some counters
\newcounter{shiftx}\setcounter{shiftx}{0}
\newcounter{shiftxTmp}\setcounter{shiftxTmp}{0}
\newcounter{shifty}\setcounter{shifty}{0}
\newcounter{shiftyTmp}\setcounter{shiftyTmp}{0}
\newcounter{maxshiftx}\setcounter{maxshiftx}{0}
\newcounter{prevshiftx}\setcounter{prevshiftx}{0}
\newcounter{prevshifty}\setcounter{prevshifty}{0}
\newcounter{posx}\setcounter{posx}{0}
\newcounter{posy}\setcounter{posy}{\stateSize-1}
\newcounter{statecnt}\setcounter{statecnt}{0}
\newcounter{newline}\setcounter{newline}{0}
\newcommand{\SBSR}{SB-SR}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% DRAW THE STATE
%%
\newcommand*\state[1]{%{nextTransition}
  %% Reset newline to 0
  \ifthenelse{\equal{\value{newline}}{1}}{\setcounter{newline}{0}}{}

  %% If the user want a dashed link to the next line
  \ifthenelse{	\(
    \equal{\linkRound}{1}
    \AND
    \equal{\linkWithPreviousState}{1}
    \AND
    \value{statecnt}>0
    \AND
    \NOT\equal{\currentFeedForward}{1}
    \)
  } {%
    \def\linkWithPreviousState{0}
    \draw[shift={(\value{maxshiftx},\value{prevshifty})}][][->] 
    ++(\stateWidth,\stateSize/2) 
    -- +(2,0)
    -- +(2,-\stateSize/2-\yGap/2)
    -- (-2-\value{maxshiftx},0-\yGap/2)
    -- (-2-\value{maxshiftx},0-\stateSize/2-\yGap)
    -- (0-\value{maxshiftx},0-\stateSize/2-\yGap);
  }{}

  \ifthenelse{\equal{#1}{0}} {%
    \setcounter{newline}{1}
    \def\linkWithPreviousState{1}
  }



  %% \foreach \x in {0,4,8,12} { 
  %%   \foreach \y in {0,4,8,12} { 
  %%     \draw[shift={(\value{shiftx},\value{shifty})},line width=1pt] 
  %%     ++(\x,\y) rectangle +(4,4);
  %%   }
  %% }
  

  \foreach \x in {0,...,{\numexpr \stateWidth-1}} { 
    \foreach \y in {0,...,{\numexpr \stateSize-1}} { 
      \draw[shift={(\value{shiftx},\value{shifty})}, line width=1pt] 
      ++(\x,\y) rectangle +(1,1);
    }
  }
  
  %% Add State Number when needed/wanted
  \ifthenelse{ \(
    \equal{\stateIndexing}{0} 
    \OR 
    \equal{\value{statecnt}}{-1} \)
  } {}{%
    \node[black,above] 
    at +(\value{shiftx}+\stateWidth/2,\value{shifty}+\stateSize+1) 
    {\fontsize{\textStateSize}{\textStateSize}\tt S\arabic{statecnt}};
  }	
  
  %% Add a transition with name if needed
  \ifthenelse{\equal{#1}{0}} {%
    \setcounter{prevshifty}{\value{shifty}}
    \setcounter{prevshiftx}{\value{shiftx}}
    \addtocounter{shifty}{-\stateSize}
    \addtocounter{shifty}{-\yGap}
    \setcounter{maxshiftx}{\value{shiftx}}
    \setcounter{shiftx}{-\stateWidth-\arrowLength-\xGap-\xGap}
  } {
    \ifthenelse{\equal{\arrowLength}{0}}{}{
     \ifthenelse{\equal{#1}{\SBSR}} {%
      \draw[shift={(\value{shiftx},\value{shifty})}] [->] 
      ++({\stateWidth +\xGap},{\stateSize/2}) 
      -- node[above] {\fontsize{\textArrowSize}{\textArrowSize}\tt SB} node[below] {\fontsize{\textArrowSize}{\textArrowSize}\tt SR}
	    +(\arrowLength,0);
     
     }{    
      \draw[shift={(\value{shiftx},\value{shifty})}] [->] 
      ++({\stateWidth +\xGap},{\stateSize/2}) 
      -- node[below] {\fontsize{\textArrowSize}{\textArrowSize}\tt #1} 
      	+(\arrowLength,0);
      }
    }
  }
  \ifthenelse{\equal{#1}{0}} {} {\addtocounter{statecnt}{1}}
  \addtocounter{shiftx}{\stateWidth}
  \addtocounter{shiftx}{\arrowLength}
  \addtocounter{shiftx}{\xGap}
  \addtocounter{shiftx}{\xGap}
}



\newcommand*\statee[2]{%{nextTransition}
  %% Reset newline to 0
  \ifthenelse{\equal{\value{newline}}{1}}{\setcounter{newline}{0}}{}

  %% If the user want a dashed link to the next line
  \ifthenelse{	\(
    \equal{\linkRound}{1}
    \AND
    \equal{\linkWithPreviousState}{1}
    \AND
    \value{statecnt}>0
    \AND
    \NOT\equal{\currentFeedForward}{1}
    \)
  } {%
    \def\linkWithPreviousState{0}
    \draw[shift={(\value{maxshiftx},\value{prevshifty})}][dashed][->] 
    ++(\stateWidth,\stateSize/2) 
    -- +(2,0)
    -- +(2,-\stateSize/2-\yGap/2)
    -- (-2-\value{maxshiftx},0-\yGap/2)
    -- (-2-\value{maxshiftx},0-\stateSize/2-\yGap)
    -- (0-\value{maxshiftx},0-\stateSize/2-\yGap);
  }{}

  \ifthenelse{\equal{#1}{0}} {%
    \setcounter{newline}{1}
    \def\linkWithPreviousState{1}
  }



  %% \foreach \x in {0,4,8,12} { 
  %%   \foreach \y in {0,4,8,12} { 
  %%     \draw[shift={(\value{shiftx},\value{shifty})},line width=1pt] 
  %%     ++(\x,\y) rectangle +(4,4);
  %%   }
  %% }
  

  \foreach \x in {0,...,{\numexpr \stateWidth-1}} { 
    \foreach \y in {0,...,{\numexpr \stateSize-1}} { 
      \draw[shift={(\value{shiftx},\value{shifty})}] 
      ++(\x,\y) rectangle +(1,1);
    }
  }
  
  %% Add State Number when needed/wanted
  \ifthenelse{ \(
    \equal{\stateIndexing}{0} 
    \OR 
    \equal{\value{statecnt}}{-1} \)
  } {}{%
    \node[black,above] 
    at +(\value{shiftx}+\stateWidth/2,\value{shifty}+\stateSize+1) 
    {\fontsize{\textStateSize}{\textStateSize}\tt S\arabic{statecnt}};
  }	
  
  %% Add a transition with name if needed
  \ifthenelse{\equal{#1}{0}} {%
    \setcounter{prevshifty}{\value{shifty}}
    \setcounter{prevshiftx}{\value{shiftx}}
    \addtocounter{shifty}{-\stateSize}
    \addtocounter{shifty}{-\yGap}
    \setcounter{maxshiftx}{\value{shiftx}}
    \setcounter{shiftx}{-\stateWidth-\arrowLength-\xGap-\xGap}
  } {
    \ifthenelse{\equal{\arrowLength}{0}}{}{
     \ifthenelse{\equal{#1}{\SBSR}} {%
      \draw[shift={(\value{shiftx},\value{shifty})}] [->] 
      ++({\stateWidth +\xGap},{\stateSize/2}) 
      -- node[above] {\fontsize{\textArrowSize}{\textArrowSize}\sf SB} node[below] {\fontsize{\textArrowSize}{\textArrowSize}\sf SR}
	    +(\arrowLength,0);
     
     }{    
      \draw[shift={(\value{shiftx},\value{shifty})}] [->] 
      ++({\stateWidth +\xGap},{\stateSize/2}) 
      -- node[above] {\fontsize{\textArrowSize}{\textArrowSize}\sf #1} 
    	     node[below] {\fontsize{\textArrowSize}{\textArrowSize}\sf #2} 
      	+(\arrowLength,0);
      }
    }
  }
  \ifthenelse{\equal{#1}{0}} {} {\addtocounter{statecnt}{1}}
  \addtocounter{shiftx}{\stateWidth}
  \addtocounter{shiftx}{\arrowLength}
  \addtocounter{shiftx}{\xGap}
  \addtocounter{shiftx}{\xGap}
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%% DRAW THE STATE ON THE SUBKEY
%%
\newcommand*\stateAK{%{nextTransition}

  \foreach \x in {0,...,{\numexpr \stateWidth-1}} { 
    \foreach \y in {0,...,{\numexpr \stateSize-1}} { 
      \draw[shift={(\value{shiftx}-4,\value{shifty}+5)}] 
      ++(\x,\y) rectangle +(1,1);
    }
  }
  \draw[shift={(\value{shiftx}-2,\value{shifty}+5)}] (0,0) -- (0,-3);
  \draw[shift={(\value{shiftx}-2,\value{shifty}+5-3)}] circle (0.3);
 
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% ARROW BETWEEN STATES
%%
\newcommand\stateArrowAbove[2]{

  \setcounter{shiftxTmp}{\value{shiftx}}
  \setcounter{shiftyTmp}{\value{shifty}}
  #1;
  \ifthenelse{\equal{\value{newline}}{1}}{
    \draw[shift={(\value{shiftxTmp},\value{shiftyTmp})}] 
         [->] ++(\stateWidth/2,\stateSize+2) 
         -- node[above] {\fontsize{1.2cm}{1.4cm}\tt #2} 
         +(\value{prevshiftx}-\stateWidth-\arrowLength,0);
  }{
    \draw[shift={(\value{shiftxTmp},\value{shiftyTmp})}] 
         [->] ++(\stateWidth/2,\stateSize+1) 
         -- node[above] {\fontsize{1.2cm}{1.4cm}\tt #2} 
         +(\value{shiftx}-\stateWidth-\arrowLength-2*\xGap,0);
  }
}

\newcommand\stateArrowBelow[2]{

  \setcounter{shiftxTmp}{\value{shiftx}}
  \setcounter{shiftyTmp}{\value{shifty}}
  #1;
  \ifthenelse{\equal{\value{newline}}{1}}{
    \draw[shift={(\value{shiftxTmp},\value{shiftyTmp})}] 
         [->] ++(\stateWidth/2,-1) 
         -- node[below] {\fontsize{1.2cm}{1.4cm}\tt #2} 
         +(\value{prevshiftx}-\stateWidth-\arrowLength,0);
  }{
    \draw[shift={(\value{shiftxTmp},\value{shiftyTmp})}] 
         [->] ++(\stateWidth/2,-1) 
         -- node[below] {\fontsize{1.2cm}{1.4cm}\tt #2} 
         +(\value{shiftx}-\stateWidth-\arrowLength,0);

  }
}

\newcommand\defaultfeedforward{%
  \addtocounter{statecnt}{1}
  \def\currentFeedForward{1}
  %\node[circle,draw,inner sep=25pt] (xor)
  \node[XOR,scale=3] (xor)
  at (-2-\yGap/2,\value{shifty}+\stateSize+\yGap/2) {$\oplus$};
  \draw[dashed] [->] 
  ++(0,\stateSize/2) 
  -- +(-2-\yGap/2,0)
  -- +(xor);
  \draw[dashed] [->] 
  ++(\value{maxshiftx}+\stateSize/2,\value{shifty}+\stateSize+\yGap)
  -- +(0, 0-\yGap/2)
  -- (xor);
  \draw[dashed] [->] 
  ++(xor)
  -- ++(0,0-\yGap/2-\stateSize/2)
  -- +(2+\yGap/2, 0);
}

\newcommand\feedforward[1]{%
  \defaultfeedforward
  \colorstate{#1}
}

\newcommand\colorfeedforward[2]{%
  \defaultfeedforward
  \colorstate{#1}{#2}
}


\newcommand*\round{%
  \state{SR} % ShiftRows
  \state{SB} % SubBytes
  \state{MC} % MixColumns
  \state{SB} % SubBytes
  \state{SR} % ShiftRows
  \state{BSR} % BigShiftRows
  \state{MC} % MixColumns
  \state{BMC} % BigMixColumns
  \state{0} % 
}

\def\hyphenateWholeString#1{\xHyphenate#1$\wholeString\unskip}

\def\xHyphenate#1#2\wholeString {
  \if#1$%
  \else\transform{#1}%
  \takeTheRest#2\ofTheString\fi
}

\def\takeTheRest#1\ofTheString\fi{\fi \xHyphenate#1\wholeString}

\def\transform#1{
  \ifthenelse{\equal{#1}{.}}{}{%
    \addColor{#1}
  }
  \addtocounter{posx}{1}
  \ifthenelse{\equal{\value{posx}}{\stateWidth}}{%
    \setcounter{posx}{0}
    \addtocounter{posy}{-1}
  }{}%
}

\def\addColor#1{
  \ifthenelse{\equal{\blackAndWhite}{0}}{
    \ifthenelse{\equal{#1}{B}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=black]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{y}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=yellow]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{r}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=red]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{b}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=blue]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{G}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=green]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{g}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=gray]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{l}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=light-gray]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{c}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=cyan]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{p}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=purple]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{P}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=pink]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{m}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=magenta]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{M}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=Sepia!80]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{o}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=orange]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{\ifthenelse{\equal{#1}{.}}{}{%
       \draw[shift={(\value{shiftx},\value{shifty})}]
       (0.5+\value{posx},0.5+\value{posy}) 
       node {\fontsize{\textSize}{\textSize}\tt #1};
    }}
    }}}}}}}}}}}}
  }{
    %% Black AND White ONLY
    \ifthenelse{\equal{#1}{B}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=black]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{y}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt Y};
    }{
    \ifthenelse{\equal{#1}{r}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt $\blacksquare$};
    }{
    \ifthenelse{\equal{#1}{b}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt $\newmoon$};
    }{
    \ifthenelse{\equal{#1}{G}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt $\bigstar$};
    }{
    \ifthenelse{\equal{#1}{g}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=gray]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{l}}{%
      \fill[shift={(\value{shiftx},\value{shifty})}] [color=light-gray]
      (\value{posx},\value{posy}) rectangle +(1,1);
    }{
    \ifthenelse{\equal{#1}{c}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt $\checkmark$};
    }{
    \ifthenelse{\equal{#1}{p}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt P};
    }{
    \ifthenelse{\equal{#1}{m}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt M};
    }{
    \ifthenelse{\equal{#1}{P}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt I};
    }{
    \ifthenelse{\equal{#1}{o}}{%
      \draw[shift={(\value{shiftx},\value{shifty})}]
      (0.5+\value{posx},0.5+\value{posy}) 
      node {\fontsize{\textSize}{\textSize}\tt O};
    }{\ifthenelse{\equal{#1}{.}}{}{%
       \draw[shift={(\value{shiftx},\value{shifty})}]
       (0.5+\value{posx},0.5+\value{posy}) 
       node {\fontsize{\textSize}{\textSize}\tt #1};
    }}
    }}}}}}}}}}}
    
    
  }
}

\newcommand*\colorstate[2]{%{colors}{nextTransition}
  \setcounter{posx}{0}
  \setcounter{posy}{\stateSize-1}
  \hyphenateWholeString{#1}
  \state{#2}
}

\newcommand*\colorstatee[3]{%{colors}{nextTransition}
  \setcounter{posx}{0}
  \setcounter{posy}{\stateSize-1}
  \hyphenateWholeString{#1}
  \statee{#2}{#3}
}


\newcommand*\colorstateAK[4]{%{colors}{nextTransition}
  \colorstate{#1}{#3}

  \addtocounter{shiftx}{-4}
  %\arrowLength-(\arrowLength-\stateWidth)/2
  
  \addtocounter{shifty}{+5}
  \setcounter{posy}{\stateSize-1}
  \hyphenateWholeString{#2}
  
  \addtocounter{shiftx}{+4}
	%(\arrowLength-\stateWidth)/2-\arrowLength
  \addtocounter{shifty}{-5}
  
  \stateAK
  \ifthenelse{\equal{#4}{0}} {%
  }{
    \draw[shift={(\value{shiftx}-4,\value{shifty}+5)}, ->] 
    (4,2) -- node[above] {\fontsize{\textArrowSize}{\textArrowSize}\tt KS}
    +(3*\stateSize+2*\arrowLength,0);
  }
}

    """
    result_string = style_string+rf"""
    \begin{{document}}
    \begin{{tikzpicture}}[scale=0.3]

      \defineStateSize{{{cipher_state_nc}}}
      \defineArrowLength{{{arrowlength}}}
      \defineTextSize{{0.8cm}}
      \defineTextArrowSize{{0.5cm}}
      \defineXGap{{{xgap}}}
      \defineYGap{{{ygap}}}
      \defineStateIndex{{0}}
      \defineLinkRound{{1}}
      \initdiffpath
      """
    # print(solution)
    # dash=f"\\draw[thick, dashed,blue] (-1,{5-9*(end_round+1)+2}) -- (-1,{5-9*(begin_round)+1}) -- (11,{5-9*(begin_round)+1}) -- (11,{5-9*(begin_round-1)+1}) -- (23,{5-9*(begin_round-1)+1}) -- (23,{5-9*(end_round+1)+2}) --(-1,{5-9*(end_round+1)+2});\n"
    # dash=f"\\draw[thick, dashed,blue] (-1,{5-9*(end_round)+1}) -- (-1,{5-9*(begin_round)+1});\n"
    ### 圈出Inbound阶段
    color = ["blue", "red", "orange"]
    draw_inbound = []
    for n in range(n_inbound):
        begin = begin_round - 1
        if n != 0:
            begin += sum(inbound_cover_round[:n])
        end = sum(inbound_cover_round[: n + 1]) + begin_round - 1
        lower_left_node = (
            f"({cipher_state_nc + 1}, {-(cipher_state_nc+ygap) * end - 1})"
        )
        upper_left_node = f"({cipher_state_nc+1},{-(cipher_state_nc+ygap)*begin-3})"
        mid_lower_node = f"({cipher_state_nc+1+2*(cipher_state_nc+arrowlength)},{-(cipher_state_nc+ygap)*begin-3})"
        mid_upper_node = f"({cipher_state_nc+1+2*(cipher_state_nc+arrowlength)},{-(cipher_state_nc+ygap)*begin+cipher_state_nc+2})"
        upper_right_node = f"({cipher_state_nc+1+4*(cipher_state_nc+arrowlength)},{-(cipher_state_nc+ygap)*begin+cipher_state_nc+2})"
        lower_right_node = f"({cipher_state_nc+1+4*(cipher_state_nc+arrowlength)},{-(cipher_state_nc+ygap) * end - 1})"
        draw = f"\\draw[thick,dashed,{color[n]}] {lower_left_node} -- {upper_left_node} -- {mid_lower_node} -- {mid_upper_node} -- {upper_right_node} -- {lower_right_node} -- {lower_left_node};\n"
        node = f"\\node [{color[n]}] at ({cipher_state_nc+1+4*(cipher_state_nc+arrowlength)+4},{-(cipher_state_nc+ygap)*begin-3}) {{Inbound {n}}};\n"
        draw_inbound.append(draw)
        draw_inbound.append(node)
    result_string += "".join(draw_inbound)

    after_shift_matrix = []
    state_matrix = [
        [cipher_state_nr * i + j for j in range(cipher_state_nc)]
        for i in range(cipher_state_nr)
    ]
    # print("cipher_mc_mr:", cipher.cipher_mc_mr)
    if cipher.cipher_mc_mr == 0:
        transposed_matrix = list(zip(*state_matrix))
        # 对转置后的每一行应用循环左移
        rotated_rows = [
            left_rotate(row, shift)
            for row, shift in zip(transposed_matrix, cipher.cipher_shift)
        ]
        # 再次转置以恢复原始的行列方向
        after_shift_matrix = list(zip(*rotated_rows))
    else:
        for i in range(cipher_state_nc):
            after_shift_matrix.append(
                left_rotate(state_matrix[i], cipher.cipher_shift[i])
            )
    # index_sr = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    index_sr = flatten_state(after_shift_matrix)
    # print(len(solution))
    for k in range(len(solution) - 1):
        matrix_begin = [
            [solution[k][j * cipher_state_nc + i] for j in range(cipher_state_nr)]
            for i in range(cipher_state_nc)
        ]
        # print(matrix_begin)
        matrix_end = [
            [solution[k + 1][j * cipher_state_nc + i] for j in range(cipher_state_nr)]
            for i in range(cipher_state_nc)
        ]
        after_sr = []
        for j in range(cipher_state_nc * cipher_state_nr):
            after_sr.append(solution[k][index_sr[j]])
        matrix_begin_sr = [
            [after_sr[j * cipher_state_nc + i] for j in range(cipher_state_nr)]
            for i in range(cipher_state_nc)
        ]

        converted_matrix_begin = [
            ["g" if item == 1 else "." for item in row] for row in matrix_begin
        ]
        # print(converted_matrix_begin)
        converted_matrix_end = [
            ["g" if item == 1 else "." for item in row] for row in matrix_end
        ]
        converted_matrix_sr = [
            ["g" if item == 1 else "." for item in row] for row in matrix_begin_sr
        ]

        if k == 0:
            result_string += "\\colorstate{\n"
            for row in range(cipher_state_nr):
                result_string += "." * cipher_state_nc + "\n"
            result_string += "  }{AK}\n"
            result_string += (
                f"\\path ({half_state_nc},{cipher_state_nc+1-(cipher_state_nc+ygap)*k}) node[scale=2]"
                + " {$rc_{"
                + str(k)
                + "}$};"
            )
        else:
            result_string += "\\colorstate{\n"
            for row in range(cipher_state_nr):
                result_string += "." * cipher_state_nc + "\n"
            result_string += "  }{AK}\n"
            result_string += (
                f"\\path ({half_state_nc},{cipher_state_nc+1-(cipher_state_nc+ygap)*k}) node[scale=2]"
                + " {$rc_{"
                + str(k)
                + "}$};"
            )

        result_string += "\\colorstate{\n"
        for row in converted_matrix_begin:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{SB}\n"
        result_string += (
            f"\\path ({half_state_nc+cipher_state_nc+arrowlength},{cipher_state_nc+1-(cipher_state_nc+ygap)*k}) node[scale=2]"
            + " {$x_{"
            + str(k)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in converted_matrix_begin:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{SR}\n"
        result_string += (
            f"\\path ({half_state_nc+2*(cipher_state_nc+arrowlength)},{cipher_state_nc+1-(cipher_state_nc+ygap)*k}) node[scale=2]"
            + " {$y_{"
            + str(k)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in converted_matrix_sr:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{MC}\n"
        result_string += (
            f"\\path ({half_state_nc+3*(cipher_state_nc+arrowlength)},{cipher_state_nc+1-(cipher_state_nc+ygap)*k}) node[scale=2]"
            + " {$z_{"
            + str(k)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in converted_matrix_end:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{0}\n"
        result_string += (
            f"\\path ({half_state_nc+4*(cipher_state_nc+arrowlength)},{cipher_state_nc+1-(cipher_state_nc+ygap)*k}) node[scale=2]"
            + " {$w_{"
            + str(k)
            + "}$};"
        )
    if cipher.cipher_last_mix:
        pass
    else:
        ## 生成最后一轮的图，没有MC操作
        end = [
            [solution[-1][j * cipher_state_nc + i] for j in range(cipher_state_nr)]
            for i in range(cipher_state_nc)
        ]
        converted_end = [["g" if item == 1 else "." for item in row] for row in end]

        end_sr = []
        for j in range(cipher_state_nc * cipher_state_nr):
            end_sr.append(solution[-1][index_sr[j]])
        end_sr_matrix = [
            [end_sr[j * cipher_state_nc + i] for j in range(cipher_state_nr)]
            for i in range(cipher_state_nc)
        ]
        converted_end_sr_matrix = [
            ["g" if item == 1 else "." for item in row] for row in end_sr_matrix
        ]

        result_string += "\\colorstate{\n"
        for row in range(cipher_state_nr):
            result_string += "." * cipher_state_nc + "\n"
        result_string += "  }{AK}\n"
        result_string += (
            f"\\path ({half_state_nc},{cipher_state_nc+1-(cipher_state_nc+ygap)*(rounds-1)}) node[scale=2]"
            + " {$rc_{"
            + str(rounds - 1)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in converted_end:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{SB}\n"
        result_string += (
            f"\\path ({half_state_nc+cipher_state_nc+arrowlength},{cipher_state_nc+1-(cipher_state_nc+ygap)*(rounds-1)}) node[scale=2]"
            + " {$x_{"
            + str(rounds - 1)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in converted_end:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{SR}\n"
        result_string += (
            f"\\path ({half_state_nc+2*(cipher_state_nc+arrowlength)},{cipher_state_nc+1-(cipher_state_nc+ygap)*(rounds-1)}) node[scale=2]"
            + " {$y_{"
            + str(rounds - 1)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in converted_end_sr_matrix:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{0}\n"
        result_string += (
            f"\\path ({half_state_nc+3*(cipher_state_nc+arrowlength)},{cipher_state_nc+1-(cipher_state_nc+ygap)*(rounds-1)}) node[scale=2]"
            + " {$z_{"
            + str(rounds - 1)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in range(cipher_state_nr):
            result_string += "." * cipher_state_nc + "\n"
        result_string += "  }{AK}\n"
        result_string += (
            f"\\path ({half_state_nc},{cipher_state_nc+1-(cipher_state_nc+ygap)*rounds}) node[scale=2]"
            + " {$rc_{"
            + str(rounds)
            + "}$};"
        )

        result_string += "\\colorstate{\n"
        for row in converted_end_sr_matrix:
            result_string += "    " + "".join(row) + "\n"
        result_string += "  }{0}\n"
        result_string += (
            f"\\path ({half_state_nc+(cipher_state_nc+arrowlength)},{cipher_state_nc+1-(cipher_state_nc+ygap)*rounds}) node[scale=2]"
            + " {$x_{"
            + str(rounds)
            + "}$};"
        )

    result_string += "\end{tikzpicture}\n\end{document}"

    folder_path = f"Rebound_trail_latex/Round_{rounds}/Inbound_{begin_round}_{end_round}_count_{count}"
    filename = f"main.tex"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # self.__model.write(f"{folder_path}/{filename}")
    with open(f"{folder_path}/{filename}", "w+") as file:
        file.write(result_string)
    # print(result_string)
    return folder_path


def sols2tex(
    solution,
    cipher,
    rounds,
    begin_round,
    end_round,
    n_inbound,
    inbound_cover_round,
    current_dir,
    sol_num,
):
    folder_paths = []
    for i in range(sol_num):
        path = sol2tex(
            solution[i],
            cipher,
            rounds,
            begin_round,
            end_round,
            n_inbound,
            inbound_cover_round,
            i + 1,
            current_dir,
        )
        folder_paths.append(path)
    return folder_paths
    # result_string = rf"""\documentclass{{standalone}}
    # \usepackage{{{current_dir}/tex_file/diffpath}}        % Custom LaTeX package to draw AES-like rounds
    # \begin{{document}}
    # \begin{{tikzpicture}}[scale=0.3]

    #   \defineStateSize{{4}}
    #   \defineArrowLength{{2}}
    #   \defineTextSize{{0.4cm}}
    #   \defineTextArrowSize{{0.3cm}}
    #   \defineXGap{{0}}
    #   \defineYGap{{5}}
    #   \defineStateIndex{{0}}
    #   \defineLinkRound{{1}}
    #   \initdiffpath
    #   """
    # # print(solution)
    # ## 生成除了最后一轮的图
    # index_sr = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    # for k in range(len(solution) - 1):
    #     matrix_begin = [[solution[k][j * 4 + i] for j in range(4)] for i in range(4)]
    #     # print(matrix_begin)
    #     matrix_end = [[solution[k + 1][j * 4 + i] for j in range(4)] for i in range(4)]
    #     after_sr = []
    #     for j in range(16):
    #         after_sr.append(solution[k][index_sr[j]])
    #     matrix_begin_sr = [[after_sr[j * 4 + i] for j in range(4)] for i in range(4)]

    #     converted_matrix_begin = [
    #         ["g" if item == 1 else "." for item in row] for row in matrix_begin
    #     ]
    #     # print(converted_matrix_begin)
    #     converted_matrix_end = [
    #         ["g" if item == 1 else "." for item in row] for row in matrix_end
    #     ]
    #     converted_matrix_sr = [
    #         ["g" if item == 1 else "." for item in row] for row in matrix_begin_sr
    #     ]

    #     result_string += "\\colorstate{\n"
    #     for row in converted_matrix_begin:
    #         result_string += "    " + "".join(row) + "\n"
    #     result_string += "  }{SB}\n"
    #     result_string += f"\\path ({2},{5-9*k}) node" + " {$x_{" + str(k) + "}$};"

    #     result_string += "\\colorstate{\n"
    #     for row in converted_matrix_begin:
    #         result_string += "    " + "".join(row) + "\n"
    #     result_string += "  }{SR}\n"
    #     result_string += f"\\path ({8},{5-9*k}) node" + " {$y_{" + str(k) + "}$};"

    #     result_string += "\\colorstate{\n"
    #     for row in converted_matrix_sr:
    #         result_string += "    " + "".join(row) + "\n"
    #     result_string += "  }{MC}\n"
    #     result_string += f"\\path ({14},{5-9*k}) node" + " {$z_{" + str(k) + "}$};"

    #     result_string += "\\colorstate{\n"
    #     for row in converted_matrix_end:
    #         result_string += "    " + "".join(row) + "\n"
    #     result_string += "  }{0}\n"
    #     result_string += f"\\path ({20},{5-9*k}) node" + " {$w_{" + str(k) + "}$};"

    # ## 生成最后一轮的图，没有MC操作
    # end = [[solution[-1][j * 4 + i] for j in range(4)] for i in range(4)]
    # converted_end = [["g" if item == 1 else "." for item in row] for row in end]

    # end_sr = []
    # for j in range(16):
    #     end_sr.append(solution[-1][index_sr[j]])
    # end_sr_matrix = [[end_sr[j * 4 + i] for j in range(4)] for i in range(4)]
    # converted_end_sr_matrix = [
    #     ["g" if item == 1 else "." for item in row] for row in end_sr_matrix
    # ]

    # result_string += "\\colorstate{\n"
    # for row in converted_end:
    #     result_string += "    " + "".join(row) + "\n"
    # result_string += "  }{SB}\n"
    # result_string += (
    #     f"\\path ({2},{5-9*(rounds-1)}) node" + " {$x_{" + str(rounds - 1) + "}$};"
    # )

    # result_string += "\\colorstate{\n"
    # for row in converted_end:
    #     result_string += "    " + "".join(row) + "\n"
    # result_string += "  }{SR}\n"
    # result_string += (
    #     f"\\path ({8},{5-9*(rounds-1)}) node" + " {$y_{" + str(rounds - 1) + "}$};"
    # )

    # result_string += "\\colorstate{\n"
    # for row in converted_end_sr_matrix:
    #     result_string += "    " + "".join(row) + "\n"
    # result_string += "  }{0}\n"
    # result_string += (
    #     f"\\path ({14},{5-9*(rounds-1)}) node" + " {$z_{" + str(rounds - 1) + "}$};"
    # )

    # result_string += "\\colorstate{\n"
    # for row in converted_end_sr_matrix:
    #     result_string += "    " + "".join(row) + "\n"
    # result_string += "  }{0}\n"
    # result_string += f"\\path ({2},{5-9*rounds}) node" + " {$x_{" + str(rounds) + "}$};"

    # result_string += "\end{tikzpicture}\n\end{document}"

    # folder_path = f"AES_rebound_trail_latex/Multi_sol_AES{128}_round_{rounds}"
    # filename = f"sol_{sol_num}.tex"
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)
    # # self.__model.write(f"{folder_path}/{filename}")
    # with open(f"{folder_path}/{filename}", "w+") as file:
    #     file.write(result_string)
    # print(result_string)
