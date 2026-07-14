import streamlit as st
import PyPDF2
import os
import re
import streamlit.components.v1 as components
import base64
from pathlib import Path



if 'selected_department' not in st.session_state:
    st.title("🎓  Choose your department")
    
    
    # أقسام الهندسة
    departments = {
        "Computer and Systems Engineering(CSE)": "cse",
        "Artificial Intellegence Engineering (AI)": "ai",
        "Electronics and Communications Engineering(ECE)": "communications", 
        "Biomedical Engineering(BME)": "medical",
        "Mechatronics Engineering(MTE)": "mechatronics",
        "Architectural  Engineering(ARC)": "architecture",
        "Civil Engineering(CIV)": "civil",
        "Sustainable Architecture Engineering(SAE)": "ARC",
        "Preparatory Level 0": "pre"
    }
    
    cols = st.columns(2)
    
    for i, (dept_name, dept_code) in enumerate(departments.items()):
        with cols[i % 2]:
            if st.button(f"**{dept_name}**", use_container_width=True, key=dept_code):
                st.session_state.selected_department = dept_code
                st.session_state.department_name = dept_name
                st.rerun()

else:
    # إذا تم اختيار قسم، عرض الشات بوت
    department_name = st.session_state.get('department_name', 'هندسة الحاسوب')
    
    st.title(f"💻 {department_name} - Chatbot")
    st.markdown("---")
    
    # زر للعودة لاختيار القسم
    if st.button("🔄 Change Department", use_container_width=False):
        if 'selected_department' in st.session_state:
            del st.session_state.selected_department
        if 'department_bot' in st.session_state:
            del st.session_state.department_bot
        if 'chat_history' in st.session_state:
            st.session_state.chat_history = []
        st.rerun()

