import pandas as pd
import joblib
import os
import requests
from io import BytesIO
from PIL import Image
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

st.set_page_config(
    page_title="期末成绩预测",
    page_icon="📊",
    layout="wide"  
)

def train_and_save_model(data_path):
    if not os.path.exists(data_path):
        st.error(f"数据文件 {data_path} 不存在，请检查文件路径！")
        return None, None
    """训练成绩预测模型并保存（首次运行自动执行）""" 
    df = pd.read_csv(data_path, encoding="utf-8")
    
    feature_cols = ["性别", "专业", "每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率"]
    target_col = "期末考试分数"
    X = df[feature_cols]
    y = df[target_col]
    
    categorical_features = ["性别", "专业"]
    numerical_features = ["每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(sparse_output=False, drop="first"), categorical_features),
            ("num", StandardScaler(), numerical_features)
        ])
    
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    model.fit(X, y)
    
    joblib.dump(model, "grade_prediction_model.pkl")
    joblib.dump(feature_cols, "feature_columns.pkl")
    return model, feature_cols

def load_model():
    model_path = "grade_prediction_model.pkl"
    feature_path = "feature_columns.pkl"
    data_path = "学生数据.txt"
    
    if not os.path.exists(model_path) or not os.path.exists(feature_path):
        with st.spinner("首次运行，正在训练预测模型..."):
            return train_and_save_model(data_path)
    else:
        model = joblib.load(model_path)
        feature_cols = joblib.load(feature_path)
        return model, feature_cols

model, feature_cols = load_model()

st.title("期末成绩预测")
st.subheader("请输入学生的学习信息，系统将预测其期末成绩并提供学习建议")
    
col1, col2 = st.columns(2, gap="large")
    
with col1:
    student_id = st.text_input("学号", placeholder="请输入学号（如2023000001）")
    gender = st.selectbox("性别", ["男", "女"])
    majors = ["工商管理", "人工智能", "财务管理", "电子商务", "大数据管理"]
    major = st.selectbox("专业", majors)
    study_hours = st.number_input(
        "每周学习时长（小时）", 
        min_value=0.0, 
        max_value=60.0, 
        step=0.01, 
        placeholder="请输入学习时长"
    )
    
with col2:
    attendance = st.number_input(
        "上课出勤率", 
        min_value=0.0, 
        max_value=1.0, 
        step=0.01, 
        placeholder="如0.9表示90%"
    )
    midterm_score = st.number_input(
        "期中考试分数", 
        min_value=0.0, 
        max_value=100.0, 
        step=0.01, 
        placeholder="请输入期中分数"
    )
    homework_completion = st.number_input(
        "作业完成率", 
        min_value=0.0, 
        max_value=1.0, 
        step=0.01, 
        placeholder="如0.85表示85%"
    )
    
predict_btn = st.button("预测期末成绩", use_container_width=True)
    
if predict_btn:
    input_data = {
        "学号": student_id,
        "性别": gender,
        "专业": major,
        "每周学习时长（小时）": study_hours,
        "上课出勤率": attendance,
        "期中考试分数": midterm_score,
        "作业完成率": homework_completion
    }
        
    missing_fields = [k for k, v in input_data.items() if pd.isna(v) and k not in ["学号"]]
    if missing_fields:
        st.error(f"请完善以下必填字段：{', '.join(missing_fields)}")
    else:
        model_input = pd.DataFrame({
            "性别": [gender],
            "专业": [major],
            "每周学习时长（小时）": [study_hours],
            "上课出勤率": [attendance],
            "期中考试分数": [midterm_score],
            "作业完成率": [homework_completion]
        })
            
        with st.spinner("正在预测期末成绩..."):
            predicted_grade = model.predict(model_input)[0]
            predicted_grade_rounded = round(predicted_grade, 1)
            
        st.subheader("预测结果")
        st.success(f"预测期末成绩：{predicted_grade_rounded}分")
            
        pass_score = 60.0
        if predicted_grade_rounded >= pass_score:
            st.write("### Congratulations!")
            try:
                congrats_img = Image.open("congrats.png")
                st.image(congrats_img, caption="恭喜！成绩及格", use_container_width=True)
            except FileNotFoundError:
                congrats_url = "https://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web2208/site/picture/0/s4dbef854f7df48569a904af14df9d0c8.png"
                response = requests.get(congrats_url)
                st.image(Image.open(BytesIO(response.content)), caption="恭喜！成绩及格", use_container_width="auto")
            st.info("学习建议：继续保持当前学习节奏，可适当攻克薄弱知识点，提升成绩上限。")
        else:
            st.write("### 继续加油！")
            try:
                encourage_img = Image.open("encourage.png")
                st.image(encourage_img, caption="成绩暂未及格，继续努力", use_container_width="auto")
            except FileNotFoundError:
                encourage_url = "https://bpic.588ku.com/element_origin_min_pic/21/09/05/07841ac5d51073b5c7ac829f9f03a77b.jpg"
                response = requests.get(encourage_url)
                st.image(Image.open(BytesIO(response.content)), caption="成绩暂未及格，继续努力", use_container_width="auto")
            st.warning(f"学习建议：1. 增加每周学习时长（当前{study_hours}小时，建议提升至15小时以上）；2. 提高上课出勤率（当前{attendance*100:.0f}%，建议提升至80%以上）；3. 确保作业完成率达标（当前{homework_completion*100:.0f}%，建议提升至85%以上）。")
