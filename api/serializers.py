from rest_framework import serializers
from database_management.models import Teacher, Student, ScoreProj, ScoreAdvisor, ScorePoster, ScheduleRoom, DateExam, SchedulePoster
from database_management.models import Project, Settings
from django.contrib.auth.models import User

class RoomSerializer(serializers.Serializer):

    room_name = serializers.CharField(max_length=1024)

class ProjectSerializer(serializers.Serializer):
    proj_name_th = serializers.CharField(max_length=1024)
    proj_name_en = serializers.CharField(max_length=1024)    
    proj_major = serializers.CharField(max_length=1024)
    proj_advisor = serializers.CharField(max_length=1024)
    proj_co_advisor = serializers.CharField(max_length=1024)
    proj_years = serializers.IntegerField(default=0)
    proj_semester = serializers.IntegerField(default=1)
    proj_advisor = serializers.CharField(max_length=1024)
    proj_co_advisor = serializers.CharField(max_length=1024) 

class AdvisorSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Project
        # fields = ('id', 'proj_advisor', 'proj_co_advisor')
        fields = ('id', )

class CheckGradeDoneSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Teacher
        fields = ('score_projs', 'score_posters')
        # fields = ('__all__')

class CheckSettingSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Settings
        fields = ('activate', 'forms')

class ScheduleApiSerializer(serializers.Serializer):
    proj_name_th = serializers.CharField(max_length=1024)
    proj_name_en = serializers.CharField(max_length=1024)    
    time = serializers.CharField(max_length=256)
    room_name = serializers.CharField(max_length=1024)
    date_exam = serializers.CharField(max_length=256)

class ProjectApiSerializer(serializers.Serializer):
    proj_name_th = serializers.CharField(max_length=1024)
    proj_name_en = serializers.CharField(max_length=1024)
    proj_major = serializers.CharField(max_length=1024)
    proj_advisor = serializers.CharField(max_length=1024)
    proj_co_advisor = serializers.CharField(max_length=1024)
    proj_years = serializers.IntegerField(default=0)
    proj_semester = serializers.IntegerField(default=1)    
    student_id = serializers.CharField(max_length=1024)
    student_name = serializers.CharField(max_length=1024, default='')  

class GradeApiSerializer(serializers.Serializer):
    presentation = serializers.IntegerField(default=0)
    question = serializers.IntegerField(default=0)
    report = serializers.IntegerField(default=0)
    presentation_media = serializers.IntegerField(default=0)
    discover = serializers.IntegerField(default=0)
    analysis = serializers.IntegerField(default=0)
    quantity = serializers.IntegerField(default=0)
    levels = serializers.IntegerField(default=0)
    quality = serializers.IntegerField(default=0)
    
class ScoreProjSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreProj
        fields = ('__all__')

class ScoreAdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreAdvisor
        fields = ('__all__')

class ScorePosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScorePoster
        fields = ('__all__')


class GradeSerializer(serializers.Serializer):

    # proj_id = serializers.ForeignKey(Project, on_delete=models.CASCADE)
    # grade_proj_id = serializers.PrimaryKeyRelatedField(source='Project')
    grade_proj_id = serializers.PrimaryKeyRelatedField(read_only=True)
    presentation = serializers.IntegerField(default=0)
    question = serializers.IntegerField(default=0)
    report = serializers.IntegerField(default=0)
    presentation_media = serializers.IntegerField(default=0)
    discover = serializers.IntegerField(default=0)
    analysis = serializers.IntegerField(default=0)
    quantity = serializers.IntegerField(default=0)
    levels = serializers.IntegerField(default=0)
    quality = serializers.IntegerField(default=0)

class GradeAdvisorSerializer(serializers.Serializer):

    grade_advisor_proj_id = serializers.PrimaryKeyRelatedField(read_only=True)
    propose = serializers.IntegerField(default=0)
    planning = serializers.IntegerField(default=0)
    tool = serializers.IntegerField(default=0)
    advice = serializers.IntegerField(default=0)
    improve = serializers.IntegerField(default=0)
    quality_report = serializers.IntegerField(default=0)
    quality_project = serializers.IntegerField(default=0)

class GradePosterSerializer(serializers.Serializer):

    grade_poster_proj_id = serializers.PrimaryKeyRelatedField(read_only=True)
    time_spo = serializers.IntegerField(default=0)
    character_spo = serializers.IntegerField(default=0)
    presentation_spo = serializers.IntegerField(default=0)
    question_spo = serializers.IntegerField(default=0)
    media_spo = serializers.IntegerField(default=0)
    quality_spo = serializers.IntegerField(default=0)

class ScheduleRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleRoom
        fields = ('__all__')
        # depth = 2

class TimeExamSerializer(serializers.Serializer):

    time_exam = serializers.CharField(max_length=256)
    time_period = serializers.IntegerField(default=0)

class TimeExamOnlySerializer(serializers.Serializer):

    time_exam = serializers.CharField(max_length=256)

class DateExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = DateExam
        fields = ('__all__')

class DateExamOnlySerializer(serializers.Serializer):

    date_exam = serializers.CharField(max_length=256)


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('teacher_name', 'schedule_teacher', 'schepost_teacher')
        depth = 2

class TeacherScheduleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('schedule_teacher', )

class TeacherSchedulePosterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('schepost_teacher', )

class TeacherIdSerializer(serializers.Serializer):

    id = serializers.IntegerField()

class TeacherLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('__all__')
        # fields = ('id', 'login_user','teacher_name')

class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('is_superuser', 'is_staff', 'is_active', 'id')


class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = ('student_id', 'student_name')

class ProjectNameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ('id', 'proj_name_en')

class TeacherScoreIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('score_projs', 'id')

class SchedulePosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchedulePoster
        fields = ('__all__')

class DateSchedulePosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchedulePoster
        fields = ('date_post', )

class DateScheduleProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = DateExam
        fields = ('date_exam', 'room_id_id')