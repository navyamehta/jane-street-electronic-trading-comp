#We implement an innovative "micro" version of the Moving Average Convergence Divergence (MACD) Indicator by using
#12-reading and 20-reading exponential moving averages from the live inputs from the market-place. We have a small
#error margin of 0.15 to ensure that minor fluctuations don't severely affect our positions.

import pandas as pd
import numpy as np