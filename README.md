# Lithuanian parliamentary election data

This repository stores a cleaned up version of Lithuanian parliamentary election voting data. The original data sets are freely available from <https://www.rinkejopuslapis.lt/ataskaitu-formavimas> website. The original data sets were downloaded on August 31, 2016. Some minor issues were fixed (mismatched total votes counts).

This data set was studied in a paper [1]. You may freely reuse the data in your analysis. Though a reference to [1] would be appreciated. 

Note that this data set does not contain any data about voting by post (preliminary voting) as well as no votes cast in embassies and consulates.

# Data structure

Each year data set is stored in 4 distinct files:
* "YYYY-parties.csv" - stores names of the parties which participated in the election
* "YYYY-major-district.csv" - stores names of the electoral districts
* "YYYY-minor-district.csv" - stores names of the poling stations, as well as number of registered voters and total vote count
* "YYYY-votes.csv" - stores number of votes cast for parties in polling stations

**YYYY-parties.csv**. This file stores two columns - `org_id` and `org_name`. `org_id` is an identifier for party whose name is `org_name`.

**YYYY-major-district.csv**. This file stores two columns - `major_id` and `major_name`. `major_id` is an identifier for an electoral district whose name is `major_name`.

**YYYY-minor-district.csv**. This file stores six columns:
* `minor_gid` - generic identifier for a polling station (this is a unique id)
* `major_id` - identifier of electoral district to which this polling station belongs
* `minor_id` - identifier assigned to a polling station by electoral commission (there are duplicates even in the same electoral district)
* `minor_name` - name of the polling station
* `registered_voters` - number of voter assigned to this polling station
* `votes` - number of votes cast in this polling station

**YYYY-votes.csv**. This files stores three columns:
* `minor_gid` - polling station identifier
* `org_id` - party identifier
* `votes` - votes cast for the party in the polling station

All data files contain exactly one header row with column names. All data files are semicolon separated.

# Tool

This repository also contains Python script file which helps converting
between the raw data downloaded and the data presented here (see `tool`
directory). It was tested on the 2020 election data.

# Updates

* 2018 November 20. Added 2016 election data.
* 2024 July 7. Added 2020 election data.

# References

1. A. Kononovicius, *Empirical analysis and agent-based modeling of Lithuanian parliamentary elections*, Complexity **2017**: 7354642. doi: [10.1155/2017/7354642](https://dx.doi.org/10.1155/2017/7354642). arXiv: [1704.02101 [physics.soc-ph]](https://arxiv.org/abs/1704.02101).
