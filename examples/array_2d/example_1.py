"""Create a randomized 2-D array (10 rows x 5 columns) and visualize it."""

from leetpy import Array2D

root = Array2D.create(rows=10, cols=5)  # create a random 2-D array
Array2D.print(root)  # visualize the array

"""
(random) Output:
  │      0           1           2           3           4     
──┼────────────────────────────────────────────────────────────
0 │ -461582327  1290777198   547320440  -1507301247  -56374412
1 │  302376901  -985335389  1326487483   -45064970   829201975
2 │ -1861798780 -964151733  -729317109  -1759444319 1078726806
3 │ 1635824683  1799492614   739458816  1381044606   -12855012
4 │ -459650970   -60571857   -61165952  -149561582  -495478061
5 │ -1383695716  899197731  -264108884   702319358   211280366
6 │ -807529251   -94234227  1661399497   754980611   920879385
7 │ -1545530628  725882430   590886674  -1477165950 -1085676070
8 │ 1142606987  -1289809918 -1472859112 -1263244779 -1556336881
9 │ -1995582807 -485137082  -1480208601 1174202142  -1474358038
"""