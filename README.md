# news-image-20261121-entry (v2)

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/iAm-182/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/iAm-182/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page summing up Saturday 21 November 2026 in a single
image, drawn with PIL primitives (original vector artwork, no photos, no
downloaded images). **44 stories across 6 continents**, every one an event
of, or first reported on, Saturday 21 November 2026 (any time zone),
verified against live reporting on the day.

v2 fixes two date errors in v1 and more than doubles the coverage (16 → 44
stories): the Shenzhen trilateral summit ended on 19 November, so it is no
longer listed as today's news (it is named in the DATE CHECK box instead);
the missiles that crashed in Poland came down on 20 November, so today's
lead is NATO chief Rutte flying to Warsaw and Poland asking for
reinforcements. New in v2: COP31 in overtime, the M6.7 Peru earthquake,
BepiColombo entering orbit around Mercury, Saudi defences downing three
Houthi missiles over Riyadh, Bitcoin below $59,000, Nvidia's worst week
since 2008, Eisenkot tapped to form Israel's next government, the Siberian
military plane crash, the Gaza aid call, and 31 more briefs — plus a world
map pinning where each big story happened and a DATE CHECK box that names
what was deliberately left out as not-today's news.

Running `draw.py` regenerates `entry.png` (1024×1024, ~252 KB);
`main.py` copies that file to the grader's output folder. Deterministic:
two runs write identical bytes. The footer states the date discipline —
every story on the page was first reported on Saturday 21 November 2026.