class CompleteCSEBot:
    def __init__(self, department="cse"):
        self.department = department
        self.pdf_path = self.get_department_pdf_path(department)
        self.full_text = ""
        self.total_pages = 0
        self.chunks = []
        self.is_loaded = False
        
        # جميع الأسئلة المتوقعة وإجاباتها مع أنماط مطابقة موسعة
        self.comprehensive_qa = {}
        
        # استدعاء الدوال حسب القسم
        if department == "cse":
            self.setup_cse_qa()
        elif department == "ai":
            self.setup_ai_qa()
        elif department == "mechatronics":
            self.setup_mechatronics_qa()
        elif department == "communications":
            self.setup_communications_qa()
        elif department == "medical":
            self.setup_medical_qa()
        elif department == "architecture":
            self.setup_architecture_qa()
        elif department == "civil":
            self.setup_civil_qa()
        elif department == "ARC":
            self.setup_ARC_qa() 
        elif department == "pre":
            self.setup_pre_qa()    
    def setup_cse_qa(self):
        """إعداد QA لهندسة الحاسوب"""
        self.comprehensive_qa = {
             'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات',  'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],

                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },

            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                    "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",
 
                ],
                'response': self.get_Cse_prerequisites0_response()
            },
            
            # المواد الإجبارية
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
             
                ],
                'response': self.get_Cse_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
    
                ],
                'response': self.get_Cse_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
                  
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
      
            
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
      # العقوبات التأديبية
           # 'disciplinary': {
           #     'patterns': [
            #        'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
            #        'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
              #      'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
              #  ],
             #   'questions': [
            #        "ما هي العقوبات التأديبية؟",
             #       "ما أنواع المخالفات التأديبية؟",
            #        "كيف يتم معالجة المخالفات السلوكية؟"
              #  ],
              # # 'response': self.get_Cse_disciplinary_response()
           # },
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل','توزيع'
                ],
                'questions': [
                    "توزيع الدرجات?"
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
                 
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات
            'transfers': {
                'patterns': [
                    'تحويل', 'نقل', 'تحويل من قسم', 'تحويل إلى قسم', 'transfer', 
                    'تحويل قسم', 'نقل قسم', 'التحويل بين الأقسام', 'شروط التحويل',
                    'كيف أنتقل قسم', 'تحويل تخصص', 'التحويل الداخلي'
                ],
                'questions': [
              
                    "كيف يتم تحويل للقسم؟"
                ],
                'response': self.get_Cse_transfers_response()
            },
            
           
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'gpa<2', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"
                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
             
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },

            # اللائحة القديمة vs الجديدة
            'regulation_comparison': {
                'patterns': [
                    'لائحة قديمة', 'لائحة جديدة', 'فرق', 'مقارنة', 'اختلاف', 'التغييرات',
                    'قديم vs جديد', 'اللائحة الجديدة', 'اللائحة القديمة', 'التحديثات',
                    'ماذا تغير', 'التعديلات', '170 ساعة', '160 ساعة', 'الفرق بين اللوائح',
                    'مقارنة اللائحة القديمة والجديدة', 'التغييرات في اللائحة'
                ],
                'questions': [
                    "ما الفرق بين اللائحة القديمة والجديدة؟",
                  
                ],
                'response': self.get_Cse_regulation_comparison_response()
            },

            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
                 
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب','Attendace'
                ],
                'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },

            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى؟",
                 
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
         
                ],
                'response': self.get_Cse_student_activities_response()
            },


            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
                
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
              
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
     
        }
        
    def setup_ARC_qa(self):
        self.comprehensive_qa = {
                   'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            
            # المتطلبات السابقة

            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                            "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",

                ],
                'response': self.get_ARC_prerequisites0_response()
            },
            
            # المواد الإجبارية

            
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
              
                ],
                'response': self.get_ARC_compulsory_courses_response()
            },
            
            # المواد الاختيارية

            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
                ],
                'response': self.get_ARC_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                   
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
              
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
           
            
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
            # العقوبات التأديبية
           # 'disciplinary': {
           #     'patterns': [
            #        'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
            #        'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
              #      'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
              #  ],
             #   'questions': [
            #        "ما هي العقوبات التأديبية؟",
             #       "ما أنواع المخالفات التأديبية؟",
            #        "كيف يتم معالجة المخالفات السلوكية؟"
              #  ],
              # # 'response': self.get_Cse_disciplinary_response()
           # },
            
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "كيفية  تقييم المواد؟",
      
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
                  
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات
            'transfers': {
                'patterns': [
                    'تحويل', 'نقل', 'تحويل من قسم', 'تحويل إلى قسم', 'transfer', 
                    'تحويل قسم', 'نقل قسم', 'التحويل بين الأقسام', 'شروط التحويل',
                    'كيف أنتقل قسم', 'تحويل تخصص', 'التحويل الداخلي'
                ],
                'questions': [
        
                    "كيف يتم تحويل المواد في التحويل للقسم؟"
                ],
                'response': self.get_ARC_transfers_response()
            },
            
           
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                     "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
             
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
                
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
        'attendance_removal': {
            'patterns': [
                'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب', 'attendance'
    ],
        'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

    ],
    'response': self.get_Cse_attendance_removal_response()  # استدعاء الدالة العامة
},
            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى ؟",
                
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
                   
                ],
                'response': self.get_Cse_student_activities_response()
            },

            # الخدمات الجامعية
    

            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
                   
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                  
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
           
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
    
        }
    def setup_ai_qa(self):
        """إعداد QA لهندسة الذكاء الاصطناعي"""
        self.comprehensive_qa = {
                   'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            
            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                     "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",

                ],
                'response': self.get_ai_prerequisites0_response()
            },
            # المتطلبات السابقة

            # المواد الإجبارية
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
                  
                ],
                'response': self.get_ai_compulsory_courses_response()
            },
            

            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
                 
                ],
                'response': self.get_ai_elective_courses_response()
            },
            

            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                   
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
              
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
           
            
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
            # العقوبات التأديبية
           # 'disciplinary': {
           #     'patterns': [
            #        'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
            #        'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
              #      'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
              #  ],
             #   'questions': [
            #        "ما هي العقوبات التأديبية؟",
             #       "ما أنواع المخالفات التأديبية؟",
            #        "كيف يتم معالجة المخالفات السلوكية؟"
              #  ],
              # # 'response': self.get_Cse_disciplinary_response()
           # },
            
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "كيفية  تقييم المواد؟",
      
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
                  
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات
            'transfers': {
                'patterns': [
                    'تحويل', 'نقل', 'تحويل من قسم', 'تحويل إلى قسم', 'transfer', 
                    'تحويل قسم', 'نقل قسم', 'التحويل بين الأقسام', 'شروط التحويل',
                    'كيف أنتقل قسم', 'تحويل تخصص', 'التحويل الداخلي'
                ],
                'questions': [
        
                    "كيف يتم تحويل المواد في التحويل للقسم؟"
                ],
                'response': self.get_ai_transfers_response()
            },
            
           
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
             
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
                
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب'
                ],
                'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },

            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى ؟",
                
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
                   
                ],
                'response': self.get_Cse_student_activities_response()
            },

            # الخدمات الجامعية


            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
                   
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                  
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
           
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
    
        }
    def setup_mechatronics_qa(self):
        """إعداد QA للميكاترونكس"""
        self.comprehensive_qa = {
                   'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                    "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",

                ],
                'response': self.get_mechatronics_prerequisites0_response()
            },
            
            # المواد الإجبارية
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
                  
                ],
                'response': self.get_mechatronics_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
                
                ],
                'response': self.get_mechatronics_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
                   
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
          
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
          # العقوبات التأديبية
           # 'disciplinary': {
           #     'patterns': [
            #        'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
            #        'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
              #      'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
              #  ],
             #   'questions': [
            #        "ما هي العقوبات التأديبية؟",
             #       "ما أنواع المخالفات التأديبية؟",
            #        "كيف يتم معالجة المخالفات السلوكية؟"
              #  ],
              # # 'response': self.get_Cse_disciplinary_response()
           # },
             
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "كيفية  تقييم المواد؟",
               
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
              
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات
   
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
                
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
           
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب'
                ],
                'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },

            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى ؟",
                   
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
                   
                ],
                'response': self.get_Cse_student_activities_response()
            },


            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
             
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                   
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                    
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
               
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
       
        }
    
    def setup_communications_qa(self):
        """إعداد QA لهندسة الاتصالات"""
        self.comprehensive_qa = {
            'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                        "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",

                ],
                'response': self.get_communications_prerequisites0_response()
            },
            
            # المواد الإجبارية
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
                  
                ],
                'response': self.get_communications_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
                 
                ],
                'response': self.get_communications_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
                 
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
         
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
          # العقوبات التأديبية
           # 'disciplinary': {
           #     'patterns': [
            #        'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
            #        'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
              #      'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
              #  ],
             #   'questions': [
            #        "ما هي العقوبات التأديبية؟",
             #       "ما أنواع المخالفات التأديبية؟",
            #        "كيف يتم معالجة المخالفات السلوكية؟"
              #  ],
              # # 'response': self.get_Cse_disciplinary_response()
           # },
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "كيفية  تقييم المواد؟",
                   
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
                 
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات

            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
                 
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                   
                    "كيف يمكن أن أصبح من الأوائل؟"
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب'
                ],
                'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },

            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى ؟",
             
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
                 
                ],
                'response': self.get_Cse_student_activities_response()
            },

            # الخدمات الجامعية


            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
              
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                   
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                   
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
               
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
        
        }
    
    def setup_medical_qa(self):
        """إعداد QA للهندسة الطبية"""
        self.comprehensive_qa = {
         'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                    "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",

                ],
                'response': self.get_medical_prerequisites0_response()
            },
            
            # المواد الإجبارية
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
                  
                ],
                'response': self.get_medical_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
                 
                ],
                'response': self.get_medical_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
                
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
        
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
           # العقوبات التأديبية
           # 'disciplinary': {
           #     'patterns': [
            #        'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
            #        'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
              #      'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
              #  ],
             #   'questions': [
            #        "ما هي العقوبات التأديبية؟",
             #       "ما أنواع المخالفات التأديبية؟",
            #        "كيف يتم معالجة المخالفات السلوكية؟"
              #  ],
              # # 'response': self.get_Cse_disciplinary_response()
           # },
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "كيفية  تقييم المواد؟",
                   
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
                
                ],
                'response': self.get_Cse_registration_response()
            },
            
   
           
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
                  
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
                  
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب'
                ],
                'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },

            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى ؟",
                 
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
               
                ],
                'response': self.get_Cse_student_activities_response()
            },

            # الخدمات الجامعية
 
            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
                  
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                 
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                 
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
            
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
        
        }
    
    def setup_architecture_qa(self):
        """إعداد QA للهندسة المعمارية"""
        self.comprehensive_qa = {
         'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            
            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                    "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",

                ],
                'response': self.get_architecture_prerequisites0_response()
            },
            
            # المواد الإجبارية
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
                
                ],
                'response': self.get_architecture_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
                 
                ],
                'response': self.get_architecture_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
                   
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
        
            
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
           # 'disciplinary': {
           #     'patterns': [
            #        'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
            #        'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
              #      'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
              #  ],
             #   'questions': [
            #        "ما هي العقوبات التأديبية؟",
             #       "ما أنواع المخالفات التأديبية؟",
            #        "كيف يتم معالجة المخالفات السلوكية؟"
              #  ],
              # # 'response': self.get_Cse_disciplinary_response()
           # },
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "كيفية تقييم المواد؟",
              
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
                
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات
            'transfers': {
                'patterns': [
                    'تحويل', 'نقل', 'تحويل من قسم', 'تحويل إلى قسم', 'transfer', 
                    'تحويل قسم', 'نقل قسم', 'التحويل بين الأقسام', 'شروط التحويل',
                    'كيف أنتقل قسم', 'تحويل تخصص', 'التحويل الداخلي'
                ],
                'questions': [
              
                    "كيف يتم تحويل المواد في التحويل للقسم؟"
                ],
                'response': self.get_architecture_transfers_response()
            },
            
           
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
               
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
               
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب'
                ],
                'questions': [
                     "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },

            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى ؟",
                 
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
               
                ],
                'response': self.get_Cse_student_activities_response()
            },

            # الخدمات الجامعية
   
            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
                
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                  
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                  
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
                
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
        
        }
    def setup_civil_qa(self):
        """إعداد QA للهندسة المدنية"""
        self.comprehensive_qa = {
         'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            # المتطلبات السابقة
            'prerequisites': {
                'patterns': [
                    'متطلب', 'سابق', 'مرافق', 'يشترط', 'يجب', 'متطلبات', 'مسار', 
                    'prerequisite', 'corequisite', 'شرط', 'يشترط', 'متطلبات المواد',
                    'المتطلبات السابقة للمادة', 'شرط تسجيل المادة', 'المتطلبات اللازمة',
                    'ما هي المتطلبات', 'يشترط لدراسة', 'متطلبات قبل المادة', 'شروط المادة'
                ],
                'questions': [
                    "ما هي المسارات الدراسية الرئيسية(prerequisites)؟",

                ],
                'response': self.get_civil_prerequisites0_response()
            },
            
            # المواد الإجبارية
            'compulsory_courses': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في القسم؟",
              
                ],
                'response': self.get_civil_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة؟",
                 
                ],
                'response': self.get_civil_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
                   
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
    
            
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            
            # العقوبات التأديبية
            #'disciplinary': {
                #'patterns': [
                 #   'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
                #    'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
                 #   'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
                #],
                #'questions': [
                 #   "ما هي العقوبات التأديبية؟",
                 #   "ما أنواع المخالفات التأديبية؟",
                 #   "كيف يتم معالجة المخالفات السلوكية؟"
               # ],
              #  'response': self.get_Cse_disciplinary_response()
           # },
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "توزيع الدرجات في المواد؟",
         
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
              
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات
  
            
           
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
              
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
              
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب'
                ],
                'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },

            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى؟",
                 
                ],
                'response': self.get_Cse_student_rights_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
                 
                ],
                'response': self.get_Cse_student_activities_response()
            },

            # الخدمات الجامعية
          

            # السكن والمعيشة
            'housing': {
                'patterns': [
                    'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
                    'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
                    'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
                ],
                'questions': [
                    "كيفية التقديم للسكن الجامعي؟",
               
                ],
                'response': self.get_Cse_housing_response()
            },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                 
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                    
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
             
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },
        }
   # نظام الشكاوى والمقترحات
    def setup_pre_qa(self):
        """إعداد QA للهندسة المدنية"""
        self.comprehensive_qa = {
         'gpa_system': {
                'patterns': [
                    'معدل', 'تراكمي', 'نقاط', 'تقدير', 'حساب المعدل', 'كيفية حساب', 
                    'grade', 'point', 'average', 'gpa', 'المعدل التراكمي', 'تقديرات',
                    'درجات', 'نظام الدرجات', 'كيف احسب معدلي', 'حساب المعدل التراكمي',
                    'نظام النقاط', 'تقدير المواد', 'الدرجات النهائية', 'كيفية حساب المعدل'
                ],
                'questions': [
                    "كيف يتم حساب المعدل التراكمي(gpa)؟",
                 
                ],
                'response': self.get_Cse_gpa_response()
            },
            
            # الساعات المعتمدة
            'credit_hours': {
                'patterns': [
                    'ساعة', 'معتمدة', 'وحدات', 'إجمالي', 'عدد الساعات', 'مطلوب', 
                    'credit', 'hours', 'ساعات مطلوبة', 'عدد الوحدات', 'ساعات معتمدة',
                    'نظام الساعات', 'كيفية حساب الساعات', 'مجموع الساعات', 'ساعات التخرج',
                    'الساعات المطلوبة للتخرج', 'نظام الساعات المعتمدة', 'شرح الساعات المعتمدة',
                    'كم ساعة', 'عدد الساعات', 'ساعات الدراسة', 'مجموع الساعات المعتمدة'
                ],
                'questions': [
                    "كم عدد الساعات المطلوبة للتخرج؟",
               
                ],
                'response': self.get_Cse_credits_response()
            },
            
            
            # شروط التخرج
            'graduation': {
                'patterns': [
                    'تخرج', 'شهادة', 'شروط', 'متطلبات التخرج', 'شروط التخرج', 'التخرج', 
                    'graduation', 'requirements', 'شهادة التخرج', 'شروط نيل الشهادة',
                    'متطلبات التخرج النهائية', 'كيف اتخرج', 'شروط التخرج من الكلية',
                    'نهاية الدراسة', 'استلام الشهادة', 'إجراءات التخرج', 'موعد التخرج'
                ],
                'questions': [
                    "ما هي شروط التخرج من القسم؟",
                ],
                'response': self.get_Cse_graduation_response()
            },
            
            # المتطلبات السابقة

            # المواد الإجبارية
            'compulsory_courses Civil': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم الهندسة المدنية؟",
              
                ],
                'response': self.get_civil_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses Civil': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة لقسم الهندسة المدنية؟",
                 
                ],
                'response': self.get_civil_elective_courses_response()
            },
            
            # المشروع
            'project': {
                'patterns': [
                    'مشروع', 'تخرج', 'project', 'مشروع التخرج', 'graduation project', 'مشروع',
                    'مشروع التخرج', 'بحث التخرج', 'مشروع نهائي', 'مشروع التخرج', 'بحث التخرج'
                ],
                'questions': [
                    "كم عدد ساعات مشروع التخرج؟",
                ],
                'response': self.get_Cse_project_response()
            },
            
            # التدريب الميداني
            'training': {
                'patterns': [
                    'تدريب', 'ميداني', 'تدريب ميداني', 'field training', 'تدريب', 'training',
                    'التدريب الميداني', 'تدريب عملي', 'تدريب صيفي', 'التدريب الصيفي', 'تدريب مهني'
                ],
                'questions': [
                    "هل يوجد تدريب ميداني؟",
                   
                ],
                'response': self.get_Cse_training_response()
            },
            
            # الفصول الدراسية
            'semesters': {
                'patterns': [
                    'فصل', 'فصول', 'مستوى', 'ترتيب', 'خطة دراسية', 'semester', 'study plan', 
                    'خطة', 'مستويات', 'الخطة الدراسية', 'ترتيب الفصول', 'مستوى دراسي',
                    'جدول المواد', 'توزيع المواد', 'خطة الدراسة', 'الفصول الدراسية'
                ],
                'questions': [
                    "ما هي الخطة الدراسية المقترحة؟",
                ],
                'response': self.get_Cse_semesters_response()
            },
            
            # الرسوم والتكاليف
                'compulsory_courses CSE': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم هندسة الحاسب؟",
             
                ],
                'response': self.get_Cse_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses CSE': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة في قسم هندسة الحاسب؟",
    
                ],
                'response': self.get_Cse_elective_courses_response()
            },
            
            
            # نظام الغياب
            'attendance': {
                'patterns': [
                    'غياب', 'حضور', 'نسبة حضور', 'عقوبات غياب', 'attendance', 'absence', 
                    'نسبة الغياب', 'الغياب المسموح', 'حد الغياب', 'متى تحرم من الامتحان',
                    'نسبة الحرمان', 'الغياب يمنع الامتحان', 'الغياب والتأخير',
                    'كم يوم غياب مسموح', 'نسبة الغياب للحرمان', 'عقوبة الغياب'
                ],
                'questions': [
                    "ما هي نسبة الغياب المسموحة؟",
                ],
                'response': self.get_Cse_attendance_response()
            },
            'compulsory_courses Architecture': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم عمارة؟",
                
                ],
                'response': self.get_architecture_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses Architecture': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة في قسم عمارة؟",
                 
                ],
                'response': self.get_architecture_elective_courses_response()
            },            
            # الإنذارات الأكاديمية
            'warnings': {
                'patterns': [
                    'إنذار', 'إنذارات', 'إنذار أكاديمي', 'معدل منخفض', 'warning', 
                    'academic warning', 'انذار', 'الإنذار الأكاديمي', 'إنذار دراسي',
                    'متى يصدر الإنذار', 'عواقب الإنذار', 'الطلاب تحت الإنذار'
                ],
                'questions': [
                    "متى يصدر الإنذار الأكاديمي؟",
                ],
                'response': self.get_Cse_warnings_response()
            },
            'compulsory_courses Mechatronics': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم الميكاترونكس؟",
                  
                ],
                'response': self.get_mechatronics_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses Mechatronics': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة في قسم الميكاترونكس؟",
                
                ],
                'response': self.get_mechatronics_elective_courses_response()
            },            
            # العقوبات التأديبية
            #'disciplinary': {
                #'patterns': [
                 #   'عقوبات', 'تأديبية', 'مخالفات', 'سلوك', 'انضباط', 'disciplinary', 
                #    'punishment', 'عقوبة', 'العقوبات التأديبية', 'مخالفات سلوكية',
                 #   'انضباط طلابي', 'لجنة الانضباط', 'عقوبات سلوكية'
                #],
                #'questions': [
                 #   "ما هي العقوبات التأديبية؟",
                 #   "ما أنواع المخالفات التأديبية؟",
                 #   "كيف يتم معالجة المخالفات السلوكية؟"
               # ],
              #  'response': self.get_Cse_disciplinary_response()
           # },
            
            # الامتحانات
            'exams': {
                'patterns': [
                    'امتحان', 'اختبار', 'نهائي', 'midterm', 'امتحانات', 'exam', 'test', 
                    'final', 'اختبارات', 'الامتحان النهائي', 'امتحان منتصف الفصل',
                    'تقييم المواد', 'نظام الامتحانات', 'شروط الامتحان', 'امتحان نهاية الفصل'
                ],
                'questions': [
                    "توزيع الدرجات في المواد؟",
         
                ],
                'response': self.get_Cse_exams_response()
            },
            
            # التسجيل والإجراءات
            'registration': {
                'patterns': [
                    'تسجيل', 'إجراءات', 'سحب', 'إضافة', 'حذف', 'registration', 'add', 
                    'drop', 'تسجيل مواد', 'مواعيد التسجيل', 'فترة التسجيل', 'كيف اسجل',
                    'طريقة التسجيل', 'التسجيل في المواد', 'بداية التسجيل', 'نهاية التسجيل',
                    'موعد التسجيل', 'التسجيل متى يبدأ', 'وقت التسجيل', 'تسجيل المقررات'
                ],
                'questions': [
                    "كيفية التسجيل في المواد؟",
              
                ],
                'response': self.get_Cse_registration_response()
            },
            
            # التحويلات
            'compulsory_courses Communications': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم الاتصالات؟",
                  
                ],
                'response': self.get_communications_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses Communications': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة في قسم الاتصالات؟",
                 
                ],
                'response': self.get_communications_elective_courses_response()
            },
              
            
           
            
            # الطلاب تحت الإنذار
            'warning_students': {
                'patterns': [
                    'ساعات مسموحة','طالب تحت انذار', 'طالب انذار', 'ساعات قليلة', '12 ساعة', 
                    'حد ادنى ساعات', 'warning student', 'low gpa', 'معدل منخفض',
                    'gpa اقل من 2', 'الطلاب ضعيفي المستوى', 'تقييد ساعات',
                    'الحد الأقصى للساعات', 'الطالب اللايت لود', 'الطالب منخفض المعدل',
                    'قواعد التسجيل للمعدل المنخفض', 'الطلاب المحذرين', '14 ساعة'
                ],
                'questions': [
                    "قواعد التسجيل للمعدل المنخفض"

                ],
                'response': self.get_Cse_warning_students_response()
            },

            # إعادة الميدتيرم
            'midterm_retake': {
                'patterns': [
                    'ميدتيرم', 'إعادة', 'أعيد', 'امتحان منتصف', 'midterm', 'retake', 
                    'إعادة الامتحان', 'فرصة ثانية', 'إعادة الميدتيرم', 'form إعادة',
                    'نموذج إعادة', 'فورم إعادة', 'إعادة امتحان منتصف الفصل',
                    'كيف أعيد الميدتيرم', 'إجراءات إعادة الميدتيرم', 'امتحان بديل'
                ],
                'questions': [
              
                    "هل يوجد نموذج لإعادة الميدتيرم؟"
                ],
                'response': self.get_Cse_midterm_retake_response()
            },


            # تحديد الأوائل
            'top_students': {
                'patterns': [
                    'أول', 'متفوق', 'الأوائل', 'ترتيب', 'تصنيف', 'الأفضل', 'top', 'ranking',
                    'الطلاب المتفوقين', 'كيف يتم تحديد الأول', 'معايير التميز',
                    'آلية تحديد الأوائل', 'كيف يصبح الطالب أول', 'شروط التفوق',
                    'ترتيب الطلاب', 'التصنيف الأكاديمي'
                ],
                'questions': [
                    "كيف يتم تحديد الطلاب الأوائل؟",
              
                ],
                'response': self.get_Cse_top_students_response()
            },

            # إزالة أيام الغياب
            'attendance_removal': {
                'patterns': [
                    'إزالة غياب', 'إثبات مرض', 'عيادات الجامعة', 'عذر غياب', 'تخفيف غياب',
                    'إلغاء غياب', 'تصحيح غياب', 'تقديم عذر', 'مستندات الغياب',
                    'كيف أزيل الغياب', 'إجراءات إثبات المرض', 'العيادات الجامعية',
                    'شهادة مرضية', 'تعديل الغياب', 'حذف أيام الغياب'
                ],
                'questions': [
                    "كيف يمكن إزالة أيام الغياب Attendance؟",

                ],
                'response': self.get_Cse_attendance_removal_response()
            },
            'compulsory_courses AI': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم الذكاء الاصطناعي؟",
                  
                ],
                'response': self.get_ai_compulsory_courses_response()
            },
            'compulsory_courses Medical': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم طبية؟",
                  
                ],
                'response': self.get_medical_compulsory_courses_response()
            },
            
            # المواد الاختيارية
            'elective_courses Medical': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة في قسم طبية؟",
                 
                ],
                'response': self.get_medical_elective_courses_response()
            },            

            # المواد الاختيارية
            'elective_courses AI': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة في قسم الذكاء الاصطناعي؟",
                 
                ],
                'response': self.get_ai_elective_courses_response()
            },
            # شكاوى وحقوق الطالب
            'student_rights': {
                'patterns': [
                    'شكوى', 'مدرس', 'حقوق', 'طالب', 'اعتذار', 'إعفاء', 'رسوم', 'complaint', 
                    'rights', 'student', 'تقديم شكوى', 'شكوى مدرس', 'حقوق الطالب',
                    'كيف أقدم شكوى', 'الشكوى على المدرس', 'لجنة الشكاوى'
                ],
                'questions': [
                    "كيف أقدم شكوى؟",
                 
                ],
                'response': self.get_Cse_student_rights_response()
            },
            'compulsory_courses ARC': {
                'patterns': [
                    'إجباري', 'اجباري', 'مواد إجبارية', 'متطلبات إجبارية', 'compulsory', 
                    'mandatory', 'مواد اجبارية', 'المواد الإجبارية', 'مواد أساسية',
                    'متطلبات أساسية', 'مواد إلزامية', 'المواد المطلوبة', 'مواد القسم'
                ],
                'questions': [
                    "ما هي المواد الإجبارية في قسم العمارة المستدامة؟",
              
                ],
                'response': self.get_ARC_compulsory_courses_response()
            },
            
            # المواد الاختيارية

            # المواد الاختيارية
            'elective_courses ARC': {
                'patterns': [
                    'اختياري', 'مواد اختيارية', 'elective', 'مجموعة اختيارية', 'مواد اختياري', 
                    'electives', 'مواد اختيار', 'المواد الاختيارية', 'اختيار مواد',
                    'مجموعات اختيارية', 'مواد تخصصية', 'مواد اختيارية متاحة'
                ],
                'questions': [
                    "ما هي المواد الاختيارية المتاحة في قسم العمارة المستدامة؟",
                ],
                'response': self.get_ARC_elective_courses_response()
            },

            # الأنشطة الطلابية
            'student_activities': {
                'patterns': [
                    'أنشطة', 'أندية', 'طلابية', 'نادي', 'مسابقات', 'عمل تطوعي', 'أنشطة طلابية', 
                    'activities', 'clubs', 'volunteer', 'الأنشطة الطلابية', 'الأندية الطلابية',
                    'كيف أنضم لنادي', 'المسابقات العلمية', 'النشاط الطلابي'
                ],
                'questions': [
                    "ما هي المسابقات العلمية المتاحة؟",
                 
                ],
                'response': self.get_Cse_student_activities_response()
            },

            # الخدمات الجامعية
          

            # السكن والمعيشة
          #  'housing': {
           #     'patterns': [
              #      'سكن', 'جامعي', 'داخلي', 'إقامة', 'سكن طلابي', 'سكن داخلي', 'housing', 
             #       'dormitory', 'residence', 'السكن الجامعي', 'السكن الداخلي',
             #       'كيفية التقديم للسكن', 'مرافق السكن', 'السكن الطلابي'
             #   ],
             #   'questions': [
            #        "كيفية التقديم للسكن الجامعي؟",
            #   
           #     ],
           #     'response': self.get_Cse_housing_response()
          #  },

            # الدعم الأكاديمي
            'academic_support': {
                'patterns': [
                    'دعم', 'أكاديمي', 'مرشد', 'دراسي', 'تحصيلي', 'تحسين', 'مستوى', 
                    'academic support', 'advisor', 'tutoring', 'الدعم الأكاديمي',
                    'المرشد الأكاديمي', 'حصص تقوية', 'تحسين المستوى', 'الدعم الدراسي'
                ],
                'questions': [
                    "ما هي خدمات الدعم الأكاديمي المتاحة؟",
                 
                ],
                'response': self.get_Cse_academic_support_response()
            },

            # البحث العلمي
            'research': {
                'patterns': [
                    'بحث', 'علمي', 'أبحاث', 'منشورات', 'مجلات', 'علمية', 'research', 
                    'publications', 'journals', 'البحث العلمي', 'المجلات العلمية',
                    'كيف أشارك في أبحاث', 'النشر العلمي', 'الأبحاث العلمية'
                ],
                'questions': [
                    "كيف أشارك في الأبحاث العلمية؟",
                    
                ],
                'response': self.get_Cse_research_response()
            },

          
            # نظام المكافآت والحوافز
            'rewards_system': {
                'patterns': [
                    'مكافأة', 'حوافز', 'تشجيع', 'تفوق', 'تميز', 'جوائز', 'rewards',
                    'incentives', 'encouragement', 'المكافآت', 'الحوافز', 'جوائز التفوق'
                ],
                'questions': [
             
                    "ما هي جوائز التميز الأكاديمي؟"
                ],
                'response': self.get_Cse_rewards_system_response()
            },

            # نظام الشكاوى والمقترحات
          
            
        }

    
    def get_department_pdf_path(self, department):
        """الحصول على مسار ملف PDF حسب القسم"""
        base_path = r"C:\\Users\\Esra\\Desktop\\chat\\اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf"
        pdf_files = {
            "Cse": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf",
            "AI": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf",
            "ECE": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf",
            "BME": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf",
            "MTE": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf",
            "ARC": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf",
            "civil": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf",
            "civil": "اللائحــــة الداخليــة كلية الهندسة - جامعة حورس مصر لمرحلــــــــة البكالوريوس ( نظام الساعات المعتمدة ) 2025.pdf"
        }
        return os.path.join(base_path, pdf_files.get(department, "CSE Regulation 2025-9-22.pdf"))

    # ========== دوال هندسة الحاسوب (CSE) ==========
    
    def get_Cse_rewards_system_response(self):
        return """
## 🏆 نظام المكافآت والحوافز

### 💰 المكافآت المالية:
- **البحث العلمي:** منح للأبحاث المتميزة
- **الأنشطة:** جوائز للمشاركة الفعالة

### 📜 شهادات التقدير:
- **التفوق الدراسي:** شهادات للطلاب المتفوقين
- **التميز البحثي:** شهادات للمشاركة في الأبحاث
- **الأنشطة الطلابية:** شهادات للقيادة والمشاركة

### 🎯 حوافز أخرى:
- **الابتعاث:** فرص للدراسة بالخارج
- **التدريب:** فرص تدريب متميزة
"""

    def get_Cse_complaints_suggestions_response(self):
        return """
## 📝 نظام الشكاوى والمقترحات

### 📋 قنوات تقديم الشكاوى:
- **الإلكترونية:** عبر البوابة الإلكترونية
- **الورقية:** نماذج في شؤون الطلاب

"""

    # الدوال الأساسية
    def get_Cse_midterm_retake_response(self):
        return """
🔄 **نظام إعادة امتحان الميدتيرم - مفصل**

## 📋 إجراءات إعادة الميدتيرم:

### الخطوات:
1. *التسجيل في الفورم الخاصة بالاعادة اسأل عنها مرشدك الاكاديمي:** 
2. **اختيار المادة:** تحديد المادة المراد إعادة امتحانها
3. **تعبئة النموذج:** إدخال البيانات المطلوبة
4. **الموافقة الإلكترونية:** من المرشد الأكاديمي

"""

    def get_Cse_regulation_comparison_response(self):
        return """
🔄 **مقارنة اللائحة القديمة والجديدة - مفصل**

## 📊 الفروق الرئيسية:

### إجمالي الساعات:
- **اللائحة القديمة:** 170 ساعة معتمدة
- **اللائحة الجديدة:** 160 ساعة معتمدة
- **الفرق:** 10 ساعات أقل

## 🎯 مزايا اللائحة الجديدة:
- **مرونة أكبر:** مواد اختيارية أكثر
- **ملاءمة سوق العمل:** تخصصات حديثة
- **مشاريع عملية:** زيادة الجانب التطبيقي
"""

    def get_Cse_top_students_response(self):
        return """
🏆 **آلية تحديد الطلاب الأوائل - مفصل**

## 🎯 معايير التقييم:


## 📊 درجات التميز:
- **A+ → 100% to 97% --> 4.00
- **A  → 96% to 93%  --> 4.00
- **A- → 92% to 89%  --> 3.70
- **B+ → 88% to 84%  --> 3.30
- **B  → 83% to 80%  --> 3.00
- **B- → 79% to 76%  --> 2.70
- **C+ → 75% to 73%  --> 2.30
- **C  → 72% to 70%  --> 2.00
- **C- → 69% to 67%  --> 1.70
- **D+ → 66% to 64%  --> 1.30
- **D  → 63% to 60%  --> 1.00
- **F  → Less than 60% --> 0.00

"""

    def get_Cse_attendance_removal_response(self):
        return """
🏥 **إجراءات إزالة أيام الغياب - مفصل**

## 📋 الخطوات الرسمية:
1. **الحصول على الإثبات الطبي:** من عيادات الجامعة
2. **تعبئة النموذج:** استمارة إثبات عذر غياب
3. **التسليم والموافقة:** خلال أسبوع من العودة

## ⏰ المواعيد المهمة:
- **أقصى مدة:** أسبوعين للتقديم
- **التأخير:** عدم قبول الطلبات المتأخرة
"""

    def get_Cse_student_rights_response(self):
        return """
## 📝 شكاوى وحقوق الطالب

### 🗣️ تقديم الشكاوى:
- **التقديم الإلكتروني:** عبر بوابة الطالب
- **التقديم الورقي:** مكتب شؤون الطلاب

### 📋 حقوق الطالب الأساسية:
- **الحق في التعليم:** بيئة تعليمية مناسبة
- **الحق في التقييم العادل:** شفافية في الدرجات
- **الحق في الخصوصية:** حماية البيانات الشخصية
"""

    def get_Cse_student_activities_response(self):
        return """
## 🎯 الأنشطة الطلابية

### 👥 الأندية الطلابية:
- **النادي العلمي:** مشاريع بحثية ومسابقات
- **نادي التكنولوجيا:** ورش برمجة وتصميم
- **النادي الثقافي:** أنشطة ثقافية وفنية

### 🏆 المسابقات العلمية:
- **مسابقة البرمجة:** سنوية على مستوى الكلية
- **مسابقة الروبوتات:** مشاريع عملية
- **مسابقة الابتكار:** أفكار ومشاريع جديدة
"""



    def get_Cse_housing_response(self):
        return """
## 🏠 السكن الجامعي

### 📝 التقديم للسكن:
- **الفترة:** قبل بداية الفصل بشهر
- **الأولوية:** الطلاب من خارج المحافظة
- **الأوراق:** صورة شخصية، صورة البطاقة

"""

   

    def get_Cse_academic_support_response(self):
        return """
## 🎓 الدعم الأكاديمي

### 📞 خدمات الدعم المتاحة:
- **المرشدون الأكاديميون:** متخصصون لكل مستوى
- **مركز التعلم:** موارد ووسائل تعليمية
- **الاستشارات:** نفسية وتربوية

### 👨‍🏫 التواصل مع المرشد الأكاديمي:
- **المواعيد:** خلال ساعات العمل الرسمية
"""

    def get_Cse_research_response(self):
        return """
## 🔬 البحث العلمي

### 💡 المشاركة في الأبحاث:
- **المشاريع:** مع أعضاء هيئة التدريس
- **المؤتمرات:** محلية ودولية
- **المجموعات:** بحثية طلابية

"""

    

    # الدوال الأساسية من الكود الأصلي
    def get_Cse_warning_students_response(self):
        return """
⚠️ **الطلاب منخفضي المعدل (GPA < 2.0) - **

-**الحد الأقصى المطلق: 14 ساعة معتمدة فقط لكل فصل دراسي**
-**الحد الأدنى المسموح: 9 ساعات معتمدة**
-**Summer الترم الصيفي الحد الاقصى :8 ساعات**
### **موافقة المرشد الأكاديمي:**


**✅ الإجابة المباشرة: عند انخفاض المعدل (GPA < 2.0)، يمكنك تسجيل 14 ساعة معتمدة كحد أقصى فقط**
"""

    def get_Cse_gpa_response(self):
        return """
📊 **نظام المعدل التراكمي (GPA) - مفصل**

## 🎯 **طريقة الحساب:**
**المعادلة:** المعدل التراكمي = مجموع (الدرجة × ساعات المادة) ÷ مجموع الساعات الكلي

## 📈 **سلم التقديرات والنقاط:**
- **A+ → 100% to 97% --> 4.00**
- **A  → 96% to 93%  --> 4.00**
- **A- → 92% to 89%  --> 3.70**
- **B+ → 88% to 84%  --> 3.30**
- **B  → 83% to 80%  --> 3.00**
- **B- → 79% to 76%  --> 2.70**
- **C+ → 75% to 73%  --> 2.30**
- **C  → 72% to 70%  --> 2.00**
- **C- → 69% to 67%  --> 1.70**
- **D+ → 66% to 64%  --> 1.30**
- **D  → 63% to 60%  --> 1.00**
- **F  → Less than 60% --> 0.00**
- **P    → Pass              -->يرصد للطالب الناجح المسجل في المقررات ليس لها ساعات معتمدة**
- **F    → Fail              -->يرصد للطالب الناجح المسجل في المقررات ليس لها ساعات معتمدة**
- **W    → Withdrawn         -->يرصد للطالب المنسحب من مقرر بناءًا على طلبه**
- **FW   → Forced Withdrawn  -->يرصد للطالب المنسحب اجباريًا من مقرر ويحصل على 0.00 نقطة في هذا المقرر**
- **I    → Incomplete        -->يرصد للطالب الذي تعذر عليه استكمال متطلبات المقرر وتغيب في الامتحان النهائي بعذر مقبول وقدم طلب بذلك وتم قبوله طبقا للقواعد**
- **Abs  → Absent            -->يرصد للطالب المتغيب بدون عذر في الامتحان النهائي ويحصل علي 0.00 نقطة في هذا المقرر**
## 🎓 **الحدود الدنيا:**
- **للتخرج:** 2.0 من 4.0
- **للبقاء في القسم:** 1.5 من 4.0
"""

    def get_Cse_credits_response(self):
        return """
📚 **نظام الساعات المعتمدة - مفصل**

## 🎯 **الإجمالي المطلوب للتخرج:**
**160 ساعة معتمدة**

## 📊 **التوزيع التفصيلي:**
- **Proposal of Course Index (level 0) (32 Hrs)**
- **University (8 Hrs)**
- **Faculty (24 Hrs)**
- **Proposal of Course Index (level 1) (32 Hrs)**
- **University (2 Hrs)**
- **Faculty (8 Hrs)**
- **Department (22 Hrs)**
- **Proposal of Course Index (level 2) (32 Hrs)**
- **University (1 Hr)**
- **Faculty (4 Hrs)**
- **Department (27 Hrs)**
- **Proposal of Course Index (level 3) (32 Hrs)**
- **University (2 Hrs)**
- **Faculty (2 Hrs)**
- **Department (28 Hrs)**
- **Proposal of Course Index (level 4) (32 Hrs)** 
- **Department (32 Hrs)**
## ⚠️ **حدود التسجيل:**
- **(GPA>3.0):**مع تقديم طلب والموافقة عليه 21 ساعة كحد أقصى
- **(3.0>GPA>2.0):** 18 ساعة كحد أقصى
- **الطلاب تحت الإنذار (GPA<2.0):** 14 ساعة كحد أقصى
"""

    # باقي الدوال الأساسية...
    def get_Cse_graduation_response(self):
        return """
🎓 **شروط التخرج - مفصلة**

## ✅ **الشروط الأكاديمية:**
- **إكمال الساعات:** 160 ساعة معتمدة
- **المعدل التراكمي:** لا يقل عن 2.0
- **المتطلبات الإجبارية:** استكمال جميعها
- **مشروع التخرج:** اجتياز بنجاح
- اجتياز تدريب 1 & 2
"""

    def get_Cse_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
