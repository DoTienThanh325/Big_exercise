import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import unicodedata
import joblib
def remove_diacritics(text):
    if pd.isna(text):
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ) 

# Xử lý dữ liệu
df = pd.read_csv('Problem 4/results.csv')
df.drop(columns='Unnamed: 0', inplace=True)
df = df[df['Price'] != 'N/a']
df['Price'] = df['Price'].apply(lambda x: x[1:len(x)-1])
df_epl = pd.read_csv('Problem 1/results.csv')
df_epl.drop(columns='Unnamed: 0', inplace=True)
df_epl['Player'] = df_epl['Player'].apply(remove_diacritics)
df_epl = df_epl[df_epl['Player'].isin(df['Player'])]
df_epl = df_epl[df_epl['Playing_time: Min'] > 900]
df = df.merge(df_epl, on = ['Player', 'Playing_time: Min'], how='outer')
df.to_csv('cauthu.csv', index = True)
df['Price'] = df['Price'].astype(float)
numeric_col = df.select_dtypes(include='number').columns
numeric_col = numeric_col.drop(['Performance: CrdY', 'Performance: CrdR', 'Price'])

#Phân nhóm giá cầu thủ
try:
    df['Price'] = pd.qcut(df['Price'], q = 3, labels=['Low', 'Medium', 'High'])
except:
    print('Lỗi phân chia giá cầu thủ')
    exit()

x = df[numeric_col].fillna(0)  
y = df['Price']

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# Chia dữ liệu thành tập huấn luyện và kiểm tra
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.25, random_state=42)

# Huấn luyện mô hình LogisticRegression
model = LogisticRegression(multi_class='multinomial', max_iter=1000, random_state=42)
model.fit(x_train, y_train)

# Dự đoán và đánh giá mô hình

accuracy = model.score(x_test, y_test)
print(f'Accuracy: {accuracy:.2f}')
y_pred = model.predict(x_test)
print(f'\nClassification Report:\n')
print(classification_report(y_test, y_pred))
print('\nConfusion Matrix:')
print(confusion_matrix(y_test, y_pred))

# Tầm quan trọng đặc trưng
features_importance = pd.DataFrame({
    'Feature': numeric_col,
    'Importance': np.abs(model.coef_[0])
})
features_importance = features_importance.sort_values('Importance', ascending=False, ignore_index=True)
print('Features importance dataframe:')
print(features_importance)

# Vễ biểu đồ
plt.figure(figsize=(10, 6))
plt.barh(features_importance['Feature'], features_importance['Importance'])
plt.xlabel('Features importance of Player transfer value classification')
plt.yticks(fontsize=5) 
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('Problem 4/Feature_importance.png')

joblib.dump(model, 'Problem 4/logistic_transfer_model.pkl')
joblib.dump(scaler, 'Problem 4/scaler.pkl')