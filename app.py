import streamlit as st
import pandas as pd
import numpy as np
import random

# إعداد واجهة الموقع
st.set_page_config(page_title="متجر الذكاء الاصطناعي", layout="wide")

# 1. تحميل البيانات
@st.cache_data
def load_data():
    path = "HW__Data_S25/" # تأكد من اسم المجلد لديك
    users = pd.read_excel(f'{path}users.xlsx')
    products = pd.read_excel(f'{path}products.xlsx')
    ratings = pd.read_excel(f'{path}ratings.xlsx')
    behavior = pd.read_excel(f'{path}behavior.xlsx')
    return users, products, ratings, behavior

users, products, ratings, behavior = load_data()

# 2. منطق الخوارزمية الجينية (GA Logic)
def calculate_fitness(chromosome, user_id, behavior, ratings):
    """
    دالة اللياقة: تحسب جودة مجموعة التوصيات بناءً على سلوك المستخدم السابق.
    """
    total_score = 0
    for prod_id in chromosome:
        # البحث في السلوك (Behavior)
        user_behav = behavior[(behavior['user_id'] == user_id) & (behavior['product_id'] == prod_id)]
        if not user_behav.empty:
            score = 0
            if user_behav.iloc[0]['purchased']: score += 20  # وزن عالٍ للشراء
            elif user_behav.iloc[0]['clicked']: score += 10 # وزن متوسط للنقر
            elif user_behav.iloc[0]['viewed']: score += 2   # وزن منخفض للمشاهدة
            total_score += score
        
        # البحث في التقييمات (Ratings)
        user_rate = ratings[(ratings['user_id'] == user_id) & (ratings['product_id'] == prod_id)]
        if not user_rate.empty:
            total_score += user_rate.iloc[0]['rating'] * 2 # إضافة التقييم للياقة
            
    return total_score

def get_genetic_recommendations(user_id, products, behavior, ratings, pop_size=20, generations=10):
    all_product_ids = products['product_id'].tolist()
    
    # 1. إنشاء المجتمع الأولي (Random Population)
    # كل كروموسوم هو قائمة من 5 منتجات
    population = [random.sample(all_product_ids, 5) for _ in range(pop_size)]
    
    for _ in range(generations):
        # 2. تقييم اللياقة
        fitness_scores = [calculate_fitness(chrom, user_id, behavior, ratings) for chrom in population]
        
        # 3. الاختيار (Selection) - اختيار أفضل الوالدين
        sorted_indices = np.argsort(fitness_scores)[-2:]
        parent1, parent2 = population[sorted_indices[-1]], population[sorted_indices[-2]]
        
        # 4. التزاوج (Crossover)
        child = parent1[:2] + parent2[2:]
        
        # 5. الطفرة (Mutation) - استبدال منتج عشوائي بمنتج جديد تماماً
        if random.random() < 0.1:
            child[random.randint(0, 4)] = random.choice(all_product_ids)
            
        # استبدال الحل الأضعف بالطفل الجديد
        min_fit_idx = np.argmin(fitness_scores)
        population[min_fit_idx] = child
        
    # إرجاع أفضل حل تم الوصول إليه
    best_idx = np.argmax([calculate_fitness(c, user_id, behavior, ratings) for c in population])
    return population[best_idx]

# 3. واجهة المستخدم (UI)
st.sidebar.header("لوحة التحكم")
user_list = users['user_id'].tolist()
selected_user = st.sidebar.selectbox("اختر مستخدم (ID):", user_list)

st.title("🛍️ نظام التوصيات المتطور بالخوارزميات الجينية")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("👤 بيانات المستخدم")
    u_info = users[users['user_id'] == selected_user].iloc[0]
    st.write(f"**العمر:** {u_info['age']}")
    st.write(f"**الموقع:** {u_info['location']}")

with col2:
    st.subheader("💡 التوصيات المقترحة")
    if st.button("توليد أفضل التوصيات"):
        with st.spinner('جاري تشغيل عملية الانتقاء الطبيعي للمنتجات...'):
            rec_ids = get_genetic_recommendations(selected_user, products, behavior, ratings)
            rec_products = products[products['product_id'].isin(rec_ids)]
            
            for index, row in rec_products.iterrows():
                with st.expander(f"منتج رقم: {row['product_id']} - {row['category']}"):
                    st.write(f"السعر: **${row['price']}**")
                    st.write("سبب التوصية: تطابق عالٍ مع نمط سلوكك الشرائي.")