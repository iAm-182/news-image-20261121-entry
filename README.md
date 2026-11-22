# news-image-20261121-entry (v3)

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/iAm-182/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/iAm-182/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page summing up Saturday 21 November 2026 in a single
image, drawn with PIL primitives (original vector artwork, no photos, no
downloaded images). **48 stories across 8 regions**, every one an event
of, or first reported on, Saturday 21 November 2026 (any time zone),
checked against live reporting after the day ended.

v3 is the full-day edition. v2 was built mid-day, so v3 adds the evening's
big stories: Iran's strikes on US bases in Bahrain, the capture of
'El Chapo Isidro' in Mexico, the drone strike on the Russian ship Sparta II
off Finland, Verstappen winning the Las Vegas Grand Prix, and the ATP
Finals semi-finals in Turin. It reports results instead of previews
(F1 qualifying, ATP semis), refreshes COP31 to its end-of-Saturday state
(still no deal, second day of overtime), and corrects the markets story to
the full day (Bitcoin plunged to $55,000 before bouncing back above
$60,000; $2.7bn liquidated).

v3 also fixes fourteen errors in v2, which listed Friday's (and older)
news as Saturday's: the Siberia An-12 crash was Tuesday 17 Nov,
Eisenkot's mandate was 8 Nov, the UK-EU deals, Denmark's expulsion,
Estonia's border decision, the GTA VI sales figure, France's UN request,
Trump's data-centre threat, the Austria hack disclosure and the US
AI-chip disclosure were all 19–20 Nov, the Onkalo licence was 22 Oct,
and Tom Skerritt died 21 Oct. The Zverev group match is replaced by the
Saturday semi-finals.
The Kryvyi Rih toll is corrected to 58 hurt, as reported on Saturday
morning. Every one of those items is named in the DATE CHECK box instead
of appearing as today's news. The page also carries a UTC timeline strip
showing when the day's big stories broke.

Running `draw.py` regenerates `entry.png` (1024×1024, under 1 MiB);
`main.py` copies that file to the grader's output folder. Deterministic:
two runs write identical bytes, and the layout code fails loudly on any
overflowing line instead of truncating text. The footer states the date
discipline — every story on the page was first reported on Saturday
21 November 2026.
