import pandas as pd
import os

RAW_DATASET_DIR = './dataset/raw/'
OUTPUT_DIR = './dataset/processed/'

def convert_to_csv():
    for root, dirs, files in os.walk(RAW_DATASET_DIR):
        for file in files:
            if file.endswith('.txt'):
                input_path = os.path.join(root, file)

                relative_path = os.path.relpath(input_path, RAW_DATASET_DIR)
                output_path = os.path.join(OUTPUT_DIR, os.path.splitext(relative_path)[0] + '.csv')

                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                try:
                    df = pd.read_csv(input_path, sep='\t')
                    df.to_csv(output_path, index=False)
                    print(f'Converted {input_path} to {output_path}')
                except Exception as e:
                    print(f'Failed to convert {input_path}: {e}')

if __name__ == '__main__':
    convert_to_csv()



