import pandas as pd
import os

# 文件夹路径
input_folder = r"D:/NYU_research/big_data/raw/raw/states"
output_file = r"D:/NYU_research/big_data/raw/raw/states_filtered/all_filtered_data.txt"

# 确保输出目录存在
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# 创建一个空DataFrame来累积所有筛选后的数据
all_data = []

# 遍历所有txt文件
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)

        # 读入单个文件
        try:
            df = pd.read_csv(file_path, sep='\t', engine='python')
            df.columns = df.columns.str.strip()  # ⭐去掉列名空格
        except Exception as e:
            print(f"Failed to read {filename}: {e}")
            continue

        # 检查必须包含series_id列
        if 'series_id' not in df.columns:
            print(f"Skipping {filename} (no 'series_id' column)")
            continue

        # 筛选以003结尾的series_id（先strip再endswith）
        filtered_df = df[df['series_id'].astype(str).str.strip().str.endswith('003')]

        if filtered_df.empty:
            print(f"No valid data in {filename}, skipping.")
            continue

        # 从文件名提取州名，比如 la.data.7.Alabama.txt -> Alabama
        state_name = filename.split('.')[-2]  # 倒数第二个
        filtered_df['state_name'] = state_name

        # 将筛选后的数据加入累积列表
        all_data.append(filtered_df)

        print(f"Filtered data from {filename}, {len(filtered_df)} rows, state={state_name}")

# 所有文件处理完后，合并成一个总表
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # 保存到统一的大txt文件
    final_df.to_csv(output_file, sep='\t', index=False)

    print(f"All filtered data saved to {output_file}")
else:
    print("No data matched filter conditions.")