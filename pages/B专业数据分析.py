import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import altair as alt



st.set_page_config(page_title="专业数据分析", layout="wide")


st.title("专业数据分析")
st.markdown('***')
st.header("1. 各专业男女性别比例")


df_student = pd.read_csv("学生数据.txt")


gender_count = df_student.groupby(["专业", "性别"]).size().unstack(fill_value=0)

if gender_count.columns.tolist() == ["男", "女"]:
    gender_count = gender_count[["女", "男"]]


gender_ratio = (gender_count / gender_count.sum(axis=1).values.reshape(-1, 1) * 100).round(1)

df_gender = gender_ratio.reset_index()
df_gender.columns = ["major", "女", "男"]  


fig_gender = go.Figure()

fig_gender.add_trace(go.Bar(
    x=df_gender["major"],
    y=df_gender["男"],
    name="男",
    marker_color="#87CEEB"
))

fig_gender.add_trace(go.Bar(
    x=df_gender["major"],
    y=df_gender["女"],
    name="女",
    marker_color="#4169E1"
))

fig_gender.update_layout(
    barmode="group",  
    xaxis_title="专业",  
    yaxis_title="比例(%)", 
    height=400,  
    legend_title="性别",  
    legend=dict(orientation="v", yanchor="top", y=0.99, xanchor="right", x=0.99)  
)


col1, col2 = st.columns([2, 1]) 
with col1:
    
    st.plotly_chart(fig_gender, use_container_width=True)
with col2:
    
    st.subheader("性别比例数据")
    
    st.dataframe(df_gender.set_index("major"), use_container_width=True)





st.markdown('***')
st.header("2.各专业学习指标对比")
st.caption("各专业平均学习时间与成绩对比")

df = pd.read_csv("学生数据.txt")

metrics = ["每周学习时长（小时）", "期中考试分数", "期末考试分数"]
df_major = df.groupby("专业")[metrics].mean().round(1).reset_index()
df_melt = df_major.melt(id_vars="专业", var_name="指标", value_name="数值")


bar_layer = alt.Chart(df_melt[df_melt["指标"] == "期中考试分数"]).mark_bar(color="#4169E1").encode(
    x=alt.X("专业", axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("数值", title="指标数值"),
    tooltip=["专业", "指标", "数值"]
)

line_layer1 = alt.Chart(df_melt[df_melt["指标"] == "每周学习时长（小时）"]).mark_line(point=True, color="#87CEEB").encode(
    x="专业",
    y="数值",
    tooltip=["专业", "指标", "数值"]
)

line_layer2 = alt.Chart(df_melt[df_melt["指标"] == "期末考试分数"]).mark_line(point=True, color="#FF6347").encode(
    x="专业",
    y="数值",
    tooltip=["专业", "指标", "数值"]
)


chart = bar_layer + line_layer1 + line_layer2
chart = chart.properties(height=400).configure_axis(titleFontSize=14, labelFontSize=12)

col1, col2 = st.columns([3, 2])
with col1:
    st.altair_chart(chart, use_container_width=True, theme="streamlit")
with col2:
    st.subheader("详细数据")
    st.dataframe(df_major.set_index("专业"), use_container_width=True)
majors = ["期末考试分数", "期中考试分数", "每周学习时长（小时）"]
colors = ["#0000FF", "#FFA500", "#FF0000"]


cols = st.columns(len(majors))
for col, major, color in zip(cols, majors, colors):
    with col:
        st.markdown(
            f'<div style="display:flex; align-items:center;">'
            f'<div style="width:15px; height:15px; background-color:{color}; margin-right:8px; border-radius:2px;"></div>'
            f'{major}'
            f'</div>',
            unsafe_allow_html=True
        )





        





st.markdown('***')
st.header("3.各专业出勤率分析")
st.subheader("出勤率排名")


df = pd.read_csv("学生数据.txt")
df_attendance = df.groupby("专业")["上课出勤率"].mean().reset_index()
df_attendance["平均出勤率"] = (df_attendance["上课出勤率"] * 100).round(1)
df_attendance_sorted = df_attendance.sort_values("平均出勤率", ascending=False).reset_index(drop=True)
df_attendance_sorted["排名"] = df_attendance_sorted.index
df_result = df_attendance_sorted[["排名", "专业", "平均出勤率"]]


chart = (
    alt.Chart(df_result)
    .mark_bar()
    .encode(
        x=alt.X("专业", sort="-y", title="专业"),
        y=alt.Y("平均出勤率", title="平均出勤率(%)"),
        color=alt.Color("专业", scale=alt.Scale(scheme="category10")),  
        tooltip=["排名", "专业", "平均出勤率"]
    )
    .properties(height=350)
)


col_chart, col_table = st.columns([1, 1])
with col_chart:
    st.altair_chart(chart, use_container_width=True, theme="streamlit")
with col_table:
    st.dataframe(df_result.set_index("排名"), use_container_width=True)



st.markdown('***')
st.header("4.大数据管理专业专项分析")


df = pd.read_csv("学生数据.txt")
df_bd = df[df["专业"] == "大数据管理"].copy()


avg_study = df_bd["每周学习时长（小时）"].mean().round(1)
avg_attend = (df_bd["上课出勤率"].mean() * 100).round(1)
avg_final = df_bd["期末考试分数"].mean().round(1)
pass_rate = round((len(df_bd[df_bd["期末考试分数"] >= 60]) / len(df_bd) * 100), 1)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("平均学习时间", f"{avg_study} 小时")
with col2:
    st.metric("平均出勤率", f"{avg_attend}%")
with col3:
    st.metric("平均期末成绩", f"{avg_final} 分")
with col4:
    st.metric("及格率", f"{pass_rate}%")


st.subheader("大数据管理专业期末成绩箱线图")
boxplot = (
    alt.Chart(df_bd)
    .mark_boxplot(color="#4169E1", size=60)
    .encode(
        x=alt.X("专业:N", title="专业", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("期末考试分数:Q", title="期末成绩（分）", scale=alt.Scale(domain=[40, 100])),
        tooltip=["期末考试分数"]
    )
    .properties(height=350)
)
st.altair_chart(boxplot, use_container_width=True, theme="streamlit")


st.subheader("大数据管理专业期末成绩分布")
histogram = (
    alt.Chart(df_bd)
    .mark_bar(color="#87CEEB", opacity=0.8)
    .encode(
        x=alt.X("期末考试分数:Q", title="期末成绩（分）", bin=alt.Bin(maxbins=10)),
        y=alt.Y("count():Q", title="学生人数"),
        tooltip=[alt.Tooltip("期末考试分数:Q", bin=True, title="成绩区间"), "count():Q"]
    )
    .properties(height=350)
)
st.altair_chart(histogram, use_container_width=True, theme="streamlit")
