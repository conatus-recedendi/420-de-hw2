import torch
from torch.utils.data import Dataset
import pandas as pd
from sklearn.preprocessing import LabelEncoder

class CSVDataset(Dataset):
    def __init__(self, file_path):
        # pandas를 사용하여 데이터를 로드하고 저장
        df = pd.read_csv(file_path)
        encoder = LabelEncoder()
        
        encodedColumn = ['gender', 'education', 'region', 'loyalty_status', 'product_category', 'purchase_frequency']
        for column in encodedColumn:
            df[column] = encoder.fit_transform(df[column])
        
        
        self.data = df
    
    def __len__(self):
        # 데이터셋의 전체 길이를 반환
        return len(self.data)
    
    def __getitem__(self, idx):
        # 특정 인덱스의 데이터를 반환
        return self.data.iloc[idx]
