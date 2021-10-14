## optimal_stopping_dice

Draw a dice up to N-times, and optimally stop the trial intermediately to maximize the expectation of last value. Then take the statistics of how all possible trials would end.

```bash
($) python3 main.py 3

------------------------- stat -------------------------
#drawings   last_dice   #cases       prob
      1          5            1   0.16666666666666666
      1          6            1   0.16666666666666666
      2          4            4   0.1111111111111111
      2          5            4   0.1111111111111111
      2          6            4   0.1111111111111111
      3          1           12   0.05555555555555555
      3          2           12   0.05555555555555555
      3          3           12   0.05555555555555555
      3          4           12   0.05555555555555555
      3          5           12   0.05555555555555555
      3          6           12   0.05555555555555555

expectation of last_dice is 4.666666666666666
sum of prob = 1.0
```
