# ---------------------------------------------------------
# استيراد المكتبات البرمجية الأساسية
# ---------------------------------------------------------

# مكتبة بناء واجهات المستخدم التفاعلية
import streamlit as st
# مكتبة تحليل البيانات والتعامل مع الجداول
import pandas as pd
# مكتبة العمليات الحسابية والمنطقية المتقدمة
import numpy as np
# مكتبة برمجية لتوليد القيم العشوائية
import random

# ---------------------------------------------------------
# إعدادات الصفحة والواجهة
# ---------------------------------------------------------

# ضبط إعدادات صفحة الويب وتوسيع نطاق العرض
st.set_page_config(page_title="متجر الذكاء الاصطناعي", layout="wide")

# ---------------------------------------------------------
# 1. مرحلة جلب البيانات من ملفات الإكسل
# ---------------------------------------------------------

# تفعيل خاصية التخزين المؤقت لتسريع الأداء
@st.cache_data
def load_data():
    # المسار المجلد الذي يحتوي على الملفات
    path = "HW__Data_S25/"
    # قراءة بيانات المستخدمين
    users = pd.read_excel(f'{path}users.xlsx')
    # قراءة بيانات المنتجات
    products = pd.read_excel(f'{path}products.xlsx')
    # قراءة سجل تقييمات المستخدمين
    ratings = pd.read_excel(f'{path}ratings.xlsx')
    # قراءة سجل سلوكيات المستخدمين (نقر، شراء، مشاهدة)
    behavior = pd.read_excel(f'{path}behavior_15500.xlsx')
    return users, products, ratings, behavior

# تخزين الجداول المحملة في متغيرات برمجية
users, products, ratings, behavior = load_data()

# ---------------------------------------------------------
# 2. منطق الخوارزمية الجينية (عملية الاختيار والتطوير)
# ---------------------------------------------------------



# دالة لتقييم جودة الاقتراحات بناءً على التاريخ السلوكي
def calculate_fitness(chromosome, user_id, behavior, ratings):
    total_score = 0
    # المرور على كل منتج داخل المجموعة المقترحة
    for prod_id in chromosome:
        # استخراج سجل تفاعل المستخدم الحالي مع هذا المنتج
        user_behav = behavior[(behavior['user_id'] == user_id) & (behavior['product_id'] == prod_id)]
        if not user_behav.empty:
            score = 0
            # منح 20 نقطة في حال شراء المنتج سابقاً
            if user_behav.iloc[0]['purchased']: score += 20
            # منح 10 نقاط في حال النقر على المنتج
            elif user_behav.iloc[0]['clicked']: score += 10
            # منح نقطتين في حال المشاهدة فقط
            elif user_behav.iloc[0]['viewed']: score += 2
            total_score += score
        
        # استخراج تقييم المستخدم للمنتج من جدول التقييمات
        user_rate = ratings[(ratings['user_id'] == user_id) & (ratings['product_id'] == prod_id)]
        if not user_rate.empty:
            # إضافة قيمة التقييم بعد مضاعفتها لتعزيز دقة التوصية
            total_score += user_rate.iloc[0]['rating'] * 2
            
    return total_score

# الدالة الرئيسية لتوليد التوصيات باستخدام التطور الجيني
def get_genetic_recommendations(user_id, products, behavior, ratings, pop_size=20, generations=10):
    # تحويل قائمة أرقام المنتجات المتوفرة إلى صيغة قائمة
    all_product_ids = products['product_id'].tolist()
    
    # [أ] تكوين المجتمع الأولي: توليد 20 مجموعة عشوائية
    population = [random.sample(all_product_ids, 5) for _ in range(pop_size)]
    
    # [ب] بدء دورة حياة الأجيال الجينية
    for _ in range(generations):
        # تقييم جودة كل مجموعة (كروموسوم) في المجتمع الحالي
        fitness_scores = [calculate_fitness(chrom, user_id, behavior, ratings) for chrom in population]
        
        # [ج] مرحلة الاختيار: تحديد أفضل مجموعتين (أبوين)
        sorted_indices = np.argsort(fitness_scores)[-2:]
        parent1, parent2 = population[sorted_indices[-1]], population[sorted_indices[-2]]
        
        # [د] مرحلة التزاوج: إنتاج جيل جديد يجمع خصائص الأبوين
        child = parent1[:2] + parent2[2:]
        
        # [هـ] مرحلة الطفرة: تغيير عشوائي بسيط بنسبة عشرة بالمئة لضمان التنوع
        if random.random() < 0.1:
            child[random.randint(0, 4)] = random.choice(all_product_ids)
            
        # [و] عملية الاستبدال: استبدال المجموعة الأضعف بالمجموعة الجديدة المطورة
        min_fit_idx = np.argmin(fitness_scores)
        population[min_fit_idx] = child
        
    # البحث عن المجموعة الأفضل في الجيل الأخير وإرجاعها
    best_idx = np.argmax([calculate_fitness(c, user_id, behavior, ratings) for c in population])
    return population[best_idx]

# ---------------------------------------------------------
# 3. واجهة المستخدم الرسومية وتفاعل النظام
# ---------------------------------------------------------

# ضبط إعدادات القائمة الجانبية
st.sidebar.header("لوحة التحكم")
# استخراج قائمة معرفات المستخدمين
user_list = users['user_id'].tolist()
# إنشاء قائمة اختيار منسدلة للمستخدم
selected_user = st.sidebar.selectbox("اختر مستخدم (ID):", user_list)

# عرض العنوان الرئيسي في الصفحة
st.title("🛍️ نظام التوصيات المتطور بالخوارزميات الجينية")
st.markdown("---")

# تقسيم مساحة العرض إلى عمودين بنسب متفاوتة
col1, col2 = st.columns([1, 2])

# الجزء المخصص لعرض تفاصيل المستخدم الحالي
with col1:
    st.subheader("👤 بيانات المستخدم")
    # استرجاع بيانات الصف الأول للمستخدم المختار
    u_info = users[users['user_id'] == selected_user].iloc[0]
    st.write(f"**العمر:** {u_info['age']}")
    st.write(f"**الدولة:** {u_info['country']}")

# الجزء المخصص لتشغيل الخوارزمية وعرض النتائج
with col2:
    st.subheader("💡 التوصيات المقترحة")
    # تفعيل الخوارزمية عند الضغط على زر التوليد
    if st.button("توليد أفضل التوصيات"):
        with st.spinner('جاري تشغيل عملية الانتقاء الطبيعي للمنتجات...'):
            # طلب التوصيات من محرك الخوارزمية الجينية
            rec_ids = get_genetic_recommendations(selected_user, products, behavior, ratings)
            # فلترة جدول المنتجات لعرض المقترحات المختارة فقط
            rec_products = products[products['product_id'].isin(rec_ids)]
            
            # عرض كل منتج مقترح في صندوق معلومات مستقل
            for index, row in rec_products.iterrows():
                with st.expander(f"منتج رقم: {row['product_id']} - {row['category']}"):
                    st.write(f"السعر: **${row['price']}**")
                    st.write("سبب التوصية: تطابق عالٍ مع نمط سلوكك الشرائي.")