**Semester 2 (Spring)** 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
**Semester 3 (Fall)** 
- **Mathematics 3:** تحتاج Mathematics 2
- **Electrical Circuits 1:** تحتاج Physics 2
- **Electrical Measurements :** تحتاج Physics 2
- **Computer Programming :** تحتاج Computer Skills 
## Semester 4 ( Spring ) 
- **Mathematics 4:** تحتاج Mathematics 3 
- **Data Structures and algorithms:** تحتاج Computer Programming 
- **Electronics 2:** تحتاج Electronics 1 
- **Electrical Circuits 2:** تحتاج Electrical Circuits 1 
- **Electromagnetics:** تحتاج Physics 2 

## 🎯 **level 2:**
## Semester 5 (Fall)
- **Fundamentals of Artificial Intelligence:** تحتاج Computer Programming
- **Advanced Programming Language:** تحتاج Computer Programming
- **Signal and Systems:** تحتاج Mathematics 3 
## Semester 6 ( Spring )
- **Mathematics 5:** تحتاج Mathematics 4
- **Computer System Security:** تحتاج Data Structures and algorithms
- **Automatic Control Systems:** تحتاج Mathematics 3
- **Communication Theory:** تحتاج Signal and Systems 
- **Introduction to Machine Learning:** تحتاج Computer Programming

