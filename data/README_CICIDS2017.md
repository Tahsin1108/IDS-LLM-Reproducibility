# Dataset

This project uses the public CIC-IDS2017 dataset from the Canadian Institute for Cybersecurity.

Dataset page:

https://www.unb.ca/cic/datasets/ids-2017.html

The raw CSV files are not redistributed in this repository. Users should download the dataset from the official source.

## Expected preprocessing

- Remove non-numeric columns
- Replace missing values
- Replace infinite values
- Clip numeric features at the 0.1st and 99.9th percentiles
- Encode labels
- Use an 80/20 stratified split with random_state = 42

## Expected split

- Training samples: 320,000
- Test samples: 80,000
