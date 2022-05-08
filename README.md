# all-that-glitters-is-not-gold
Masters project for NFT valuation comparing multiple methodologies.
Uses data up to 18th April 2022 for analysis.

## Visualisations

## Predictions

## Set-up
1. Clone repository
2. Navigate to repository folder
3. Run
> source setup.sh

Enter back into env with:
> source venv.sh

Leave with:
> deactivate

## Usage
### Data
In order to get CSV files:
> python3 data_gatherer.py id_start id_end series

Where:
- id_start: the id to start gethering from
- id_end: the id to stop gathering at
- series: the name to determine which series to gather

At some point these will be handled by a bash file.

### Graphing
In order to perform cluster analysis:
> python3 cluster_analysis.py series method d

Where:
- series: the name to dertemine which series to graph
- method: the method of analysis
    - FAMD
    - K-Prototype
    - PCA
    - K-Means
    - K-Mode
    - MCA
- d: the number of dimensions or clusters

In order to produce basic networks:
> python3 trade_network.py series method time_start time_end method_number

Where:
- series: the name to dertemine which series to graph
- method: the method of analysis
    - common_singles
    - common_pairs
    - common_sequences
    - common_associations
    - simple_loops
- time_start: eliminate transactions before this time (set to 0 to ignore)
- time_end: used with time start to select a window of transactions
- method_number: used with methods that require additional numbers