## 🎯 **level 3:**
## Semester 7 (Fall) 
- **Microprocessor:** تحتاج Digital and Logic Circuits 
- **Database Systems:** تحتاج Data Structures and algorithms 
- **Computer Networks:** تحتاج Data Structures and algorithms 
- **Introduction to Vision and Robotics:** تحتاج Automatic Control Systems 
## Semester 8 ( Spring ) 
- **Microcontrollers:** تحتاج Microprocessor 
- **Digital Signal Processing:** تحتاج Digital and Logic Circuits 
- **Computer Organization and Architecture:** تحتاج Signal and Systems
- **Software Engineering:** تحتاج Computer Programming 
- **Elective Course (Program Elective B):** تحتاج Advanced Programming Language

## 🎯 **level 4:**
## Semester 9 (Fall) 
- **Operating Systems:** تحتاج Computer Organization and Architecture
- **Embedded Systems:** تحتاج Microprocessor
- **Programmable logic controllers:** تحتاج Automatic Control Systems
## Semester 10 ( Spring )
- **Mobile Communications:** تحتاج Signal and Systems 
- **Cyber Security:** تحتاج Computer System Security
- **Project 2:** تحتاج Project 1

"""
    def get_ARC_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
##Semester 2 (Spring) 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
##Semester 3 (Fall) 
- **fundamentals of architecture design :** تحتاج Engineering Drawing and Projection
- **Visual Representation :** تحتاج Engineering Drawing and Projection
- **Structural Analysis 1  :** تحتاج Mechanics (1) 
##Semester 4 ( Spring ) 
- **Theory of Architecture 2  :**تحتاج Theory of Architecture 1 
- **Perspective & Model Making  :**تحتاج Visual Representation
- **Architecture Design Studio 1  :**تحتاج fundamentals of architecture design
- **Building Materials and Construction 2 :**تحتاج Building Materials and Construction 1  

## 🎯 **level 2:**
##Semester 5 (Fall)
- **History of Architecture 2  :**تحتاج History of Architecture 1 
- **Theory of Architecture 3 :**تحتاج Theory of Architecture 2 
- **Architecture Design Studio 2   :**تحتاج MArchitecture Design Studio 1 
- **Building Materials and Construction 3  :**تحتاج Building Materials and Construction 2   
- **Environmental control  :**تحتاج Introduction to sustainability 
##Semester 6 ( Spring )
- **Architecture Design Studio 3   :**تحتاج Architecture Design Studio 2
- **Working Design 1  :**تحتاج Building Materials and Construction 3 
- **Reinforced Concrete & Foundation  :**تحتاج Structural Analysis 1 
- **Daylight & Illumination studies  :**تحتاج Environmental control 

## 🎯 **level 3:**
##Semester 7 (Fall) 
- **Environmental design Studio 1   :**تحتاج Architecture Design Studio 3
- **Working Design 2  :**تحتاج Working Design 1  
- **Environmental Rating Systems  :**تحتاج Environmental control 
- **Steel Structures :**تحتاج Structural Analysis 1 
- **Computer Modeling 2  :**تحتاج Computer Modeling 1 
##Semester 8 ( Spring ) 
- **Environmental design Studio 2  :**تحتاج Environmental design Studio 1
- **Estimation, Costing, and Specifications :**تحتاج Working Design 1 
- **Sustainability in Urbanism  :**تحتاج Environmental Rating Systems
- **Computer Modeling 3 :**تحتاج Computer Modeling 2 

## 🎯 **level 4:**
##Semester 9 (Fall) 
- **Environmental design Studio 3  :**تحتاج Environmental design Studio 2 
- **Project 1  :**تحتاج Environmental design Studio 2 
##Semester 10 ( Spring )
- **Project 2  :**تحتاج Project 1 
- **Statistics and Probability Theory  :**تحتاج Computer System Security
"""
    def get_mechatronics_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
##Semester 2 (Spring) 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
##Semester 3 (Fall) 
- **Mathematics 3:** تحتاج Mathematics 2
- **Kinematics of Mechanisms and Robots :** تحتاج Mechanics 2 
- **Electrical Circuits :** تحتاج Physics 2
- **Mechanical Drawing Assembly and CAD :** تحتاج Engineering Drawing and Projection 
- **Manufacturing Processes and Engineering Metrology :**تحتاج  Principles of Manufacturing Engineering 
##Semester 4 ( Spring ) 
- **Mathematics 4  :**تحتاج Mathematics 3 
- **Material Science and Testing  :**تحتاج Manufacturing Processes and Engineering Metrology
- **Design of Machines Elements  :**تحتاج Mechanical Drawing Assembly and CAD
- **Strength of Materials and Stress Analysis :**تحتاج Mechanics 1

## 🎯 **level 2:**
##Semester 5 (Fall)
- **Mechanical Design :**تحتاج Design of Machines Elements
- **Signals and Systems :**تحتاج Mathematics 3 
##Semester 6 ( Spring )
- **Dynamics of Mechanisms and Robots  :**تحتاج Kinematics of Mechanisms and Robots
- **Electrical Machines and Industrial Electronics :**تحتاج Electrical Circuits 
- **Microprocessors  :**تحتاج Digital and Logic Circuits 
- **Robotics Engineering :**تحتاج Mechanical Design 

## 🎯 **level 3:**
##Semester 7 (Fall) 
- **Electronic Circuits :**تحتاج Electrical Circuits   
- **CNC Machines and Material Cutting Processes :**تحتاج Mechanical Design 
- **Modeling and Simulation of Mechanical Systems :**تحتاج Mechanical Vibrations
##Semester 8 ( Spring ) 
- **Measurement Techniques and Codes :**تحتاج Manufacturing Processes and Engineering Metrology
- **CAD/CAM :**تحتاج CNC Machines and Material Cutting Processes  
- **Sensors and Actuators :**تحتاج Automatic Control and Applications  
- **Power Electronics :**تحتاج Electrical Circuits  

## 🎯 **level 4:**
##Semester 9 (Fall) 
- ** Programmable Logic Controller (PLC) :**تحتاج Digital and Logic Circuits 
- **Embeded System :**تحتاج Microprocessor
##Semester 10 ( Spring )
- ** Design of Mechatronic Systems :**تحتاج Introduction to Mechatronics 
- **Microcontrollers :**تحتاج Microprocessor
- **Motion and Control Servo Systems :**تحتاج Automatic Control and Applications
- **Digital Signal Processing :**تحتاج Signals and Systems
- **Project 2 :**تحتاج Project 1

