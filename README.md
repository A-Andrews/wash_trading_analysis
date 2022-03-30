# all-that-glitters-is-not-gold
Masters project for NFT valuation comparing multiple methodologies.

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
In order to get CSV files:
> python3 data_gatherer.py id_start id_end series
Where:
- id_start is the id to start gethering from
- id_end is the id to stop gathering at
- series is the name to determine which series to gather

At some point these will be handled by a bash file.