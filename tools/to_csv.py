import os
import pandas as pd

def process_state_series_split(input_path: str, output_base_path: str):
    df = pd.read_csv(input_path, sep='\t', skip_blank_lines=True, encoding='utf-8-sig')
    df.columns = [c.strip() for c in df.columns]

    if 'series_id' not in df.columns:
        raise ValueError(f"'series_id' not found in file: {input_path}")

    df['series_id'] = df['series_id'].astype(str)

    filename = os.path.splitext(os.path.basename(input_path))[0]
    state_name = filename.split('.')[-1]

    output_dir = os.path.join(output_base_path, 'states', state_name)
    os.makedirs(output_dir, exist_ok=True)

    for series_id, group in df.groupby('series_id'):
        output_file = os.path.join(output_dir, f"{series_id.strip()}.csv")
        group.to_csv(output_file, index=False)
        print(f"[state] {series_id} → {output_file}")

def process_normal_file(input_path: str, input_root: str, output_root: str):
    df = pd.read_csv(input_path, sep='\t', skip_blank_lines=True, encoding='utf-8-sig')
    df.columns = [c.strip() for c in df.columns]

    rel_path = os.path.relpath(input_path, input_root)
    output_path = os.path.join(output_root, os.path.splitext(rel_path)[0] + '.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"normal] → {output_path}")

def process_all(input_root='dataset/raw', output_root='dataset/processed'):
    for root, _, files in os.walk(input_root):
        for file in files:
            if file.endswith('.txt'):
                input_path = os.path.join(root, file)
                rel_path_parts = os.path.relpath(root, input_root).split(os.sep)

                try:
                    if 'states' in rel_path_parts:
                        process_state_series_split(input_path, output_root)
                    else:
                        process_normal_file(input_path, input_root, output_root)
                except Exception as e:
                    print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    process_all()