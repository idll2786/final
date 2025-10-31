import pandas as pd
import plotly.express as px
import streamlit as st



st.set_page_config(page_title="学生成绩分析平台", page_icon="", layout="wide")

import streamlit as st

st.set_page_config(page_title='学生成绩分析与预测系统', page_icon='🎓', layout="wide")
st.title('🎓学生成绩分析与预测系统')
st.markdown('***')
st.header('📄项目概述')
st.text('本项目是一个基于 Streamlit 的学生成绩分析平台，通过数据可视化和机器学习技术，帮助教育工作者和学生深入了解学业表现，并预测期末考试成绩。')
st.subheader('主要特点：')
st.markdown('''- 📊数据可视化：多维度展示学生学业数据
- 🎯专业分析：按专业分类的详细统计分析
- 📱智能预测：基于机器学习模型的成绩预测
- 💡学习建议：根据预测结果提供个性化反馈''')


st.markdown('***')
st.header('⭐️项目目标')
col1, col2, col3 = st.columns([3, 3, 3])
with col1:
    st.subheader('🎯目标一')
    st.text('分析影响因素')
    st.markdown('''- 识别关键学习指标
- 探索成绩相关因素
- 提供数据支持决策''')

with col2:
    st.subheader('📈目标二')
    st.text('可视化展示')
    st.markdown('''- 专业对比分析
- 性别差异研究
- 学习模式识别''')

with col3:
    st.subheader('💡目标三')
    st.text('成绩预测')
    st.markdown('''- 机器学习模型
- 个性化预测
- 及时干预预警''')


st.markdown('***')
st.header('技术架构')
col1, col2, col3 = st.columns([3, 3, 3])
with col1:
    st.text('前段框架')
    python_code = 'streamlit'
    st.code(python_code)

with col2:
    st.text('数据处理')
    python_code = '''Pandas
NumPy'''
    st.code(python_code)

with col3:
    st.text('可视化')
    python_code = '''Plotly
Matplotlib'''
    st.code(python_code)