"""
    def get_ai_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
##Semester 2 (Spring) 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
##Semester 3 (Fall) 
- **Mathematics 3:** تحتاج Mathematics 2
- **Electrical Circuits 1:** تحتاج Physics 2
- **Electrical Measurements :** تحتاج Physics 2
- **Computer Programming  :** تحتاج Computer Skills 
##Semester 4 ( Spring ) 
- **Mathematics 4  :**تحتاج Mathematics 3 
- **Data Structures and algorithms :**تحتاج Computer Programming 
- **Electronics 2  :**تحتاج Electronics 1 
- **Electrical Circuits 2 :**تحتاج Electrical Circuits 1 
- **Advanced Programming Languages  :**تحتاج Computer Programming 

## 🎯 **level 2:**
##Semester 5 (Fall)
- **Introduction to Machine Learning :**تحتاج Computer Programming
- **Fundamentals of Artificial Intelligence :**تحتاج Computer Programming
- **Signal and Systems  :**تحتاج Mathematics 3 
##Semester 6 ( Spring )
- **Mathematics 5  :**تحتاج Mathematics 4
- **Automatic Control Systems :**تحتاج Mathematics 3
- **Communication Theory :**تحتاج Signal and Systems 
- **Computer Organization and Architecture :**تحتاج Digital and Logic Circuits
- **Computer System Security :**تحتاج Data Structures and Algorithms


## 🎯 **level 3:**
##Semester 7 (Fall) 
- **Microprocessor  :**تحتاج Digital and Logic Circuits 
- **Introduction to Vision and Robotics :**تحتاج Automatic Control Systems 
- **Learning from Data :**تحتاج ?????
- **Operating Systems :**تحتاج Computer Organization and Architecture
- **Multi-agent Systems Design :**تحتاج Computer Organization and Architecture
##Semester 8 ( Spring ) 
- **Digital Signal Processing :**تحتاج Digital and Logic Circuits 
- **Introduction to Natural Language Processing :**تحتاج Introduction to Vision and Robotics
- **Elective 1 (Discipline) :**تحتاج Data Structures and Algorithms
- **Computer Networks :**تحتاج Data Structures and Algorithms
- **Big Data Analysis :**تحتاج Learning from Data

## 🎯 **level 4:**
##Semester 9 (Fall) 
- **Embedded Systems :**تحتاج Microprocessor
##Semester 10 ( Spring )
- **Mobile Communications :**تحتاج Signal and Systems 
- **Advanced Vision and Robotics :**تحتاج Introduction to Vision and Robotics
- **Project 2 :**تحتاج Project 1

"""
    def get_civil_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
##Semester 2 (Spring) 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
##Semester 3 (Fall) 
- **Mathematics 3:** تحتاج Mathematics 2
- **Structural Analysis 1:** تحتاج Mechanics 1
- **Civil Drawing :** تحتاج Engineering Drawing and Projection
##Semester 4 ( Spring ) 
- **Mathematics 4  :**تحتاج Mathematics 3 
- **Structure Mechanics :**تحتاج Structural Analysis 1
- **Engineering Surveying 2  :**تحتاج Engineering Surveying 1

## 🎯 **level 2:**
##Semester 5 (Fall)
- **Structural Analysis 2 :**تحتاج Structural Analysis 1
- **Concrete Technology :**تحتاج Behavior of Materials
##Semester 6 ( Spring )
- **Structural Analysis 3  :**تحتاج Structural Analysis 2
- **Computer Applications in Civil Engineering :**تحتاج Structural Analysis 1
- **Design of Concrete Structures 1 :**تحتاج Structural Analysis 1 & Concrete Technology
- **Design of Steel Structures 1 :**تحتاج Structure Mechanics &  Structural Analysis 2
- **Irrigation and Drainage Engineering :**تحتاج Hydraulics 1 & Hydrology

## 🎯 **level 3:**
##Semester 7 (Fall) 
- **Design of Concrete Structures 2  :**تحتاج Design of Concrete Structures 1
- **Design of Steel Structures 2 :**تحتاج Design of Steel Structures 1
- **Hydraulics 2 :**تحتاج Hydraulics 1 
##Semester 8 ( Spring ) 
- **Design of Concrete Structures 3 :**تحتاج Design of Concrete Structures 2
- **Sanitary Engineering :**تحتاج Hydraulics 2
- **Foundations Engineering 1 :**تحتاج Design of Concrete Structures 1 & Soil Mechanics

## 🎯 **level 4:**
##Semester 9 (Fall) 
- **Foundations Engineering 2 :**تحتاج Foundations Engineering 1
- **Design of Irrigation Structures :**تحتاج Irrigation and Drainage Engineering &  Hydraulics 2
##Semester 10 ( Spring )
- **Project 2 :**تحتاج Project 1

"""
    def get_medical_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
##**Semester 2 (Spring)** 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
##**Semester 3 (Fall)** 
- **Mathematics 3:** تحتاج Mathematics 2
- **Strength of Materials and Stress Analysis:** تحتاج Mechanics 1 
- **Electrical Circuits 1 :** تحتاج Physics 2
##**Semester 4 ( Spring )** 
- **Mathematics 4  :**تحتاج Mathematics 3 
- **Data Structures and algorithms :**تحتاج Computer Programming 
- **Computer Programming :**تحتاج Computer Skills 
- **Electromagnetics :**تحتاج Mathematics 3 & Physics 2 

## 🎯 **level 2:**
##Semester 5 (Fall)
- **Numerical Methods and Operation Research  :**تحتاج Mathematics 2
- **Biochemistry  :**تحتاج Organic Chemistry
- **Automatic Control Systems  :**تحتاج Mathematics 3
- **Electronics 2  :**تحتاج Electronics 1 
##Semester 6 ( Spring )
- **Mathematics 5  :**تحتاج Mathematics 4
- **Introduction to Physiology  :**تحتاج Introduction to Anatomy 
- **Biomedical Sensors and Actuators :**تحتاج Electronics 1
- **Measurements and Instrumentation :**تحتاج Electronics 2 
- **Signals and Systems  :**تحتاج Mathematics 3 

## 🎯 **level 3:**
##Semester 7 (Fall) 
- **Microbiology   :**تحتاج Biochemistry
- **Biomedical Instrumentation  :**تحتاج Measurements and Instrumentation
- **Biomaterials Properties :**تحتاج Strength of Materials and Stress Analysis 
- **Digital Signal Processing  :**تحتاج  Signals and Systems

##Semester 8 ( Spring ) 
- **Medical Equipment 1  :**تحتاج Biomedical instrumentation 
- **Database Systems  :**تحتاج Data Structures and Algorithms 

## 🎯 **level 4:**
##Semester 9 (Fall) 
- **Applied Digital Image Processing  :**تحتاج Signals and Systems
- **Medical Equipment 2  :**تحتاج Medical Equipment 1
##Semester 10 ( Spring )
- **Medical Imaging  :**تحتاج SApplied Digital Image Processing  
- **Project in Biomedical Engineering (2) :**تحتاج Project in Biomedical Engineering (1) 
- **Embedded Systems :**تحتاج Automatic Control Systems 
"""
    def get_communications_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
##**Semester 2 (Spring)** 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
##**Semester 3 (Fall)** 
- **Mathematics 3:** تحتاج Mathematics 2
- **Electrical Circuits 1:** تحتاج Physics 2
- **Electrical Measurements :** تحتاج Physics 2
- **Computer Programming  :** تحتاج Computer Skills 
##**Semester 4 ( Spring )** 
- **Mathematics 4  :**تحتاج Mathematics 3 
- **Data Structures and algorithms :**تحتاج Computer Programming 
- **Electronics 2  :**تحتاج Electronics 1 
- **Electrical Circuits 2 :**تحتاج Electrical Circuits 1 
- **Electromagnetics  :**تحتاج Physics 2 

## 🎯 **level 2:**
##Semester 5 (Fall)
- **Electronic Devices :**تحتاج Electronics 2
- **Signal and Systems :**تحتاج Mathematics 3
##Semester 6 ( Spring )
- **Mathematics 5  :**تحتاج Mathematics 4
- **Computer System Security :**تحتاج Data Structures and algorithms
- **Automatic Control Systems :**تحتاج Mathematics 3
- **Communication Theory :**تحتاج Signal and Systems 
- **Introduction to Machine Learning :**تحتاج Computer Programming

## 🎯 **level 3:**
##Semester 7 (Fall) 
- **Microprocessor  :**تحتاج Digital and Logic Circuits 
- **Information Security :**تحتاج Computer System Security
- **Digital Communications :**تحتاج Communication Theory
- **Introduction to Vision and Robotics :**تحتاج Automatic Control Systems 
- **Electronics Engineering :**تحتاج Electronics 2
##Semester 8 ( Spring ) 
- **Electromagnetic Waves :**تحتاج Electromagnetics
- **Digital Signal Processing :**تحتاج Digital and Logic Circuits 
- **Optoelectronics :**تحتاج Electronics 2
- **Antenna and Wave Propagation :**تحتاج Electromagnetics

## 🎯 **level 4:**
##Semester 9 (Fall) 
- **Microwave Engineering and Arrays :**تحتاج Electromagnetics
- **Optical Communications :**تحتاج Optoelectronics
- **Embedded Systems :**تحتاج Microprocessor
- **AI in Communication Systems :**تحتاج Fundamentals of Artificial Intelligence
##Semester 10 ( Spring )
- **Mobile Communications :**تحتاج Signal and Systems 
- **Integrated Circuits Design :**تحتاج Electronics Engineering
- **Project 2 :**تحتاج Project 1

"""
    def get_architecture_prerequisites0_response(self):
        return """
🔗 **نظام المتطلبات السابقة - مفصل**

## 📋 **أنواع المتطلبات:**
- **المتطلبات السابقة:** مواد يجب اجتيازها قبل التسجيل
- **المتطلبات المرافقة:** مواد يجب/يمكن تسجيلها معاً

## 🎯 **level 0:**
##**Semester 2 (Spring)** 
- **Mathematics 2:** تحتاج Mathematics 1
- **Physics 2:** تحتاج Physics 1
- **Mechanics 2 :** تحتاج Mechanics 1

## 🎯 **level 1:**
##**Semester 3 (Fall)** 
- **fundamentals of architecture design:** تحتاج Engineering Drawing and Projection
- **Visual Representation:** تحتاج Engineering Drawing and Projection
- **Structural Analysis 1 :** تحتاج Mechanics (1)
##**Semester 4 ( Spring )** 
- **Theory of Architecture 2 :**تحتاج Theory of Architecture 1
- **Perspective and Model Making:**تحتاج Visual Representation 
- **Architecture Design Studio 1  :**تحتاج fundamentals of architecture design
- **Building Materials and Construction 2:**تحتاج Building Materials and Construction 1

## 🎯 **level 2:**
##Semester 5 (Fall)
- **History of Architecture 2 :**تحتاج History of Architecture 1
- **Theory of Architecture 3:**تحتاج Theory of Architecture 2
- **Architecture Design Studio 2 :**تحتاج Architecture Design Studio 1
- **Building Materials and Construction 3 :**تحتاج Building Materials and Construction 2
##Semester 6 ( Spring )
- **Architecture Design Studio 3  :**تحتاج Architecture Design Studio 2
- **Working Design 1 :**تحتاج Building Materials and Construction 3
- **Reinforced Concrete and Foundation :**تحتاج Structural Analysis 1

## 🎯 **level 3:**
##Semester 7 (Fall) 
- **Architecture Design Studio 4  :**تحتاج Architecture Design Studio 3
- **Working Design 2 :**تحتاج Working Design 1
- **Landscape Design :**تحتاج Introduction to Urban Planning
- **Steel Structures :**تحتاج Structural Analysis 1
- **Computer Modeling 2:**تحتاج Computer Modeling 1
##Semester 8 ( Spring ) 
- **Architecture Design Studio 5 :**تحتاج Architecture Design Studio 4
- **Estimation, Costing, and Specifications :**تحتاج Working Design 1
- **Urban Design :**تحتاج Landscape Design
- **Field Training 2 :**تحتاج XXX 291

## 🎯 **level 4:**
##Semester 9 (Fall) 
- **Architecture Design Studio 6:**تحتاج Architecture Design Studio 5
- **Project 1 :**تحتاج Architecture Design Studio 5
##Semester 10 ( Spring )
- **Project 2:**تحتاج Project 1
- **Water Supply and Building Sanitation :**تحتاج Estimation, Costing, and Specifications

"""
    def get_Cse_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص العام 61 ساعة **
**Electrical**
-**EPE 115 Electrical Circuits    
-**EPE 341 Electrical Machines and Industrial Electronics   
-**EPE 345 Power Electronics  

**Communication**
-**ECE 111 Electronics 
-**ECE 112 Electronics  
-**ECE 221 Signal and Systems  
-**ECE 231 Communication Theory 
-**ECE 321 Digital Signal Processing  
-**ECE 432 Mobile Communications

**Atificial Intelligence**
-**AIE 211 Fundamentals of Artificial Intelligence
-**AIE 221 Introduction to Machine Learning  
-**AIE 341 Introduction to Vision and Robotics

**Computer**
-**CSE 222 Computer System Security  
-**CSE 211 Automatic Control Systems 
-**CSE 231 Digital and Logic Circuits 
-**CSE 333 Microprocessor  
-**CSE 121 Computer Programming 
-**CSE 122 Data Structures and algorithms 
-**CSE 412 Embedded Systems
"""

    def get_communications_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص العام 61 ساعة **
**Basic Science**
-**BAS 212 Mathematics 5 

**Electrical**
-**EPE 112 Electrical Circuits 1  
-**EPE 114 Electrical Circuits 2  
-**EPE 113 Electrical Measurements  
-**EPE 151 Electromagnetics  

**Communication**
-**ECE 111 Electronics 
-**ECE 112 Electronics  
-**ECE 221 Signal and Systems  
-**ECE 231 Communication Theory 
-**ECE 321 Digital Signal Processing  
-**ECE 432 Mobile Communications

