"""
For example, consider the following navigation subsystem:

[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
Some of the lines aren't corrupted, just incomplete; you can ignore these lines for now. The remaining five lines are corrupted:

{([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
[[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
[{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
[<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
<{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.
Stop at the first incorrect closing character on each corrupted line.

Did you know that syntax checkers actually have contests to see who can get the high score for syntax errors in a file? It's true! To calculate the syntax error score for a line, take the first illegal character on the line and look it up in the following table:

): 3 points.
]: 57 points.
}: 1197 points.
>: 25137 points.
In the above example, an illegal ) was found twice (2*3 = 6 points), an illegal ] was found once (57 points), an illegal } was found once (1197 points), and an illegal > was found once (25137 points). So, the total syntax error score for this file is 6+57+1197+25137 = 26397 points!

Find the first illegal character in each corrupted line of the navigation subsystem. What is the total syntax error score for those errors?
"""

import numpy as np
import pandas as pd
import scipy

datafile = "Data/10_input.txt"
# datafile = "Data/10_input_test.txt"


openers = ('(', '[', '{', '<')
closers = (')', ']', '}', '>')
closer2opener = dict(zip(closers, openers))
opener2closer = dict(zip(openers, closers))
points = {')':3, ']':57, '}':1197, '>':25137}
print("Scoring rules:", points)
score = 0
# score_dict = dict.fromkeys(closers, 0)

with open(datafile, 'r') as file:
    for line_no, line in enumerate(file):
        # print(line.strip())
        stack = []
        corrupt_line = False
        for n,c in enumerate(line.strip()):
            if c in openers:
                stack.append(c)
            elif c in closers:
                corresponding_opener = closer2opener[c]
                if stack[-1] == corresponding_opener:
                    stack.pop()
                else:
                    corrupt_line = True
                    # score_dict[c] +=  points[c]
                    score += points[c]
                    break
            else:
                raise AssertionError(f"Illegal character encountered: {c}")
        if corrupt_line:
            print(f"{line.strip():30}. Expected {opener2closer[stack[-1]]}, but found {c} instead. Score = {score}")
        else:
            print(f"{line.strip():30}. Line OK! Score = {score}")


print(f"Final score = {score}")
