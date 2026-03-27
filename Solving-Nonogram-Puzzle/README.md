# Contents
- [Nonogram Puzzle: Introduction](#nonogram-puzzle-introduction)
- [How to use](#how-to-use)
- [Collaborators](#collaborators)
- [Files and Directories in the repository](#files-and-directories-in-the-repository)
# Nonogram Puzzle: Introduction
A game invented by 2 Japanese people, which goal is to recover the picture with information given at the side of the grid.<br>
For clear details: [Nonogram](https://en.wikipedia.org/wiki/Nonogram).<br>
We will try to solve a puzzle with size m x n (0 < m,n < 30). The puzzle can be unsolvable, has single answer or multiple answers.
![ducki](https://user-images.githubusercontent.com/91714479/209899429-a10d7dd2-3392-46fe-93b3-162e5ebcd8f5.png)
# How to use
Create a text file for the input called `input.txt`, the input includes:
- First line is the size of the test (mxn).
- Next m lines is the row information.
- Next n lines is the column information.

Download and run the file `run.py`.<br>
For example you can download file `input.txt` of us, then copy and paste the value from `datasets`.<br>
You can generate random tests and adjust the size by file `PuzzleGenerator.py`.
# Collaborators
We are K66 of Hanoi University of Science and Technology, major in Data Science and Artificial Intelligence. Under the guidance of our lecturer, Nguyen Nhat Quang, we work together on this problem.
- Phan Duc Hung
- Nguyen Viet Minh
- Pham Quang Trung
- Truong Gia Bach
# Files and directories in the repository
`read_input.py`: read the input from text file to collect information.<br>
`PuzzleGenerator.py`: generate random puzzle.<br>
`algorithms\ConstraintProgramming.py`: use Constraint Programming to solve.<br>
`algorithms\DFS(BackTracking).py`: use BackTracking to solve.<br>
`algorithms\LogicalBackTrack.py`: use Logical BackTrack to solve.<br>
`algorithms\SimulatedAnnealing.py`: use Simulated Annealing to solve.<br>
`datasets`: folder with available tests that we use to test all algorithms.<br>
`input.py`: input file, already filled for example.<br>
`input.txt`: the text file to collect input.<br>
`run.py`: solve the input
