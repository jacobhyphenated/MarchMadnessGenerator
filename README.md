## March Madness Bracket Generator
Intelligently generate your 2023 March Madness Bracket. This script will generate a different bracket every time it is run. It uses a combination of random numbers and the [Five Thirty Eight Forecast](https://projects.fivethirtyeight.com/2023-march-madness-predictions/) to stochastically generate a bracket, telling you which team it expects to win each round.

### Running this script
You need to have python 3 installed.

1. Clone this project
1. Using a command line program, go to the cloned directory
1. run `python generateBracket.py`

### Output Format
By default the script will print the random winners of each round in the console. You can also choose a different output format by running `python generateBracket.py -o json`. The currently available output options are:
* `print` - the default, prints text into the console
* `json` - creates a json object structure mapping rounds to an array of winners
* `json-region` - further nests the json object with by mapping the region of each winning team within each round

### How does it work?
The starting point is the data that drives the Five Thirty Eight March Madness Predictions. This is available as a csv file from their website. A copy of that data is included in this project.

The program will go round by round calculating the winner based on the 538 projection. For example, if a team has an 80% chance to win the first round, and you run this program 1000 times, you would expect to see that team win about 800 times.

For subsequent rounds, the same process is repeated, but it uses a conditional probability calculated from the number on the Five Thirty Eight website. This is based on the formula:
```
P(A|B) = P(A and B) / P(B)
```

The value we want to use is `P(A|B)`, the probability of the team winning the round (given that they won the previous round). The Five Thirty Eight forecast will give us the `P(A and B)` value from their forecast. We can then use the probability of winning the previous round (`P(B)`) to finish the formula.

This process is repeated, round by round, until only one team remains.

### Defining the random seed
If you'd like to set the random seed used to generate the brackets, run
```
python generateBracket.py --seed=<seed>
```
where `<seed>` is the seed you would like to use.  This allows you to re-create a bracket using a given seed. 

### Qualifying Games
Often, probability forecasts will be published before all qualifying and play-in games are finished. This generator will reflect that uncertainty. As qualifying matches are completed, I will update the csv file with the probability data to account for any changes.

## License
The MIT License (MIT)

Copyright (c) 2023 Jacob Kanipe-Illig

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
