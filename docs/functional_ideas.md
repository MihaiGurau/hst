# Functional project ideas

This document contains various functional that I should / could / might implement in the project.

## Charts and portfolio analysis

Adding charts that show what industry was most traded, what the most traded stocks were, etc.

Consider checking out the [streamlit-lightweight-charts](https://github.com/freyastreamlit/streamlit-lightweight-charts)
plugin for finance charts.

## Volume alerts

Consider triggering alerts when the volume to be traded exceeds what the company was worth
or the total traded volume on that date.

## More trading parameters

- [ ] daily / monthly trade frequency
- [ ] do not trade on day X if all selected stocks went down on day X
- [ ] choose to trade the best / second best / third best stock on a given day
- [ ] what about the worst ones? how quickly could you run out of money (**this might be out of scope**)

## Using LLMs, since it's 2024 and they're still all the craze

Consider using [Google Gemma](https://github.com/google-deepmind/gemma) to analyze news articles about the best
performing stock(s) (on a given period) and come up with summaries about why they performed well.

This will most likely be completely meaningless from a cause-effect standpoint, but it could be fun.

News articles could be retrieved from Seeking Alpha or other financial news websites.

Another idea would be to use LLMs to come up with analogies for the gains (e.g., 10k gains = "random LLM analogy here").