**Atificial Intelligence**
-**AIE 211 Fundamentals of Artificial Intelligence
-**AIE 221 Introduction to Machine Learning  
-**AIE 341 Introduction to Vision and Robotics

**Computer**
-**CSE 222 Computer System Security  
-**CSE 211 Automatic Control Systems 
-**CSE 231 Digital and Logic Circuits 
-**CSE 333 Microprocessor  
-**CSE 121 Computer Programming 
-**CSE 122 Data Structures and algorithms 
-**CSE 412 Embedded Systems

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص الدقيق 30 ساعة **
-** ECE 441 Microwave Engineering and Arrays (3 Hrs)
-** ECE 411 Integrated Circuits Design (3 Hrs)
-** ECE 342 Antenna and Wave Propagation (3 Hrs) 
-** ECE 331 Digital Communications (3 Hrs) 
-** ECE 211 Electronic Devices (3 Hrs)
-** ECE 312 Optoelectronics (3 Hrs)
-** ECE 431 Optical Communications (3 Hrs) 
-** ECE 351 Information Security (2 Hrs)
-** ECE 451 AI in Communication Systems (2 Hrs)
-** ECE 311 Electronics Engineering (2 Hrs)
-** ECE 341 Electromagnetic Waves (3 Hrs)
"""
    def get_ai_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص العام 61 ساعة **
**Basic Science**
-**BAS 212 Mathematics 5 

**Electrical**
-**EPE 112 Electrical Circuits 1  
-**EPE 114 Electrical Circuits 2  
-**EPE 113 Electrical Measurements   

**Communication**
-**ECE 111 Electronics 
-**ECE 112 Electronics  
-**ECE 221 Signal and Systems  
-**ECE 231 Communication Theory 
-**ECE 321 Digital Signal Processing  
-**ECE 432 Mobile Communications

**Atificial Intelligence**
-**AIE 211 Fundamentals of Artificial Intelligence
-**AIE 221 Introduction to Machine Learning  
-**AIE 341 Introduction to Vision and Robotics

**Computer**
-**CSE 121 Computer Programming
-**CSE 221 Advanced Programming Languages
-**CSE 122 Data Structures and algorithms
-**CSE 211 Automatic Control Systems
-**CSE 231 Digital and Logic Circuits 
-**CSE 333 Microprocessor    
-**CSE 412 Embedded Systems
-**CSE 222 Computer System Security

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص الدقيق 24 ساعة **
-** AIE 321 Learning from Data
-** AIE 322 Big Data Analysis
-** AIE 351 Introduction to Natural Language Processing
-** AIE 371 Multi Agent Systems Design
-** CSE 331 Computer Organization and Architecture
-** CSE 431 Operating Systems
-** CSE 332 Computer Networks
-** AIE 461 Pattern Recognition
-** AIE 441 Advanced Vision and Robotics

"""
    def get_ARC_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 **المقررات الاجبارية لمتطلبات التخصص العام 68 ساعة **
** Civil Engineering Department**
- ** CIV 111 Structural Analysis 1
- ** CIV 141 Behavior of Materials 
- ** CIV 222 Reinforced Concrete & Foundation
- ** CIV 232 Steel Structures 
- **  Engineering Surveying for architect

**Architectural Engineering Department**
-**ARC 112 Visual Representation 
-**ARC 113 Perspective & Model Making 
-**ARC 121 fundamentals of architecture design
-**ARC 122 Architecture Design Studio 1 
-**ARC 221 Architecture Design Studio 2 
-**ARC 222 Architecture Design Studio 3 
-**ARC 131 Building Materials and Construction 1
-**ARC 132 Building Materials and Construction 2 
- **ARC 231 Building Materials and Construction 3
- **ARC 232 Working Design 1 
- **ARC 331 Working Design 2 
- **ARC 332 Estimation, Costing, and Specifications 
- **ARC 141 History of Architecture 1 
- **ARC 142 Theory of Architecture 1 
- **ARC 143 Theory of Architecture 2 
- **ARC 241 History of Architecture 2 
- **ARC 242 Theory of Architecture 3
- **ARC 251 Computer Modeling 1 
- **ARC 351 Computer Modeling 2 
- **ARC 352 Computer Modeling 3 
- **ARC 262 Introduction to Urban Planning 

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص الدقيق 37 ساعة **
-** SAE 181 Introduction to sustainability
-** SAE 281 Environmental control
-** SAE 282 Daylight & Illumination studies
-** SAE 321 Environmental design Studio 1
-** SAE 322 Environmental design Studio 2
-** SAE 421 Environmental design Studio 3
-** SAE 381 Environmental Rating Systems
-** SAE 382 Sustainability in Urbanism
-** SAE 353 Embedded systems in sustainable architectur

"""
    def get_civil_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص العام 61 ساعة **
**Architecture**
-**ARC 133 Building Materials and Construction

**Civil**
-**CIV 111 Structural Analysis 1  
-**CIV 112 Structure Mechanics  
-**CIV 141 Behavior of Materials 
-**CIV 161 Engineering Surveying 1
-**CIV 162 Engineering Surveying 2 
-**CIV 171 Hydraulics 1 
-**CIV 181 Civil Drawing
-**CIV 211 Structural Analysis 2 
-**CIV 212 Structural Analysis 3  
-**CIV 213 Computer Applications in Civil Engineering
-**CIV 221 Design of Concrete Structures 1
-**CIV 231 Design of Steel Structures 1 
-**CIV 241 Concrete Technology
-**CIV 251 Soil Mechanics 
-**CIV 281 Hydrology
-**CIV 282 Irrigation and Drainage Engineering 
-**CIV 321 Design of Concrete Structures 2  
-**CIV 351 Foundations Engineering 1
-**CIV 361 Quantities Surveying and Costs Estimating
-**CIV 371 Hydraulics 2
-**CIV 461 Construction Project Management

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص الدقيق 24 ساعة **
-** CIV 322 Design of Concrete Structures 3
-** CIV 331 Design of Steel Structures 2
-** CIV 362 Transportation and Traffic Engineering
-** CIV 363 Highway and Airport Engineering
-** CIV 364 Sanitary Engineering
-** CIV 451 Foundations Engineering 2
-** CIV 462 Construction Equipment and Methods
-** CIV 481 Design of Irrigation Structures


"""
    def get_mechatronics_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص العام 61 ساعة ** 

**Electrical**
-**EPE 115 Electrical Circuits
-**EPE 341 Electrical Machines and Industrial Electronics
-**EPE 345 Power Electronics

**Design & Manufacturing Engineering Department DME**
-**DME 112 Mechanical Drawing Assembly and CAD
-**DME 121 Manufacturing Processes and Engineering Metrology
-**DME 131 Material Science and Testing
-**DME 113 Strength of Materials and Stress Analysis
-**DME 311 Modeling and Simulation of Mechanical Systems
-**DME 111 Kinematics of Mechanisms and Robots
-**DME 212 Dynamics of Mechanisms and Robots
-**DME 114 Design of Machines Elements
-**DME 211 Mechanical Design
-**DME 221 Mechanical Vibrations
-**DME 322 Automatic Control and Applications
-**DME 323 Measurement Techniques and Codes

**Mechanical Power Engineering Department MPE**
-**MPE 143 Thermodynamics
-**MPE 241 Fluid Mechanics
-**MPE 242 Heat Transfer 

**Computer & Systems Engineering Department CSE **
-**CSE 231 Digital and Logic Circuits
-**CSE 122 Data Structures and Algorithms
-**CSE 333 Microprocessors

**Mechatronics Engineering Department MET**
-**MET 451 Programmable Logic Controller(PLC)

** Electronics & Communications Engineering Department ECE**
-**ECE 322 Electronic Circuits

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص الدقيق 30 ساعة **
** Electronics & Communications Engineering Department ECE**
-**ECE 221 Signals and Systems
-**ECE 321 Digital Signal Processing

**Mechatronics Engineering Department MET**
-**MET 452 Introduction to Mechatronics
-**MET 361 Sensors and actuators
-**MET 251 Robotics Engineering
-**MET 454 Design of Mechatronic Systems
-**MET 455 Motion and Control Servo Systems

**Design & Manufacturing Engineering Department DME**
-**DME 321 CNC Machines and Material Cutting Processes
-**DME 312 CAD/CAM

**Computer & Systems Engineering Department CSE **
-**CSE 412 Embeded System
-**CSE 311 Microcontrollers

"""
    def get_medical_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص العام 61 ساعة ** 
**Basic Sciences Department BAS **
-**BAS 212 Mathematics 5

**Electrical Power Engineering Department EPE **
-**EPE 112 Electrical Circuits 1
-**EPE 151 Electromagnetics

**Design & Manufacturing Engineering Department DME**
-**DME 113 Strength of Materials and Stress Analysis

**Computer & Systems Engineering Department CSE **
-**CSE 121 Computer Programming
-**CSE 122 Data Structure and Algorithms
-**CSE 211 Automatic Control systems
-**CSE 231 Digital and Logic Circuits
-**CSE 321 Database Systems
-**CSE 412 Embedded Systems

** Electronics & Communications Engineering Department ECE**
-**ECE 111 Electronics 1
-**ECE 112 Electronics 2
-**ECE 221 Signals and Systems

**Biomedical Engineering Department BME **
-**BME 121 Introduction to Anatomy
-**BME 231 Biomedical Sensors and Actuators
-**BME 232 Measurements and Instrumentation
-**BME 331 Biomedical Instrumentation
-**BME 332 Bioinformatics
-**BME 341 Biomaterials Properties
-**BME 431 Applied Digital Image Processing

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص الدقيق 24 ساعة **
**Biomedical Engineering Department BME **
-**BME 111 Organic Chemistry
-**BME 211 Biochemistry
-**BME 221 Introduction to Physiology
-**BME 311 Microbiology
-**BME 351 Clinical Engineering
-**BME 352 Medical Equipment 1
-**BME 432 Medical Imaging
-**BME 451 Medical Equipment 2

"""
    def get_architecture_compulsory_courses_response(self):
        return """
📖 **المواد الإجبارية - مفصلة**

## 🎯 ** المقررات الاجبارية لمتطلبات التخصص 96 ساعة ** 
**Civil Engineering Department CIV  **
-**CIV 111 Structural Analysis 1
-**CIV 163 Engineering Surveying for architect
-**CIV 141 Behavior of Materials
-**CIV 222 Reinforced Concrete and Foundation
-**CIV 232 Steel Structures

** Architectural Engineering Department ARC **
-**ARC 112 Visual Representation
-**ARC 113 Perspective and Model Making
-**ARC 121 fundamentals of architecture design
-**ARC 122 Architecture Design Studio 1
-**ARC 221 Architecture Design Studio 2
-**ARC 222 Architecture Design Studio 3
-**ARC 321 Architecture Design Studio 4
-**ARC 322 Architecture Design Studio 5
-**ARC 421 Architecture Design Studio 6
-**ARC 131 Building Materials and Construction 1
-**ARC 132 Building Materials and Construction 2
-**ARC 231 Building Materials and Construction 3
-**ARC 232 Working Design 1
-**ARC 331 Working Design 2
-**ARC 332 Estimation, Costing, and Specifications
-**ARC 431 Water Supply and Building Sanitation
-**ARC 141 History of Architecture 1
-**ARC 142 Theory of Architecture 1
-**ARC 143 Theory of Architecture 2
-**ARC 241 History of Architecture 2
-**ARC 242 Theory of Architecture 3
-**ARC 251 Computer Modeling 1
-**ARC 351 Computer Modeling 2
-**ARC 261 History and Theory of Urban Planning
-**ARC 262 Introduction to Urban Planning
-**ARC 361 Landscape Design
-**ARC 362 Urban Design
-**ARC 471 Interior Design
-**ARC 461 Architectural and Urban Legalization
-**ARC 491 Project 1
-**ARC 491 Project 1

**Sustainable Architectural Engineering Department SAE **
-**SAE 181 Introduction to sustainability

"""
    def get_ARC_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 18 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### **Group A select 6 Hrs:**
- ARC x61 Landscape Design(3Hrs)
- ARC x62 Urban Design (3Hrs)
- ARC x51 Geometric Modeling  (3Hrs)
- ARC x52 Smart Building Information Systems(3Hrs)

### **Group B select 3 Hrs:**
- ARC x71 Interior Architecture Design (3 Hrs)
- ARC x53 Digital Design & Fabrication (3 Hrs)


### 
"""
    def get_architecture_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 18 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### **Group A select 12 Hrs:**
- ARC x72 Lighting and Ventilation (3Hrs)
- ARC x51 Geometric Modeling (3Hrs)
- ARC x63 Residential planning and Housing  (3Hrs)
- ARC x64 Urban Renewal (3Hrs)
- ARC x52 Smart Building Information Systems (3 Hrs)
- ARC x81 Conservation of Urban Heritage (3 Hrs)

### **Group B select 6 Hrs:**
- SAE x31 Advanced Building Systems Integration (2 Hrs)
- SAE x41 Vernacular Architecture (2 Hrs)
- SAE x42 Introduction to Shape Grammars (2 Hrs)
- SAE x51 Acoustics design (2 Hrs)
- SAE x81 Sustainable and Smart Architecture (2 Hrs)
- SAE x82 Sustainable Building Construction and Materials (2 Hrs)
- SAE x83 Thermal Comfort Measures (2 Hrs)
- SAE x84 Thermal properties of materials (2 Hrs)


### 
"""
    def get_mechatronics_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 12 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### **select 12 Hrs:**
