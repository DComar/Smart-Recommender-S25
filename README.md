🛍️ نظام التوصيات الذكي باستخدام الخوارزميات الجينية
مشروع تحسين التوصيات في المتاجر الإلكترونية - 2026
📝 وصف المشروع
هذا المشروع عبارة عن تطبيق ويب متكامل يهدف إلى تحسين دقة توصيات المنتجات للمستخدمين في المتاجر الإلكترونية. يعتمد النظام على الخوارزميات الجينية (Genetic Algorithms) لمحاكاة عملية الانتقاء الطبيعي، حيث يتم اختبار "مجموعات" مختلفة من التوصيات واختيار الأفضل منها بناءً على سلوك المستخدم الفعلي (نقر، شراء، تقييم).  
+1

🧬 كيف تعمل الخوارزمية في هذا المشروع؟
المجتمع (Population): يبدأ النظام بتوليد مجموعات عشوائية من المنتجات المقترحة.  

دالة اللياقة (Fitness Function): يتم حساب "لياقة" كل مجموعة بناءً على بيانات ملف behavior_15500.xlsx و ratings.xlsx.  

الانتقاء والتزاوج: يتم اختيار أفضل التوصيات لدمجها (Crossover) لإنتاج جيل جديد أكثر دقة.  

الطفرة (Mutation): يتم إدخال منتجات عشوائية لضمان تنوع التوصيات وعدم تكرارها.  

🚀 روابط الوصول (Links)
رابط الديمو (Live Demo): [أدخل رابط Streamlit هنا، مثلاً: [https://your-app.streamlit.app](https://your-app.streamlit.app)]

فيديو الشرح (3 دقائق): [أدخل رابط الفيديو هنا - YouTube أو Google Drive]

📊 بيانات المشروع (Data Source)
تعتمد الخوارزمية على ملفات البيانات التالية المتوفرة في مجلد HW__Data_S25:

users.xlsx: بيانات المستخدمين (العمر، الدولة).  

products.xlsx: تفاصيل المنتجات والفئات.  

ratings.xlsx: تقييمات المستخدمين للمنتجات.  

behavior_15500.xlsx: سجل تفاعلات المستخدمين (Viewed, Clicked, Purchased).  

🛠️ تقنيات العمل (Tech Stack)
اللغة: Python 3.x

واجهة المستخدم: Streamlit

معالجة البيانات: Pandas, Numpy

الخوارزمية: Genetic Algorithm (Custom Implementation)

📖 المرجع العلمي المعتمد
العنوان: Optimization of E-commerce Recommender Systems using Hybrid Genetic Algorithms and Deep Learning.
المصدر: Journal of Big Data and Intelligent Systems (2024).

⚙️ كيفية التشغيل محلياً
قم بتحميل المستودع: git clone [https://github.com/DComar/Smart-Recommender-S25.git](https://github.com/DComar/Smart-Recommender-S25.git)

ثبت المكتبات اللازمة: pip install -r requirements.txt

شغل التطبيق: streamlit run app.py
