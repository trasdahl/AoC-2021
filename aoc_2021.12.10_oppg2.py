"""
Incomplete lines don't have any incorrect characters - instead, they're missing some closing characters at the end of the line. To repair the navigation subsystem, you just need to figure out the sequence of closing characters that complete all open chunks in the line.

You can only use closing characters (), ], }, or >), and you must add them in the correct order so that only legal pairs are formed and all chunks end up closed.

In the example above, there are five incomplete lines:

[({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})].
[(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
(((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))).
{<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
<{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>.
Did you know that autocomplete tools also have contests? It's true! The score is determined by considering the completion string character-by-character. Start with a total score of 0. Then, for each character, multiply the total score by 5 and then increase the total score by the point value given for the character in the following table:

): 1 point.
]: 2 points.
}: 3 points.
>: 4 points.
So, the last completion string above - ])}> - would be scored as follows:

Start with a total score of 0.
Multiply the total score by 5 to get 0, then add the value of ] (2) to get a new total score of 2.
Multiply the total score by 5 to get 10, then add the value of ) (1) to get a new total score of 11.
Multiply the total score by 5 to get 55, then add the value of } (3) to get a new total score of 58.
Multiply the total score by 5 to get 290, then add the value of > (4) to get a new total score of 294.
The five lines' completion strings have total scores as follows:

}}]])})] - 288957 total points.
)}>]}) - 5566 total points.
}}>}>)))) - 1480781 total points.
]]}}]}]}> - 995444 total points.
])}> - 294 total points.
Autocomplete tools are an odd bunch: the winner is found by sorting all of the scores and then taking the middle score. (There will always be an odd number of scores to consider.) In this example, the middle score is 288957 because there are the same number of scores smaller and larger than it.

Find the completion string for each incomplete line, score the completion strings, and sort the scores. What is the middle score?
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
corruption_points = {')':3, ']':57, '}':1197, '>':25137}
completion_points = {')':1, ']':2, '}':3, '>':4}
print("Scoring rules:", points)
# score_dict = dict.fromkeys(closers, 0)

score = 0
completion_scores = []
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
                    # score_dict[c] += corruption_points[c]
                    score += corruption_points[c]
                    break
            else:
                raise AssertionError(f"Illegal character encountered: {c}")
        if corrupt_line:
            print(f"{line.strip():30}. Expected {opener2closer[stack[-1]]}, but found {c} instead. Score = {score}")
        else:
            print(f"{line.strip():30}. Line OK! Score = {score}")
            # print(f"Stack: {stack}")
            completion_string = ''.join([opener2closer[c] for c in stack[::-1]])
            completion_score = 0
            for c in completion_string:
                completion_score = completion_score * 5 + completion_points[c]
            completion_scores.append(completion_score)
            print(f"Completion string: {completion_string} (completion score = {completion_score}")


print(f"Completion scores = {completion_scores}")
print(f"Median completion score: {int(np.median(completion_scores))}")