- CSE 341 Software Engineering (3Hrs)
- MET 457 Bio-mechatronics (3Hrs)
- MET 458 Automotive Mechatronics  (3Hrs)
- AIE 411 Artificial Intelligence and its Applications (3Hrs)
- DME 421 Non-Traditional Machining Processes (3 Hrs)
- MPE 442 Design of Renewable Energy Systems  (3 Hrs)
- MET 471 Micro and Nano-Electromechanical Systems  (3 Hrs)
- MET 462 Mobile and Bipedal Robots (3 Hrs)
- MPE 443 Turbomachinery and Applications (3 Hrs) 
- MPE 441 Hydraulic and Pneumatic Control Systems  (3 Hrs) 
- CSE 324 Advanced Programming Techniques  (3 Hrs) 
 
###  
"""
    def get_medical_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 18 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### **select 12 Hrs:**
- BME x11 Medical and Pharmaceutical Procedures(3Hrs)
- BME x12 Industrial Pharmacy (3Hrs)
- BME x21 Public Health  (3Hrs)
- BME x22 Clinical Pathologys (3Hrs)
- BME x23 Rehabilitation Engineering (3 Hrs)
- BME x32 Internet of Medical Things (IoMT)  (3 Hrs)
- BME x33 Pattern Recognition and Classification  (3 Hrs)
- BME x34 Introduction to Deep Learning (3 Hrs)
- BME x35 Medical Decision Support Systems (MDSS) (3 Hrs) 
- BME x36 Healthcare Information Systems (HCIS) (3 Hrs) 
- BME x41 Introduction to Nanotechnology  (3 Hrs) 
- BME x42 Fluid Flow in Bio-systems  (3 Hrs)
- BME x51 Electronic Medical Records  (3 Hrs)
 
###  
"""
    def get_Cse_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 17 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### **Group A (select 2Hrs):**
- Computer Graphics  (2Hrs)
- Digital Image Processing  (2Hrs)
- Cloud Computing  (2Hrs)
- Geographic Information Systems (2Hrs)

### **Group B (select 15Hrs):**
- Web Programming Development (3 Hrs)
- Advanced Database systems  (3 Hrs)
- Distributed Systems  (3 Hrs)
- Real-time operating systems (3 Hrs)
- Computer Game Architecture and Virtual Reality  (3 Hrs) 
- Internet of Things  (3 Hrs) 
- Fuzzy and predictive control systems  (3 Hrs) 
- Data Mining  (3 Hrs) 
- Advanced Natural Language Processing  (3 Hrs)
- Deep learning  (3 Hrs)
- Bioinformatics  (3 Hrs)   
"""
   ## def get_ai_elective_courses_response(self):
   ##     return """
#🎯 #**المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 18 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### **(select 18 Hrs):**
#-** Advanced Natural Language Processing  (3 Hrs)
#-** Intelligent Decision Support Systems  (3 Hrs)
#-** Advanced Data Modeling (3 Hrs)
#-** Advanced Data Modeling (3 Hrs)
#-** Advanced Cybersecurity (3 Hrs)
#-** Artificial Intelligence and Games (3 Hrs)
#-** Artificial Knowledge Representation (3 Hrs)
#-** Advanced Machine Learning (3 Hrs)
#-** Artificial Intillegence in Smart Cities (3 Hrs)
#"""
    def get_communications_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 18 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### ** (Select 12):**
-**ECE X12 VLSI Technology
-**ECE X13 Medical Electronics
-**ECE X14 Automotive Electronics
-**ECE X33 Satellite Communications
-**ECE X34 RADAR Systems
-**ECE X35 Telephony Systems
-**ECE X21 Acoustics
-**ECE X52 Information and Coding Theory

"""
    def get_civil_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 18 ساعة اختيارية**

## 🔍 **مجموعات المواد الاختيارية:**

### **Group A (select 12 Hrs):**
-**CIV 411 Structural Dynamics (3 Hrs)
-**CIV 421 Design of Concrete Structures 4 (3 Hrs)
-**CIV 422 High Rise Buildings (3 Hrs)
-**CIV 431 Design of Steel Bridges (3 Hrs)
-**CIV 441 Repair and Strengthening of Structures (3 Hrs)
-**CIV 452 Soil Improvement (3 Hrs)
-**CIV 463 Maps, GIS and Remote Sensing (3 Hrs)
-**CIV 464 Hydrographic surveying (3 Hrs)
-**CIV 465 Railway Engineering (3 Hrs)
-**CIV 472 Harbor and Coastal Engineering (3 Hrs)
-**CIV 484 Dams Engineering (3 Hrs)
-**CIV 485 Modern Irrigation Systems (3 Hrs)
-**CIV 486 Water Resources Management (3 Hrs)

### **Group B (select 4 Hrs):**
-**CIV 323 Earthquake Engineering (2 Hrs)
-**CIV 332 Design of Composite Steel Structures (2 Hrs)
-**CIV 341 Quality Control in Structures (2 Hrs)
-**CIV 352 Engineering Geology (2 Hrs)
-**CIV 365 Pavement Design (2 Hrs)
-**CIV 366 Maintenance of Highways (2 Hrs)
-**CIV 367 Environmental Engineering (2 Hrs) 

### **Group C (select 2 Hrs):**
-**CIV 471 Applied Hydraulics (2 Hrs)
-**CIV 482 Groundwater Hydrology (2 Hrs)
-**CIV 483 Computer Applications in Water Resources (2 Hrs)

"""
    def get_ai_elective_courses_response(self):
        return """
🎯 **المواد الاختيارية - مفصلة**

## 📚 **الساعات المطلوبة: 18 ساعة اختيارية**
-**AIE x81 Advanced Natural Language Processing 
-**AIE x83 Intelligent Decision Support Systems 
-**AIE x84 Advanced Data Modeling 
-**AIE x54 Advanced Cybersecurity  
-**AIE x55 Artificial Intelligence and Games  
-**AIE x61 Artificial Knowledge Representation   
-**AIE x23 Advanced Machine Learning 
-**AIE x64  Artificial Intillegence in Smart Cities  



"""
    def get_Cse_project_response(self):
        return """
🎓 **مشروع التخرج - مفصل**

- **عدد الساعات:** 6 ساعات معتمدة
- **المدة:** فصلين دراسيين
- **التوزيع:** مشروع 1 (2 س) + مشروع 2 (4 س)

## ✅ **شروط التسجيل:**
- **للتسجيل في مشروع 1:** إكمال 112 ساعة معتمدة
- **للتسجيل في مشروع 2:** اجتياز مشروع 1
"""

    def get_Cse_training_response(self):
        return """
🏢 **التدريب الميداني - مفصل**

## 📊 **المعلومات الأساسية:**
- **النوع:** تدريب ميداني عملي
- **المدة:** فصل صيفي كامل
- **الساعات:** 48 ساعة تدريبية لكل مستوى

## ✅ **شروط الالتحاق:**
- **للتدريب 1:** إكمال 60 ساعة
- **للتدريب 2:** إكمال 90 ساعة
"""

    def get_Cse_semesters_response(self):
        return """
📅 **الخطة الدراسية - مفصلة**

## 🎯 **الهيكل العام:**
- **المدة:** 5 سنوات (10 فصول)
- **الساعات:** 160 ساعة
- **المستويات:** 5 مستويات (0-4)

## 📊 **توزيع المستويات:**
- **المستوى 0 (السنة التحضيرية):** 32 ساعة
- **المستوى 1 (السنة الأولى):** 32 ساعة
- **المستوى 2 (السنة الثانية):** 32 ساعة
- **المستوى 3 (السنة الثالثة):** 32 ساعة
- **المستوى 4 (السنة الرابعة):** 32 ساعة
"""

    def get_Cse_fees_response(self):
        return """
💰 **الرسوم والتكاليف - مفصلة**

## 🎯 **الخصومات والإعفاءات:**


"""

    def get_Cse_attendance_response(self):
        return """
⚖️ **نظام الغياب - مفصل**


### **النسبة الأساسية:**
- **الغياب المسموح:** 25% من إجمالي المحاضرات
- **الغياب غير المسموح:** أي نسبة فوق 25%
- **الحرمان التلقائي:** عند تجاوز 25%

"""

    def get_Cse_warnings_response(self):
        return """

## 🎯 **أساس النظام:**
- **الهدف:** تحسين المستوى الأكاديمي
- **التطبيق:** تلقائي بالنظام
- **الإنذار :** المعدل التراكمي أقل من 2.0
- **يتم فصل الطالب اذا تكرر انخفاض معدله عن 2.00 في ستة فصول رئيسية متتابعة**
- **يفصل الطالب اذا لم يحقق متطلبات التخرج خلال المدة القصوى (عشر سنوات)**

- **يتم فصل الطالب اذا لم يسجل اي مقررات لأكثر من فصلين دراسيين رئيسين متتاليين بدون عذر تقبله الكلية**
"""

    def get_Cse_disciplinary_response(self):
        return """
🚫 **العقوبات التأديبية - مفصل**

## 🎯 **نطاق التطبيق:**
- **السلوك:** المخالفات السلوكية
- **النظام:** مخالفات اللوائح
- **الأخلاق:** المخالفات الأخلاقية

## 📋 **أنواع المخالفات:**
- **البسيطة:** التأخير، اللباس غير اللائق
- **المتوسطة:** الإخلال بالنظام العام
- **الكبيرة:** الغش، التزوير، التعدي
"""

    def get_Cse_exams_response(self):
        return """
📝 **نظام الامتحانات - مفصل**

## 🎯 **توزيع الدرجات:**
- **اعمال السنة:** 50 درجة
- **الامتحان النهائي:** 50 درجة

## 📋 **شروط دخول الامتحان:**
- **الحضور:** ضمن النسبة المسموحة (75%)
- **التسديد:** سداد الرسوم الدراسية
- **المتطلبات:** استكمال متطلبات المادة
"""

    def get_Cse_registration_response(self):
        return """
📋 **نظام التسجيل - مفصل**

## 🎯 **مواعيد التسجيل المهمة:**

### **فترة التسجيل الرئيسية:**
- **يبدأ قبل:** أسبوع واحد من بداية الدراسة
- **يستمر لمدة:** أسبوع كامل (7 أيام)


## 💻 **طرق التسجيل:**
1. الدخول على Teams
2. اختيار "التسجيل الإلكتروني"
3. تحديد المواد المراد تسجيلها
4. التحقق من المتطلبات السابقة
5. تأكيد التسجيل النهائي
6. موافقة المرشد الاكاديمي
7. تم التسجيل بنجاح
"""

    def get_Cse_transfers_response(self):
        return """

## 🎯 **شروط التحويل إلى القسم:**
- **حصول علي تقدير C علي الأقل في مادة Computer Skills**
- **دفع رسوم التحويل للقسم**
"""
    def get_ai_transfers_response(self):
        return """

## 🎯 **شروط التحويل إلى القسم:**
- **حصول علي تقدير C علي الأقل في مادة Computer Skills**
- **دفع رسوم التحويل للقسم**
"""
    def get_architecture_transfers_response(self):
        return """

## 🎯 **شروط التحويل إلى القسم:**
- **حصول علي تقدير C علي الأقل في مادة الرسم الهندسي**
- **دفع رسوم التحويل للقسم**
"""
    def get_ARC_transfers_response(self):
        return """

## 🎯 **شروط التحويل إلى القسم:**
- **حصول علي تقدير C علي الأقل في مادة الرسم الهندسي**
- **دفع رسوم التحويل للقسم**
"""
    # ========== دوال المساعدة ==========
    
    def load_pdf_data(self):
        """تحميل ملف PDF"""
        try:
            if os.path.exists(self.pdf_path):
                with open(self.pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    full_text = ""
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        text = page.extract_text()
                        if text:
                            full_text += f"### الصفحة {page_num+1} ###\n{text}\n\n"
                    
                    self.full_text = full_text
                    self.total_pages = len(pdf_reader.pages)
                    self.chunks = self.split_text_into_chunks(full_text)
                    self.is_loaded = True
                    return True
            else:
                #st.warning(f"⚠️ ملف اللائحة غير موجود: {self.pdf_path}")
                self.is_loaded = True
                return True
        except Exception as e:
            st.warning(f"⚠️ خطأ في تحميل اللائحة: {e}")
            self.is_loaded = True
            return True
    
    def split_text_into_chunks(self, text, chunk_size=1000):
        """تقسيم النص إلى أجزاء صغيرة للبحث"""
        if not text:
            return []
            
        sentences = re.split(r'[.!?]', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + "."
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence + "."
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def get_response(self, question):
        """الحصول على إجابة شاملة"""
        question_lower = question.lower().strip()
        
        # البحث في الأسئلة المتوقعة
        best_match = self.find_best_match(question_lower)
        if best_match:
            return best_match
        
        # البحث في النص الأصلي
        original_response = self.search_original_text(question_lower)
        if original_response:
            return original_response
        
        # إجابة افتراضية
        return self.get_default_response()
    
    def find_best_match(self, question):
        """البحث عن أفضل مطابقة"""
        best_score = 0
        best_response = None
        
        for category, data in self.comprehensive_qa.items():
            score = self.calculate_match_score(question, data['patterns'])
            if score > best_score and score > 0.3:
                best_score = score
                best_response = data['response']
        
        return best_response
    
    def calculate_match_score(self, question, patterns):
        """حساب درجة المطابقة"""
        max_score = 0
        question_words = set(question.split())
        
        for pattern in patterns:
            pattern_words = set(pattern.split())
            common_words = question_words.intersection(pattern_words)
            
            if common_words:
                match_ratio = len(common_words) / len(pattern_words)
                max_score = max(max_score, match_ratio)
        
        return max_score
    
    def search_original_text(self, question):
        """البحث في النص الأصلي"""
        try:
            if not self.chunks:
                return None
                
            for chunk in self.chunks:
                if any(word in chunk.lower() for word in question.split()):
                    return f"**معلومات من اللائحة:**\n\n{chunk[:500]}..."
            
            return None
        except:
            return None
    
    def get_default_response(self):
        department_names = {
            "cse": "هندسة الحاسوب",
            "ai": "هندسة الذكاء الاصطناعي",
            "communications": "هندسة الاتصالات",
            "medical": "الهندسة الطبية",
            "mechatronics": "الميكاترونكس",
            "architecture": "الهندسة المعمارية",
            "civil": "الهندسة المدنية",
            "ARC": " الهندسة العمارةالمستدامة"

        }
        
        dept_name = department_names.get(self.department, "Computer and Systems Engineering")
        
        return f"""
🎓 **مرحباً! أنا بوت لائحة قسم {dept_name}**

💡 **أستطيع الإجابة عن جميع أسئلة اللائحة المتوقعة:**

**📊 نظام الدراسة:**
• المعدل التراكمي والتقديرات  
• الساعات المعتمدة
• شروط التخرج والمتطلبات

**📚 المواد الدراسية:**
• المواد الإجبارية والاختيارية
• المتطلبات السابقة
• مشروع التخرج

**💬 اسألني بأي طريقة تريد!**
"""

def add_to_chat_history(question, answer):
    """إضافة سؤال وإجابة إلى سجل المحادثة"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.session_state.chat_history.append({
        "question": question,
        "answer": answer,
        "timestamp": st.session_state.get('chat_counter', 0)
    })
    st.session_state.chat_counter = st.session_state.get('chat_counter', 0) + 1

def display_chat_history():
    """عرض سجل المحادثة"""
    if 'chat_history' in st.session_state and st.session_state.chat_history:
        st.markdown("---")
        st.subheader("💬 تاريخ المحادثة")
        
        for chat in reversed(st.session_state.chat_history[-10:]):  # عرض آخر 10 رسائل
            with st.chat_message("user"):
                st.markdown(f"**سؤال:** {chat['question']}")
            with st.chat_message("assistant"):
                st.markdown(chat['answer'])
            st.markdown("---")
class EnhancedCSEBot(CompleteCSEBot):
    def __init__(self, department="cse"):
        super().__init__(department)
        self.vectorizer = None
        self.qa_corpus = []
        self.qa_responses = []
        self.learned_patterns = {}
        self.initialize_learning_system()
    
    def initialize_learning_system(self):
        """تهيئة نظام التعلم من الأسئلة"""
        # بناء قاعدة معرفية من الأسئلة الحالية
        for category, data in self.comprehensive_qa.items():
            # إضافة الأسئلة المعروفة
            for question in data['questions']:
                self.qa_corpus.append(question)
                self.qa_responses.append(data['response'])
            
            # إضافة الأنماط كأسئلة إضافية
            for pattern in data['patterns'][:3]:  # أول 3 أنماط فقط
                self.qa_corpus.append(pattern)
                self.qa_responses.append(data['response'])
        
        # تدريب نموذج TF-IDF
        if self.qa_corpus:
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=[])
                tfidf_matrix = self.vectorizer.fit_transform(self.qa_corpus)
                self.tfidf_matrix = tfidf_matrix
            except:
                # إذا لم يكن scikit-learn مثبتاً، نستخدم نظام مبسط
                self.vectorizer = None
    
    def extract_keywords(self, text):
        """استخراج الكلمات المفتاحية من النص"""
        # إزالة الحروف الزائدة
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        
        # قائمة بالكلمات الشائعة لتجاهلها
        common_words = {'ما', 'كيف', 'هل', 'لماذا', 'متى', 'أين', 'كم', 'ماذا', 'عن'}
        
        # استخراج الكلمات الفريدة
        words = text.lower().split()
        keywords = [word for word in words if word not in common_words and len(word) > 2]
        
        return set(keywords)
    
    def calculate_semantic_similarity(self, question1, question2):
        """حساب التشابه الدلالي بين سؤالين"""
        try:
            if not self.vectorizer:
                return self.calculate_simple_similarity(question1, question2)
            
            # تحويل السؤالين إلى متجهات TF-IDF
            vectors = self.vectorizer.transform([question1, question2])
            
            # حساب التشابه
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])
            
            return similarity[0][0]
        except:
            return self.calculate_simple_similarity(question1, question2)
    
    def calculate_simple_similarity(self, text1, text2):
        """حساب تشابه مبسط بدون scikit-learn"""
        # تقسيم النصوص إلى كلمات
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # حساب تداخل الكلمات
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0
        
        return len(intersection) / len(union)
    
    def find_best_match_enhanced(self, question):
        """البحث عن أفضل مطابقة باستخدام التعلم"""
        best_score = 0
        best_response = None
        
        # البحث في الأنماط المتعلمة أولاً
        for key, data in self.learned_patterns.items():
            # حساب التشابه مع الأسئلة المعروفة
            max_similarity = 0
            for variation in data['variations'] + [data['question']]:
                similarity = self.calculate_semantic_similarity(question, variation)
                max_similarity = max(max_similarity, similarity)
            
            if max_similarity > best_score:
                best_score = max_similarity
                best_response = data['response']
        
        # إذا لم نجد مطابقة جيدة في الأنماط المتعلمة، نبحث في الأنماط الأساسية
        if best_score < 0.5:
            for category, data in self.comprehensive_qa.items():
                # حساب التشابه مع كل سؤال معروف
                for known_question in data['questions']:
                    similarity = self.calculate_semantic_similarity(question, known_question)
                    
                    # تحسين النتيجة باستخدام الكلمات المفتاحية
                    keywords_q = self.extract_keywords(question)
                    keywords_k = self.extract_keywords(known_question)
                    keyword_match = len(keywords_q.intersection(keywords_k)) / max(len(keywords_q), 1)
                    
                    final_score = (similarity * 0.7) + (keyword_match * 0.3)
                    
                    if final_score > best_score:
                        best_score = final_score
                        best_response = data['response']
        
        return best_response, best_score
    
    def learn_from_variations(self, question, correct_response):
        """التعلم من الاختلافات في صياغة الأسئلة"""
        # تطبيع السؤال
        normalized_q = ' '.join(sorted(question.lower().split()))
        
        # البحث عن سؤال مماثل في الأنماط المتعلمة
        best_match_key = None
        best_similarity = 0
        
        for key, data in self.learned_patterns.items():
            # مقارنة مع الأسئلة المتعلمة
            for learned_q in [data['question']] + data['variations']:
                normalized_learned = ' '.join(sorted(learned_q.lower().split()))
                similarity = self.calculate_simple_similarity(normalized_q, normalized_learned)
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match_key = key
        
        # إذا كان هناك تشابه عالٍ، نضيف هذا كتنوع
        if best_similarity > 0.6 and best_match_key:
            if question not in self.learned_patterns[best_match_key]['variations']:
                self.learned_patterns[best_match_key]['variations'].append(question)
        else:
            # إنشاء نمط جديد
            new_key = len(self.learned_patterns)
            self.learned_patterns[new_key] = {
                'question': question,
                'response': correct_response,
                'variations': [],
                'keywords': list(self.extract_keywords(question))
            }
    
    def get_response(self, question):
        """الحصول على إجابة محسنة مع التعلم"""
        question_lower = question.lower().strip()
        
        # البحث باستخدام النظام المحسن
        best_response, confidence_score = self.find_best_match_enhanced(question_lower)
        
        # إذا كانت الثقة عالية، نستخدم هذه الإجابة
        if confidence_score > 0.5 and best_response:
            # التعلم من هذا السؤال
            self.learn_from_variations(question_lower, best_response)
            return best_response
        
        # إذا لم تكن الثقة عالية، نستخدم الطريقة الأصلية
        original_response = super().get_response(question)
        
        # التعلم من هذه الإجابة أيضاً
        self.learn_from_variations(question_lower, original_response)
        
        return original_response
def main():
    # إذا تم اختيار قسم، تحميل البوت المناسب
    if 'selected_department' in st.session_state:
        # تحميل البوت إذا لم يكن محملًا أو تغير القسم
        if 'department_bot' not in st.session_state or st.session_state.department_bot.department != st.session_state.selected_department:
            st.session_state.department_bot = EnhancedCSEBot(st.session_state.selected_department)
            st.session_state.chat_history = []  # مسح المحادثة القديمة
            st.session_state.question_responses = {}  # لتخزين الإجابات للأسئلة المطروحة
            st.session_state.chat_counter = 0  # عداد للمحادثات
            st.session_state.last_clicked_question = None  # لتتبع آخر سؤال تم الضغط عليه
            
            with st.spinner(f"🔄 جاري تحميل بوت {st.session_state.department_name}..."):
                st.session_state.department_bot.load_pdf_data()
        
        bot = st.session_state.department_bot
        
        if not bot.is_loaded:
            #st.error("❌ فشل في تحميل البوت")
            return
        
        #st.success(f"✅ تم تحميل بوت {st.session_state.department_name} بنجاح!")
        
        # عرض فئات الأسئلة
        st.subheader(f" {st.session_state.department_name}")
        
        categories = list(bot.comprehensive_qa.keys())
        
        # تهيئة session state للإجابات إذا لم تكن موجودة
        if 'question_responses' not in st.session_state:
            st.session_state.question_responses = {}
        
        if 'last_clicked_question' not in st.session_state:
            st.session_state.last_clicked_question = None
        
        # تنظيم الأسئلة في صفوف
        for i in range(0, len(categories), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(categories):
                    category = categories[i + j]
                    data = bot.comprehensive_qa[category]
                    
                    with col:
                        # عرض اسم الفئة
                        category_name = category.replace('_', ' ').title()
                        st.markdown(f"**{category_name}**")
                        
                        # عرض الأسئلة
                        for question_idx, question in enumerate(data['questions']):
                            question_key = f"{category}_{question}_{question_idx}"
                            
                            # زر للسؤال
                            if st.button(question, key=f"btn_{question_key}", use_container_width=True):
                                # الحصول على الإجابة
                                answer = bot.get_response(question)
                                
                                # تخزين الإجابة في session state
                                st.session_state.question_responses[question_key] = answer
                                st.session_state.last_clicked_question = question_key
                                
                                # إضافة إلى سجل المحادثة
                                add_to_chat_history(question, answer)
                            
                            # عرض الإجابة مباشرة تحت السؤال إذا كان هو آخر سؤال تم الضغط عليه
                            if (st.session_state.last_clicked_question == question_key and 
                                question_key in st.session_state.question_responses):
                                
                                # تنسيق الإجابة في صندوق ملون
                                st.markdown("---")
                                st.markdown("### 💡 الإجابة:")
                                st.markdown(st.session_state.question_responses[question_key])
                                st.markdown("---")
        
        # شريط البحث للإسئلة المخصصة
        st.markdown("---")
        
        # استخدام form للحصول على إدخال المستخدم
        with st.form(key="custom_search_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                custom_question = st.text_input("Ask your question", 
                                              placeholder="مثل: كيف أحسب معدلي التراكمي؟",
                                              key="custom_question_input")
            with col2:
                submit_button = st.form_submit_button(label="Search", use_container_width=True)
        
        # معالجة البحث المخصص
        if submit_button and custom_question:
            with st.spinner("🔍 جاري البحث عن الإجابة..."):
                answer = bot.get_response(custom_question)
                
                # عرض نتيجة البحث
                st.markdown("---")
                st.subheader("💬 نتيجة البحث")
                st.markdown(f"**سؤال:** {custom_question}")
                st.markdown("---")
                st.markdown("### Answer")
                st.markdown(answer)
                st.markdown("---")
                
                # إضافة إلى سجل المحادثة
                add_to_chat_history(custom_question, answer)
                
                # حفظ الإجابة للعرض لاحقاً
                st.session_state.last_custom_answer = answer
                st.session_state.last_custom_question = custom_question
        
        # عرض سجل المحادثة
        display_chat_history()

# تشغيل التطبيق
if __name__ == "__main__":
    main()