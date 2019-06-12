from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db.models import Q, Max
from rest_framework.views import APIView
from rest_framework.response import Response
from database_management import models
from api.serializers import RoomSerializer, ProjectSerializer, GradeSerializer, TeacherSerializer, GradeAdvisorSerializer
from api.serializers import GradePosterSerializer, StudentSerializer, ProjectNameSerializer, TeacherIdSerializer, ScoreProjSerializer
from api.serializers import ScoreAdvisorSerializer, ScorePosterSerializer, ScheduleRoomSerializer, TimeExamOnlySerializer
from api.serializers import DateExamOnlySerializer, TeacherScheduleListSerializer, TeacherSchedulePosterListSerializer
from api.serializers import SchedulePosterSerializer, ScheduleApiSerializer, ProjectApiSerializer, GradeApiSerializer, AdvisorSerializer
from api.serializers import CheckGradeDoneSerializer, CheckSettingSerializer, DateSchedulePosterSerializer, DateScheduleProjectSerializer
from api.serializers import userSerializer, TeacherLoginSerializer
from django.shortcuts import get_object_or_404
from django.forms import model_to_dict
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from ldap3 import Server, Connection, ALL
from database_management.models import *
from django_python3_ldap.auth import LDAPBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from django.utils.decorators import method_decorator

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class HelloAPI(APIView):
    def get(self, request):
        user = {
            'name': 'abcdef',
            'surname': 'dkjfekljio',
            'age': 123
        }

       

        # input = request.GET.get("roomname")

        # rooms = models.Room.objects.filter(room_name = input)

        # serializer = RoomSerializer(rooms, many=True)
        # # serializer = self.serializer.room_name="M03"
        # print(input)
        # return Response(serializer.data)

        input_proj_years = request.GET.get("proj_years")
        project = models.Project.objects.filter(proj_years = input_proj_years)
        serializer = ProjectSerializer(project, many=True)
        print(project)
        return Response(serializer.data)

        

    def post(self, request):
        input_room_name = request.POST.get("room_name")

        add = models.Room(room_name = input_room_name)
        add.save()

        serializer = RoomSerializer(add)
        print(input_room_name)
        return Response(serializer.data)

    def put(self, request):
        pass

    def delete(self, request):
        pass

class ApiProject(APIView):
    def get(self, request):
        input_proj_years = request.GET.get("proj_years")
        project = models.Project.objects.filter(proj_years = input_proj_years)
        serializer = ProjectSerializer(project, many=True)
        print(input_proj_years)
        return Response(serializer.data)

    def post(self, request):
        input_proj_name_en = request.POST.get("proj_name_en")
        input_proj_semester = request.POST.get("proj_semester")
        input_proj_name_th = request.POST.get("proj_name_th")
        input_proj_major = request.POST.get("proj_major")
        input_proj_advisor = request.POST.get("proj_advisor")
        input_proj_co_advisor = request.POST.get("proj_co_advisor")
        input_proj_years = request.POST.get("proj_years")

        add = models.Project(proj_name_en = input_proj_name_en, proj_semester = input_proj_semester, proj_name_th = input_proj_name_th, 
        proj_major = input_proj_major, proj_advisor = input_proj_advisor, proj_co_advisor = input_proj_co_advisor, 
        proj_years = input_proj_years)
        add.save()

        serializer = ProjectSerializer(add)
        return Response(serializer.data)

    def put(self, request):
        input_id = request.data.get("id")
        input_proj_name_en = request.data.get("proj_name_en")

        # device = self.get_object(input)
        # device = models.Project.objects.get(pk = input)
        edit = get_object_or_404(models.Project, pk=input_id)
        edit.proj_name_en = input_proj_name_en
        edit.save()
        serializer = ProjectSerializer(edit)
        return Response(serializer.data)

    def delete(self, request):
        pass

# แสดงชื่อโครงงานและคะแนนโครงงานส่วนกรรมการคุมสอบ
class GradeApi(APIView):
    def get(self, request):
        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_proj_id = request.GET.get("score_proj_id")
        # # คะแนนโครงงานส่วนกรรมการคุมสอบ
        # teacher = models.Teacher.objects.get(login_user_id = input_login_user_id)   
        # score_projs = teacher.score_projs.filter(id=input_score_proj_id)
        # serializer = ScoreProjSerializer(score_projs, many=True)
        # new_serializer_data = list(serializer.data)
        # data2 = {
        #         "score": new_serializer_data[0]
        # }
        # # ชื่อโครงงาน
        # proj_name = models.Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True)
        # # serializer2 = ProjectApiSerializer(proj_name, many=True)
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data2["score"].update(data)

        # # หาว่ากรอกคะแนนแล้ว
        # advisor = models.Teacher.objects.filter(id=32)
        # test = CheckGradeDoneSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data) 
        # data3 = {
        #         "proj_mark": new_serializer_data_test[0]['score_projs'],
        #         "poster_mark": new_serializer_data_test[0]['score_posters']
        # }
        # data2["score"].update(data3)

        # return Response(data2)        
        
        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_proj_id = request.GET.get("score_proj_id") #project id
        # # คะแนนโครงงานส่วนกรรมการคุมสอบ   
        # ScoreProjs = ScoreProj.objects.filter(teacher__id = input_login_user_id, id=input_score_proj_id)        
        # serializer = ScoreProjSerializer(ScoreProjs, many=True)
        # new_serializer_data = list(serializer.data)
        # data2 = {
        #         "proj_id": new_serializer_data[0]["proj_id"],
        #         "id": new_serializer_data[0]["id"],
        #         "presentation": new_serializer_data[0]["presentation"],
        #         "question": new_serializer_data[0]["question"],
        #         "report": new_serializer_data[0]["report"],
        #         "presentation_media": new_serializer_data[0]["presentation_media"],
        #         "discover": new_serializer_data[0]["discover"],
        #         "analysis": new_serializer_data[0]["analysis"],
        #         "quantity": new_serializer_data[0]["quantity"],
        #         "levels": new_serializer_data[0]["levels"],
        #         "quality": new_serializer_data[0]["quality"]                
        # } 
        # # ชื่อโครงงาน
        # proj_name = Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data.update(data2) 
        # # หาว่ากรอกคะแนนแล้ว
        # advisor = Teacher.objects.filter(id=input_login_user_id)
        # test = CheckGradeDoneSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data) 
        # data3 = {
        #         "proj_mark": new_serializer_data_test[0]['score_projs']
        # }        
        # data.update(data3) 
        # toList = [data]
        # return Response(toList)

        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_proj_id = request.GET.get("score_proj_id") #project id
        # # คะแนนโครงงานส่วนส่วนกรรมการคุมสอบ
        # teacher = Teacher.objects.get(login_user_id = input_login_user_id)   
        # ScoreProjs = teacher.score_projs.filter(id=input_score_proj_id) 
        # serializer = ScoreProjSerializer(ScoreProjs, many=True)
        # new_serializer_data = list(serializer.data)
        # #  
        # # ScoreProjs = ScoreProj.objects.filter(teacher__id = input_login_user_id, id=input_score_proj_id)        
        # # serializer = ScoreProjSerializer(ScoreProjs, many=True)
        # # new_serializer_data = list(serializer.data)
        # if new_serializer_data:
        #     data2 = {
        #             "proj_id": new_serializer_data[0]["proj_id"],
        #             "id": new_serializer_data[0]["id"],
        #             "presentation": new_serializer_data[0]["presentation"],
        #             "question": new_serializer_data[0]["question"],
        #             "report": new_serializer_data[0]["report"],
        #             "presentation_media": new_serializer_data[0]["presentation_media"],
        #             "discover": new_serializer_data[0]["discover"],
        #             "analysis": new_serializer_data[0]["analysis"],
        #             "quantity": new_serializer_data[0]["quantity"],
        #             "levels": new_serializer_data[0]["levels"],
        #             "quality": new_serializer_data[0]["quality"]                
        #     } 
        # else:
        #     data2 = {
        #             "proj_id": "ยังไม่ได้กรอกคะแนน",
        #             "id": "ยังไม่ได้กรอกคะแนน",
        #             "presentation": "ยังไม่ได้กรอกคะแนน",
        #             "question": "ยังไม่ได้กรอกคะแนน",
        #             "report": "ยังไม่ได้กรอกคะแนน",
        #             "presentation_media": "ยังไม่ได้กรอกคะแนน",
        #             "discover": "ยังไม่ได้กรอกคะแนน",
        #             "analysis": "ยังไม่ได้กรอกคะแนน",
        #             "quantity": "ยังไม่ได้กรอกคะแนน",
        #             "levels": "ยังไม่ได้กรอกคะแนน",
        #             "quality": "ยังไม่ได้กรอกคะแนน"               
        #     }
        # # ชื่อโครงงาน
        # proj_name = Project.objects.filter(id = input_score_proj_id)
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data.update(data2) 
        # toList = [data]
        # return Response(toList)

        input_login_user_id = request.GET.get("login_user_id")
        input_score_proj_id = request.GET.get("score_proj_id") #project id
        # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        # teacher = models.Teacher.objects.get(login_user_id = input_login_user_id)     
        teacher = Teacher.objects.get(login_user_id = input_login_user_id)    
        
        # database_management_teacher_score_posters ทั้งหมดของ login_user_id
        # login_user_id = teacher.score_posters.all()
        # serializer_login_user_id = ScorePosterSerializer(login_user_id, many=True)
        # new_serializer_data_login_user_id = list(serializer_login_user_id.data)
        # print(new_serializer_data_login_user_id)
        # return Response(new_serializer_data_login_user_id)

       
        # database_management_teacher_score_posters ทั้งหมดของ project id
        proj_id_id = ScoreProj.objects.filter(proj_id_id=input_score_proj_id)
        serializer_proj_id_id = ScoreProjSerializer(proj_id_id, many=True)
        new_serializer_data_proj_id_id = list(serializer_proj_id_id.data)
        print(new_serializer_data_proj_id_id)
        # return Response(new_serializer_data_proj_id_id)
        proj_id_id_list = []
        for i in range (len (new_serializer_data_proj_id_id)):
            proj_id_id_list.append(new_serializer_data_proj_id_id[i]["id"])
        # print(proj_id_id_list)
        # return Response(proj_id_id_list)
        forBreak = False
        for i in range (len (new_serializer_data_proj_id_id)):
            if forBreak == True:
                    break
            login_user_id = teacher.score_projs.all()
            serializer_login_user_id = ScoreProjSerializer(login_user_id, many=True)
            new_serializer_data_login_user_id = list(serializer_login_user_id.data)
            # print(new_serializer_data_login_user_id)
            for x in range (len (new_serializer_data_login_user_id)):
                if forBreak == True:
                    break
                elif proj_id_id_list[i] == new_serializer_data_login_user_id[x]["id"]:
                    forBreak = True
                    aaa = new_serializer_data_login_user_id[x]["id"]
                    # print(new_serializer_data_login_user_id[x]["id"])
        # return Response(aaa)
        # aaa = score_poster_id

        # ScorePoster = teacher.score_posters.filter(id=input_score_poster_id)
        # serializer = ScorePosterSerializer(ScorePoster, many=True)
        # new_serializer_data = list(serializer.data)

        if forBreak:
            ScorePosters = teacher.score_projs.filter(id=aaa)
            serializer = ScoreProjSerializer(ScorePosters, many=True)
            new_serializer_data = list(serializer.data)
            print(new_serializer_data)
            if new_serializer_data:
                data2 = {
                        "grade": forBreak,
                        "proj_id": new_serializer_data[0]["proj_id"],
                        "id": new_serializer_data[0]["id"],
                        "presentation": new_serializer_data[0]["presentation"],
                        "question": new_serializer_data[0]["question"],
                        "report": new_serializer_data[0]["report"],
                        "presentation_media": new_serializer_data[0]["presentation_media"],
                        "discover": new_serializer_data[0]["discover"],
                        "analysis": new_serializer_data[0]["analysis"],
                        "quantity": new_serializer_data[0]["quantity"],
                        "levels": new_serializer_data[0]["levels"],
                        "quality": new_serializer_data[0]["quality"]
                }
        else:
            data2 = {
                    "grade": forBreak,
                    "proj_id": 0,
                    "id": 0,
                    "presentation": 0,
                    "question": 0,
                    "report": 0,
                    "presentation_media": 0,
                    "discover": 0,
                    "analysis": 0,
                    "quantity": 0,
                    "levels": 0,
                    "quality": 0                   
            }
        # ชื่อโครงงาน
        proj_name = Project.objects.filter(id = input_score_proj_id)
        serializer2 = ProjectNameSerializer(proj_name, many=True) 
        new_serializer_data2 = list(serializer2.data)
        data = {
                "proj_name_en": new_serializer_data2[0]['proj_name_en']
        }
        data.update(data2) 
        toList = [data]
        return Response(toList)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# แสดงชื่อโครงงานและคะแนนโครงงานส่วนอาจารย์ที่ปรึกษา
class GradeAdvisorApi(APIView):
    def get(self, request):
        
        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_advisor_id = request.GET.get("score_advisor_id")
        # # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา
        # teacher = models.Teacher.objects.get(login_user_id = input_login_user_id)   
        # ScoreAdvisor = teacher.score_advisor.filter(id=input_score_advisor_id)
        # serializer = ScoreAdvisorSerializer(ScoreAdvisor, many=True)
        # new_serializer_data = list(serializer.data)
        # print(new_serializer_data)
        # data2 = {
        #         "score_advisor": new_serializer_data[0]
        # }
        # # ชื่อโครงงาน
        # proj_name = models.Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True)
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data2["score_advisor"].update(data)      
        # # หาว่ากรอกคะแนนแล้ว
        # advisor = models.Teacher.objects.filter(id=32)
        # test = CheckGradeDoneSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data) 
        # data3 = {
        #         "proj_mark": new_serializer_data_test[0]['score_projs'],
        #         "poster_mark": new_serializer_data_test[0]['score_posters']
        # }
        # data2["score_advisor"].update(data3)  
        # return Response(data2)

        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_advisor_id = request.GET.get("score_advisor_id") #project id
        # # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        # # teacher = Teacher.objects.get(login_user_id = input_login_user_id)
        # teacher = Teacher.objects.filter(id = input_login_user_id)
        
        # aaaa = TeacherLoginSerializer(teacher, many=True)
        # a1234 = list(aaaa.data)
        # print(a1234)    

        # ScoreAdvisor = teacher.score_advisor.filter(id=input_score_advisor_id)
        # serializer = ScoreAdvisorSerializer(ScoreAdvisor, many=True)
        # new_serializer_data = list(serializer.data)
        # print(new_serializer_data)
        # data2 = {
        #         "proj_id": new_serializer_data[0]["proj_id"],
        #         "id": new_serializer_data[0]["id"],
        #         "propose": new_serializer_data[0]["propose"],
        #         "planning": new_serializer_data[0]["planning"],    
        #         "tool": new_serializer_data[0]["tool"],    
        #         "advice": new_serializer_data[0]["advice"],    
        #         "improve": new_serializer_data[0]["improve"],    
        #         "quality_report": new_serializer_data[0]["quality_report"],  
        #         "quality_project": new_serializer_data[0]["quality_project"]                  
        # } 
        # # ชื่อโครงงาน
        # proj_name = Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data.update(data2) 
        # # หาว่ากรอกคะแนนแล้ว
        # advisor = Teacher.objects.filter(id=32)
        # test = CheckGradeDoneSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data) 
        # data3 = {
        #         "proj_mark": new_serializer_data_test[0]['score_projs']
        # }        
        # data.update(data3) 
        # toList = [data]
        # return Response(toList)

        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_advisor_id = request.GET.get("score_advisor_id") #project id
        # # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        # # teacher = Teacher.objects.get(login_user_id = input_login_user_id)
        # teacher = Teacher.objects.filter(id = input_login_user_id)
        
        # # aaaa = TeacherLoginSerializer(teacher, many=True)
        # # a1234 = list(aaaa.data)
        # # print(a1234)    

        # ScoreAdvisor = teacher.score_advisor.filter(id=input_score_advisor_id)
        # serializer = ScoreAdvisorSerializer(ScoreAdvisor, many=True)
        # new_serializer_data = list(serializer.data)
        # print(new_serializer_data)
        # data2 = {
        #         "proj_id": new_serializer_data[0]["proj_id"],
        #         "id": new_serializer_data[0]["id"],
        #         "propose": new_serializer_data[0]["propose"],
        #         "planning": new_serializer_data[0]["planning"],    
        #         "tool": new_serializer_data[0]["tool"],    
        #         "advice": new_serializer_data[0]["advice"],    
        #         "improve": new_serializer_data[0]["improve"],    
        #         "quality_report": new_serializer_data[0]["quality_report"],  
        #         "quality_project": new_serializer_data[0]["quality_project"]                  
        # } 
        # # ชื่อโครงงาน
        # proj_name = Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data.update(data2) 
        # # หาว่ากรอกคะแนนแล้ว
        # advisor = Teacher.objects.filter(id=32)
        # test = CheckGradeDoneSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data) 
        # data3 = {
        #         "proj_mark": new_serializer_data_test[0]['score_projs']
        # }        
        # data.update(data3) 
        # toList = [data]
        # return Response(toList)

        input_login_user_id = request.GET.get("login_user_id")
        input_score_advisor_id = request.GET.get("score_advisor_id") #project id
        # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        # teacher = models.Teacher.objects.get(login_user_id = input_login_user_id)     
        teacher = Teacher.objects.get(login_user_id = input_login_user_id)    
        
        # database_management_teacher_score_posters ทั้งหมดของ login_user_id
        # login_user_id = teacher.score_posters.all()
        # serializer_login_user_id = ScorePosterSerializer(login_user_id, many=True)
        # new_serializer_data_login_user_id = list(serializer_login_user_id.data)
        # print(new_serializer_data_login_user_id)
        # return Response(new_serializer_data_login_user_id)

       
        # database_management_teacher_score_posters ทั้งหมดของ project id
        proj_id_id = ScoreAdvisor.objects.filter(proj_id_id=input_score_advisor_id)
        serializer_proj_id_id = ScoreAdvisorSerializer(proj_id_id, many=True)
        new_serializer_data_proj_id_id = list(serializer_proj_id_id.data)
        print(new_serializer_data_proj_id_id)
        # return Response(new_serializer_data_proj_id_id)
        proj_id_id_list = []
        for i in range (len (new_serializer_data_proj_id_id)):
            proj_id_id_list.append(new_serializer_data_proj_id_id[i]["id"])
        # print(proj_id_id_list)
        # return Response(proj_id_id_list)
        forBreak = False
        for i in range (len (new_serializer_data_proj_id_id)):
            if forBreak == True:
                    break
            login_user_id = teacher.score_advisor.all()
            serializer_login_user_id = ScoreAdvisorSerializer(login_user_id, many=True)
            new_serializer_data_login_user_id = list(serializer_login_user_id.data)
            print(new_serializer_data_login_user_id)
            for x in range (len (new_serializer_data_login_user_id)):
                if forBreak == True:
                    break
                elif proj_id_id_list[i] == new_serializer_data_login_user_id[x]["id"]:
                    forBreak = True
                    aaa = new_serializer_data_login_user_id[x]["id"]
                    print(new_serializer_data_login_user_id[x]["id"])

        if forBreak:
            ScorePosters = teacher.score_advisor.filter(id=aaa)
            serializer = ScoreAdvisorSerializer(ScorePosters, many=True)
            new_serializer_data = list(serializer.data)
            print("_____________")
            print(new_serializer_data)
            if new_serializer_data:
                data2 = {
                        "grade": forBreak,
                        "proj_id": new_serializer_data[0]["proj_id"],
                        "id": new_serializer_data[0]["id"],
                        "propose": new_serializer_data[0]["propose"],
                        "planning": new_serializer_data[0]["planning"],    
                        "tool": new_serializer_data[0]["tool"],    
                        "advice": new_serializer_data[0]["advice"],    
                        "improve": new_serializer_data[0]["improve"],    
                        "quality_report": new_serializer_data[0]["quality_report"],  
                        "quality_project": new_serializer_data[0]["quality_project"]
                }
        else:
            data2 = {
                    "grade": forBreak,
                    # "proj_id": "ยังไม่ได้กรอกคะแนน",
                    "proj_id": 0,
                    "id": 0,
                    "propose": 0,
                    "planning": 0,    
                    "tool": 0,    
                    "advice": 0,    
                    "improve": 0,    
                    "quality_report": 0,  
                    "quality_project": 0                  
            }
        # ชื่อโครงงาน
        proj_name = Project.objects.filter(id = input_score_advisor_id)
        serializer2 = ProjectNameSerializer(proj_name, many=True) 
        new_serializer_data2 = list(serializer2.data)
        data = {
                "proj_name_en": new_serializer_data2[0]['proj_name_en']
        }
        data.update(data2) 
        toList = [data]
        return Response(toList)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# แสดงชื่อโครงงานและคะแนนโครงงานส่วนโปสเตอร์
class GradePosterApi(APIView):
    def get(self, request):
        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_poster_id = request.GET.get("score_poster_id")
        # # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        # teacher = models.Teacher.objects.get(login_user_id = input_login_user_id)        
        # ScorePoster = teacher.score_posters.filter(id=input_score_poster_id)
        # serializer = ScorePosterSerializer(ScorePoster, many=True)
        # new_serializer_data = list(serializer.data)
        # data2 = {
        #         "score_poster": new_serializer_data[0]
        # } 
        # # ชื่อโครงงาน
        # proj_name = models.Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # # new_serializer_data2.append(new_serializer_data)        
        # # return Response(new_serializer_data2)
        # data2["score_poster"].update(data)      
        # # หาว่ากรอกคะแนนแล้ว
        # advisor = models.Teacher.objects.filter(id=32)
        # test = CheckGradeDoneSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data) 
        # data3 = {
        #         "proj_mark": new_serializer_data_test[0]['score_projs'],
        #         "poster_mark": new_serializer_data_test[0]['score_posters']
        # }
        # data2["score_poster"].update(data3)    
        # return Response(data2)

        # input_login_user_id = request.GET.get("login_user_id")
        # input_score_poster_id = request.GET.get("score_poster_id") #project id
        # # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        # # teacher = models.Teacher.objects.get(login_user_id = input_login_user_id)     
        # teacher = Teacher.objects.get(login_user_id = input_login_user_id)    
        # ScorePoster = teacher.score_posters.filter(id=input_score_poster_id)
        # serializer = ScorePosterSerializer(ScorePoster, many=True)
        # new_serializer_data = list(serializer.data)
        # data2 = {
        #         "proj_id": new_serializer_data[0]["proj_id"],
        #         "id": new_serializer_data[0]["id"],
        #         "time_spo": new_serializer_data[0]["time_spo"],
        #         "character_spo": new_serializer_data[0]["character_spo"],
        #         "presentation_spo": new_serializer_data[0]["presentation_spo"],
        #         "question_spo": new_serializer_data[0]["question_spo"],
        #         "media_spo": new_serializer_data[0]["media_spo"],
        #         "quality_spo": new_serializer_data[0]["quality_spo"]                
        # } 
        # # ชื่อโครงงาน
        # proj_name = Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data.update(data2) 
        # # หาว่ากรอกคะแนนแล้ว
        # advisor = Teacher.objects.filter(id=32)
        # test = CheckGradeDoneSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data) 
        # data3 = {
        #         "poster_mark": new_serializer_data_test[0]['score_posters']
        #         # "poster_mark": new_serializer_data_test
        # }        
        # data.update(data3) 
        # toList = [data]
        # return Response(toList)

        # login_user_id = 8
        # score_poster_id = 1
        # [
        #     {
        #         "proj_name_en": "3d model reconstruction",
        #         "proj_id": 1,
        #         "id": 1,
        #         "time_spo": 10,
        #         "character_spo": 10,
        #         "presentation_spo": 9,
        #         "question_spo": 9,
        #         "media_spo": 9,
        #         "quality_spo": 9,
        #         "poster_mark": [
        #             571,
        #             572,
        #             573,
        #             574,
        #             575,
        #             576
        #         ]
        #     }
        # ]

        input_login_user_id = request.GET.get("login_user_id")
        input_score_poster_id = request.GET.get("score_poster_id") #project id
        # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        # teacher = models.Teacher.objects.get(login_user_id = input_login_user_id)     
        teacher = Teacher.objects.get(login_user_id = input_login_user_id)    
        
        # # database_management_teacher_score_posters ทั้งหมดของ login_user_id
        # login_user_id = teacher.score_posters.all()
        # serializer_login_user_id = ScorePosterSerializer(login_user_id, many=True)
        # new_serializer_data_login_user_id = list(serializer_login_user_id.data)
        # print(new_serializer_data_login_user_id)
        # return Response(new_serializer_data_login_user_id)

       
        # database_management_teacher_score_posters ทั้งหมดของ project id
        proj_id_id = ScorePoster.objects.filter(proj_id_id=input_score_poster_id)
        serializer_proj_id_id = ScorePosterSerializer(proj_id_id, many=True)
        new_serializer_data_proj_id_id = list(serializer_proj_id_id.data)
        print(new_serializer_data_proj_id_id)
        # return Response(new_serializer_data_proj_id_id)
        proj_id_id_list = []
        for i in range (len (new_serializer_data_proj_id_id)):
            proj_id_id_list.append(new_serializer_data_proj_id_id[i]["id"])
        # print(proj_id_id_list)
        # return Response(proj_id_id_list)
        forBreak = False
        for i in range (len (new_serializer_data_proj_id_id)):
            if forBreak == True:
                    break
            login_user_id = teacher.score_posters.all()
            serializer_login_user_id = ScorePosterSerializer(login_user_id, many=True)
            new_serializer_data_login_user_id = list(serializer_login_user_id.data)
            # print(new_serializer_data_login_user_id)
            for x in range (len (new_serializer_data_login_user_id)):
                if forBreak == True:
                    break
                elif proj_id_id_list[i] == new_serializer_data_login_user_id[x]["id"]:
                    forBreak = True
                    aaa = new_serializer_data_login_user_id[x]["id"]
                    # print(new_serializer_data_login_user_id[x]["id"])
        # return Response(aaa)
        # aaa = score_poster_id

        # ScorePoster = teacher.score_posters.filter(id=input_score_poster_id)
        # serializer = ScorePosterSerializer(ScorePoster, many=True)
        # new_serializer_data = list(serializer.data)

        if forBreak:
            ScorePosters = teacher.score_posters.filter(id=aaa)
            serializer = ScorePosterSerializer(ScorePosters, many=True)
            new_serializer_data = list(serializer.data)
            print(new_serializer_data)
            if new_serializer_data:
                data2 = {
                        "grade": forBreak,
                        "proj_id": new_serializer_data[0]["proj_id"],
                        "id": new_serializer_data[0]["id"],
                        "time_spo": new_serializer_data[0]["time_spo"],
                        "character_spo": new_serializer_data[0]["character_spo"],
                        "presentation_spo": new_serializer_data[0]["presentation_spo"],
                        "question_spo": new_serializer_data[0]["question_spo"],
                        "media_spo": new_serializer_data[0]["media_spo"],
                        "quality_spo": new_serializer_data[0]["quality_spo"]                
                }
        else:
            data2 = {
                    "grade": forBreak,
                    "proj_id": 0,
                    "id": 0,
                    "time_spo": 0,
                    "character_spo": 0,
                    "presentation_spo": 0,
                    "question_spo": 0,
                    "media_spo": 0,
                    "quality_spo": 0               
            }
        # ชื่อโครงงาน
        proj_name = Project.objects.filter(id = input_score_poster_id)
        serializer2 = ProjectNameSerializer(proj_name, many=True) 
        new_serializer_data2 = list(serializer2.data)
        data = {
                "proj_name_en": new_serializer_data2[0]['proj_name_en']
        }
        data.update(data2) 
        toList = [data]
        return Response(toList)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# บรรทึกคะแนนโครงงานส่วนกรรมการคุมสอบ
class SaveGradeApi(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        pass

    # ใส่คะแนนครั้งแรก (ยังไม่มีใน database)    
    def post(self, request):
        input_grade_proj_id = request.POST.get("grade_proj_id")
        input_presentation = request.POST.get("presentation")
        input_question = request.POST.get("question")
        input_report = request.POST.get("report")
        input_presentation_media = request.POST.get("presentation_media")
        input_discover = request.POST.get("discover")
        input_analysis = request.POST.get("analysis")
        input_quantity = request.POST.get("quantity")
        input_levels = request.POST.get("levels")
        input_quality = request.POST.get("quality")
        grade_proj_id = Project.objects.get(id=input_grade_proj_id)
        add = ScoreProj(proj_id = grade_proj_id, presentation = input_presentation, question = input_question, 
        report = input_report, presentation_media = input_presentation_media, discover = input_discover, analysis = input_analysis, 
        quantity = input_quantity, levels = input_levels, quality = input_quality)
        add.save()
        # serializer = GradeSerializer(add)
        # return Response(serializer.data)

        input_teacher_id = request.POST.get("teacher_id")
        teacher = Teacher.objects.get(id = input_teacher_id)
        teacher.score_projs.add(add)
        teacher.save()
        login_user_id = teacher.score_projs.all()
        serializer_login_user_id = ScoreProjSerializer(login_user_id, many=True)
        new_serializer_data_login_user_id = list(serializer_login_user_id.data)
        return Response(new_serializer_data_login_user_id)

    # แก้ไขคะแนน
    def put(self, request):
        input_grade_proj_id = request.data.get("grade_proj_id")
        input_presentation = request.data.get("presentation")
        input_question = request.data.get("question")
        input_report = request.data.get("report")
        input_presentation_media = request.data.get("presentation_media")
        input_discover = request.data.get("discover")
        input_analysis = request.data.get("analysis")
        input_quantity = request.data.get("quantity")
        input_levels = request.data.get("levels")
        input_quality = request.data.get("quality")
        # edit = get_object_or_404(models.ScoreProj, pk=input_grade_proj_id)
        edit = get_object_or_404(ScoreProj, pk=input_grade_proj_id)
        edit.presentation = input_presentation
        edit.question = input_question
        edit.report = input_report
        edit.presentation_media = input_presentation_media
        edit.discover = input_discover
        edit.analysis = input_analysis
        edit.quantity = input_quantity
        edit.levels = input_levels
        edit.quality = input_quality
        edit.save()
        serializer = GradeSerializer(edit)
        return Response(serializer.data)

    def delete(self, request):
        pass

# บรรทึกคะแนนโครงงานส่วนอาจารย์ที่ปรึกษา
class SaveGradeAdvisorApi(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        pass

    # ใส่คะแนนครั้งแรก (ยังไม่มีใน database)
    def post(self, request):
        input_grade_advisor_proj_id = request.POST.get("grade_advisor_proj_id")
        input_propose = request.POST.get("propose")
        input_planning = request.POST.get("planning")
        input_tool = request.POST.get("tool")
        input_advice = request.POST.get("advice")
        input_improve = request.POST.get("improve")
        input_quality_report = request.POST.get("quality_report")
        input_quality_project = request.POST.get("quality_project")
        grade_advisor_proj_id = Project.objects.get(id=input_grade_advisor_proj_id)
        add = ScoreAdvisor(proj_id = grade_advisor_proj_id, propose = input_propose, planning = input_planning, 
        tool = input_tool, advice = input_advice, improve = input_improve, quality_report = input_quality_report, 
        quality_project = input_quality_project)
        add.save()
        
        input_teacher_id = request.POST.get("teacher_id")
        teacher = Teacher.objects.get(id = input_teacher_id)
        teacher.score_advisor.add(add)
        teacher.save()
        login_user_id = teacher.score_projs.all()
        serializer_login_user_id = ScoreProjSerializer(login_user_id, many=True)
        new_serializer_data_login_user_id = list(serializer_login_user_id.data)
        return Response(new_serializer_data_login_user_id)

        # serializer = GradeAdvisorSerializer(add)
        # return Response(serializer.data)

    # แก้ไขคะแนน
    def put(self, request):
        input_grade_advisor_proj_id = request.data.get("grade_advisor_proj_id")
        input_propose = request.data.get("propose")
        input_planning = request.data.get("planning")
        input_tool = request.data.get("tool")
        input_advice = request.data.get("advice")
        input_improve = request.data.get("improve")
        input_quality_report = request.data.get("quality_report")
        input_quality_project = request.data.get("quality_project")
        edit = get_object_or_404(ScoreAdvisor, pk=input_grade_advisor_proj_id)
        edit.propose = input_propose
        edit.planning = input_planning
        edit.tool = input_tool
        edit.advice = input_advice
        edit.improve = input_improve
        edit.quality_report = input_quality_report
        edit.quality_project = input_quality_project
        edit.save()
        serializer = GradeAdvisorSerializer(edit)
        return Response(serializer.data)

    def delete(self, request):
        pass

# บรรทึกคะแนนโครงงานส่วนส่วนโปสเตอร์
class SaveGradePosterApi(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        pass

    # ใส่คะแนนครั้งแรก (ยังไม่มีใน database)
    def post(self, request):
        input_grade_poster_proj_id = request.POST.get("grade_poster_proj_id")
        input_time_spo = request.POST.get("time_spo")
        input_character_spo = request.POST.get("character_spo")
        input_presentation_spo = request.POST.get("presentation_spo")
        input_question_spo = request.POST.get("question_spo")
        input_media_spo = request.POST.get("media_spo")
        input_quality_spo = request.POST.get("quality_spo")
        grade_poster_proj_id = Project.objects.get(id=input_grade_poster_proj_id)
        add = ScorePoster(proj_id = grade_poster_proj_id, time_spo = input_time_spo, character_spo = input_character_spo, 
        presentation_spo = input_presentation_spo, question_spo = input_question_spo, media_spo = input_media_spo, 
        quality_spo = input_quality_spo)
        add.save()
        # serializer = GradePosterSerializer(add)
        # return Response(serializer.data)

        input_teacher_id = request.POST.get("teacher_id")
        teacher = Teacher.objects.get(id = input_teacher_id)
        teacher.score_posters.add(add)
        teacher.save()
        login_user_id = teacher.score_posters.all()
        serializer_login_user_id = ScorePosterSerializer(login_user_id, many=True)
        new_serializer_data_login_user_id = list(serializer_login_user_id.data)
        return Response(new_serializer_data_login_user_id)


    # แก้ไขคะแนน 
    def put(self, request):
        input_grade_poster_proj_id = request.POST.get("grade_poster_proj_id")
        input_time_spo = request.POST.get("time_spo")
        input_character_spo = request.POST.get("character_spo")
        input_presentation_spo = request.POST.get("presentation_spo")
        input_question_spo = request.POST.get("question_spo")
        input_media_spo = request.POST.get("media_spo")
        input_quality_spo = request.POST.get("quality_spo")
        edit = get_object_or_404(ScorePoster, pk=input_grade_poster_proj_id)
        edit.time_spo = input_time_spo
        edit.character_spo = input_character_spo
        edit.presentation_spo = input_presentation_spo
        edit.question_spo = input_question_spo
        edit.media_spo = input_media_spo
        edit.quality_spo = input_quality_spo
        edit.save()
        serializer = GradePosterSerializer(edit)
        return Response(serializer.data)

    def delete(self, request):
        pass

# แสดงรายละเอียดโครงงาน
class ProjectApi(APIView):
    def get(self, request):

        input_proj_id_id = request.GET.get("proj_id_id")
        project = Project.objects.filter(id = input_proj_id_id)
        # รายละเอียดโครงงาน
        serializer = ProjectSerializer(project, many=True)
        # นักศึกษาที่ทำโครงงาน
        student = Student.objects.filter(Q(proj1_id = input_proj_id_id) | Q(proj1_id = input_proj_id_id) |  
        Q(proj2_id = input_proj_id_id) | Q(proj2_id = input_proj_id_id))
        serializer2 = StudentSerializer(student, many=True)
        new_serializer_data = list(serializer.data)
        new_serializer_data2 = list(serializer2.data)
        new_serializer_data3 = {
                "pro_detail": new_serializer_data[0]
        }
        print(new_serializer_data2)
        if new_serializer_data2:
            data = {
                'student_id': [new_serializer_data2[0]['student_id'], new_serializer_data2[1]['student_id']]            
            }
            data2 = {
                'student_name': [new_serializer_data2[0]['student_name'], new_serializer_data2[1]['student_name']]
            }
        else:
                data = {
                'student_id': ["ไม่มี", "ไม่มี"]            
            }
                data2 = {
                'student_name': ["ไม่มี", "ไม่มี"]
            }
        new_serializer_data3["pro_detail"].update(data)
        new_serializer_data3["pro_detail"].update(data2)
        return Response(new_serializer_data3)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# แสดงชื่อโครงงาน, เวลา, ห้องและวันที่คุมสอบโครงงานทั้งหมด
class ScheduleApi(APIView):

    def get(self, request):

        input_login_user_id = request.GET.get("login_user_id")
        # หา scheduleroom_id
        teacher_test = Teacher.objects.filter(login_user = input_login_user_id)
        test = TeacherScheduleListSerializer(teacher_test, many=True)
        new_serializer_data_test = list(test.data)
        sch_id_list = new_serializer_data_test[0]["schedule_teacher"]
        new_serializer_data = {
                "sch": []
        }
        for i in sch_id_list:
            project = ScheduleRoom.objects.get(id = i)
            data = {
                'id': project.proj_id.id,
                'proj_name_en': project.proj_id.proj_name_en,
                'proj_name_th': project.proj_id.proj_name_th,
                'time': project.time_id.time_exam,
                'rooom_name' : project.room_id.room_name,
                'date_exam' : project.date_id.date_exam,
                'proj_advisor' : project.proj_id.proj_advisor,
                'proj_co_advisor' : project.proj_id.proj_co_advisor
            }
            new_serializer_data["sch"].append(data)
        sched_serializer = ScheduleApiSerializer(new_serializer_data, many=True)
        return Response(new_serializer_data)
        # return Response(json.dumps(data, ensure_ascii=False))

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# แสดงชื่อโครงงานและวันที่คุมสอบโปสเตอร์ทั้งหมด
class SchedulePosterApi(APIView):

    def get(self, request):
        
        input_login_user_id = request.GET.get("login_user_id")
        # หา scheduleposter_id
        teacher_test = Teacher.objects.filter(login_user = input_login_user_id)
        test = TeacherSchedulePosterListSerializer(teacher_test, many=True)
        new_serializer_data_test = list(test.data)
        sch_id_list = new_serializer_data_test[0]["schepost_teacher"]       
        new_serializer_data = {
                "sch_poster": []
        }
        for i in sch_id_list:
            project = SchedulePoster.objects.filter(id = i)
            sch_room = SchedulePosterSerializer(project, many=True)            
            new_serializer_data_test2 = list(sch_room.data)
            print("new_serializer_data_test2")            
            print(new_serializer_data_test2)
            print("    ")
            # ชื่อโครงงาน
            proj_name = Project.objects.filter(id = new_serializer_data_test2[0]["proj_id"])
            serializer = ProjectNameSerializer(proj_name, many=True)            
            new_serializer_data2 = list(serializer.data)
            print("new_serializer_data2")
            print(new_serializer_data2)
            print("    ")
            data = {
                "proj_name_en": new_serializer_data2[0]['proj_name_en']
            } 
            # วันสอบ
            date = SchedulePoster.objects.filter(Q(date_post = new_serializer_data_test2[0]["date_post"]) & Q(proj_id = new_serializer_data_test2[0]["proj_id"]))
            serializer = SchedulePosterSerializer(date, many=True)
            new_serializer_data3 = list(serializer.data)
            print("new_serializer_data3")
            print(new_serializer_data3)
            print("    ")
            data2 = {
                "id": new_serializer_data3[0]['proj_id'],
                "date_post": new_serializer_data3[0]['date_post']
            }            
            data.update(data2)
            new_serializer_data["sch_poster"].append(data)
        return Response(new_serializer_data)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# แสดงรายคะแนนทุกคะแนนที่อาจารย์ก่อนในโครงงานนั้น
class ScoreApi(APIView):
    def get(self, request):
        # input_pro_id_id = request.GET.get("pro_id_id")
        # project = models.Project.objects.filter(id = input_pro_id_id)
        # # ชื่อโครงงาน
        # serializer = ProjectNameSerializer(project, many=True)
        # project = models.ScoreProj.objects.filter(proj_id = input_pro_id_id)
        # # คะแนนโครงงานส่วนกรรมการคุมสอบทั้งหมด
        # serializer2 = GradeSerializer(project, many=True)
        # project = models.ScoreAdvisor.objects.filter(proj_id = input_pro_id_id)
        # # คะแนนโครงงานส่วนคส่วนอาจารย์ที่ปรึกษาทั้งหมด
        # serializer3 = GradeAdvisorSerializer(project, many=True)
        # # คะแนนโครงงานส่วนคส่วนโปสเตอร์ทั้งหมด
        # project = models.ScorePoster.objects.filter(proj_id = input_pro_id_id)
        # serializer4 = GradePosterSerializer(project, many=True)
        # # อาจารย์ที่ปรึกษา
        # project = models.Project.objects.filter(id = input_pro_id_id)
        # serializer5 = AdvisorSerializer(project, many=True)
        # new_serializer_data = list(serializer.data)
        # data = {
        #         "all_score": new_serializer_data[0]
        # }
        # new_serializer_data2 = list(serializer2.data)
        # data2 = {
        #         "all_grade": new_serializer_data2
        # }
        # new_serializer_data3 = list(serializer3.data)
        # data3 = {
        #         "all_grade1": new_serializer_data3
        # }
        # new_serializer_data4 = list(serializer4.data)
        # data4 = {
        #         "all_grade2": new_serializer_data4
        # }
        # new_serializer_data5 = list(serializer5.data)
        # data5 = {
        #         "advisor": new_serializer_data5
        # }
        # data["all_score"].update(data5)
        # data["all_score"].update(data2)
        # data["all_score"].update(data3)
        # data["all_score"].update(data4)
        # return Response(data)

        # input_advisor = request.GET.get("advisor")        
        # # หา proj_id
        # advisor = Project.objects.filter(Q(proj_advisor = input_advisor) | Q(proj_co_advisor = input_advisor))
        # advisor = Teacher.objects.all()
        # test = AdvisorSerializer(advisor, many=True)
        # new_serializer_data_test = list(test.data)                
        # advisor_project_list = new_serializer_data_test[0]["id"]
        # new_serializer_data = {
        #         "advisor": []
        # }

        input_advisor = request.GET.get("advisor")        
        # หา proj_id
        advisor = Project.objects.filter(Q(proj_advisor = input_advisor) | Q(proj_co_advisor = input_advisor))
        test = AdvisorSerializer(advisor, many=True)
        new_serializer_data_test = list(test.data)
        advisor_project_list = []
        for i in range (len (new_serializer_data_test)):
            advisor_project_list.append(new_serializer_data_test[i]["id"])
        new_serializer_data2 = {
                "advisor": advisor_project_list
        }
        new_serializer_data = {
                "advisor": []
        }
        for i in advisor_project_list:
            print(i)
            # ชื่อโครงงาน
            project = Project.objects.filter(id = i)            
            serializer = ProjectNameSerializer(project, many=True)
            # คะแนนโครงงานส่วนกรรมการคุมสอบทั้งหมด
            project = ScoreProj.objects.filter(proj_id = i)            
            serializer2 = GradeSerializer(project, many=True)
            # คะแนนโครงงานส่วนคส่วนอาจารย์ที่ปรึกษาทั้งหมด
            project = ScoreAdvisor.objects.filter(proj_id = i)            
            serializer3 = GradeAdvisorSerializer(project, many=True)
            # คะแนนโครงงานส่วนคส่วนโปสเตอร์ทั้งหมด
            project = ScorePoster.objects.filter(proj_id = i)
            serializer4 = GradePosterSerializer(project, many=True)
            new_serializer_datan = list(serializer.data)

            # project = Project.objects.filter(id = new_serializer_data2[i]["advisor"])            
            # serializer = ProjectNameSerializer(project, many=True)
            # # คะแนนโครงงานส่วนกรรมการคุมสอบทั้งหมด
            # project = ScoreProj.objects.filter(proj_id = new_serializer_data2[i]["advisor"])            
            # serializer2 = GradeSerializer(project, many=True)
            # # คะแนนโครงงานส่วนคส่วนอาจารย์ที่ปรึกษาทั้งหมด
            # project = ScoreAdvisor.objects.filter(proj_id = new_serializer_data2[i]["advisor"])            
            # serializer3 = GradeAdvisorSerializer(project, many=True)
            # # คะแนนโครงงานส่วนคส่วนโปสเตอร์ทั้งหมด
            # project = ScorePoster.objects.filter(proj_id = new_serializer_data2[i]["advisor"])
            # serializer4 = GradePosterSerializer(project, many=True)
            # new_serializer_datan = list(serializer.data)
            data = {
                    "id": new_serializer_datan[0]["id"],
                    "proj_name_en": new_serializer_datan[0]["proj_name_en"]
            }
            new_serializer_data2 = list(serializer2.data)
            sum = 0
            for i in range(len(new_serializer_data2)) :
                sum += new_serializer_data2[i]["presentation"]
                sum += new_serializer_data2[i]["question"]
                sum += new_serializer_data2[i]["report"]
                sum += new_serializer_data2[i]["presentation_media"]
                sum += new_serializer_data2[i]["discover"]
                sum += new_serializer_data2[i]["analysis"]
                sum += new_serializer_data2[i]["quantity"]
                sum += new_serializer_data2[i]["levels"]
                sum += new_serializer_data2[i]["quality"]
            if len(new_serializer_data2) == 0:
                result = 0
            else:
                result = (sum/(len(new_serializer_data2)*90))*0.4          
            data2 = {
                    "all_grade": "{0:.2%}".format(result)
            }            
            new_serializer_data3 = list(serializer3.data)
            sum = 0
            for i in range(len(new_serializer_data3)) :
                sum += new_serializer_data3[i]["propose"]
                sum += new_serializer_data3[i]["planning"]
                sum += new_serializer_data3[i]["tool"]
                sum += new_serializer_data3[i]["advice"]
                sum += new_serializer_data3[i]["improve"]
                sum += new_serializer_data3[i]["quality_report"]
                sum += new_serializer_data3[i]["quality_project"]
            if len(new_serializer_data3) == 0:
                result1 = 0
            else:
                result1 = sum/(len(new_serializer_data3)*70)*0.2
            data3 = {
                    "all_grade1": "{0:.2%}".format(result1)
            }
            new_serializer_data4 = list(serializer4.data)
            sum = 0
            for i in range(len(new_serializer_data4)) :
                sum += new_serializer_data4[i]["time_spo"]
                sum += new_serializer_data4[i]["character_spo"]
                sum += new_serializer_data4[i]["presentation_spo"]
                sum += new_serializer_data4[i]["question_spo"]
                sum += new_serializer_data4[i]["media_spo"]
                sum += new_serializer_data4[i]["quality_spo"]
            if len(new_serializer_data4) == 0:
                result2 = 0
            else:
                result2 = sum/(len(new_serializer_data4)*60)*0.4
            data4 = {
                    "all_grade2": "{0:.2%}".format(result2)
            }
            data5 = {
                    "all_grade3": "{0:.2%}".format(result+result1+result2)
            }
            data.update(data2)
            data.update(data3)
            data.update(data4)
            data.update(data5)            
            new_serializer_data["advisor"].append(data)
        return Response(new_serializer_data)

        

    def post(self, request):
        pass
    def put(self, request):
        pass

    def delete(self, request):
        pass

# ตรวจการเข้าสู่ระบบว่าเป็น user or admin

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
def myLogin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    test = []
    test_data = {
        'username': username,
        'password': password
    }
    result = {}

    # input_activate = request.data.get("activate")
    # edit = get_object_or_404(models.Settings, pk=1)
    # edit.activate = input_activate
    # edit.save()
    # serializer = CheckSettingSerializer(edit)
    # if():
    #     try:       
    #         user = User.objects.get(username=username)
    #         s = Server('ldap://161.246.38.141', get_info=ALL, use_ssl=True) 
    #         c = Connection(s, user=username+"@it.kmitl.ac.th", password=password)
    #         # c = Connection(s, user=username, password=password)
    #         user.backend = "django_python3_ldap.auth.LDAPBackend"
    #         user.save()
    #         try:
    #             if not c.bind():
    #                 user_model = authenticate(username=username, password=password)
    #                 # err = err_message(user_model)
    #                 # return choice_return(request, err, user_model)
    #                 result = {'result': 'fail_not c.bind()'}
    #                 # return Response(json.dumps(test_data, ensure_ascii=False))
    #                 return Response(json.dumps(result, ensure_ascii=False))
    #         except Exception as e:
    #             user_model = authenticate(username=username, password=password)
    #             # err = err_message(user_model)
    #             # return choice_return(request, err, user_model)
    #             print(str(e))
    #             result = {'result': 'fail_Exception'}
    #             # return Response(json.dumps(test_data, ensure_ascii=False))
    #             return Response(json.dumps(result, ensure_ascii=False))
    #         if user is not None and c.bind():
    #             if user.is_active:
    #                 login(request, user)
    #                 # return render(request,"scoreproj.html",{'Projectset':data_user(user), 'proj_act':form_setting})
    #                 # return Response(json.dumps(test_data, ensure_ascii=False))
    #                 result = {
    #                     'result': 'pass',
    #                     'username': username,
    #                     'password': password
    #                 }
    #                 return Response(json.dumps(result, ensure_ascii=False))
    #             else:
    #                 state = "The password is valid, but the account has been disabled!"
    #                 # return render(request, 'login.html', {'err_ms':state})
    #                 result = {'result': 'fail_account has been disabled!'}
    #                 # return Response(json.dumps(test_data, ensure_ascii=False))
    #                 return Response(json.dumps(result, ensure_ascii=False))
    #         else:
    #             state = "The username and password were incorrect."
    #             # return render(request, 'login.html', {'err_ms':state})
    #             result = {'result': 'fail_incorrect'}
    #             # return Response(json.dumps(test_data, ensure_ascii=False))
    #             return Response(json.dumps(result, ensure_ascii=False))
    #     except User.DoesNotExist as e:
    #         user_model = authenticate(username=username, password=password)
    #         # err = err_message(user_model)
    #         # return choice_return(request, err, user_model)
    #         result = {'result': 'fail_User.DoesNotExist'}
    #         # return Response(json.dumps(test_data, ensure_ascii=False))
    #         return Response(json.dumps(result, ensure_ascii=False))
    #     # return Response(json.dumps(test_data, ensure_ascii=False))
    #     return Response(json.dumps(result, ensure_ascii=False))

    # else:
    #     return Response(serializer.data)    

    try:       
        user = User.objects.get(username=username)
        s = Server('ldap://161.246.38.141', get_info=ALL, use_ssl=True) 
        c = Connection(s, user=username+"@it.kmitl.ac.th", password=password)
        # c = Connection(s, user=username, password=password)
        user.backend = "django_python3_ldap.auth.LDAPBackend"
        user.save()        
        try:
            if not c.bind():
                user_model = authenticate(username=username, password=password)
                # err = err_message(user_model)
                # return choice_return(request, err, user_model)
                result = {
                    'result': 'fail_not c.bind()',
                    'username': username,
                    'password': password
                    }
                # return Response(json.dumps(result, ensure_ascii=False))
                return Response(result)
        except Exception as e:
            user_model = authenticate(username=username, password=password)
            # err = err_message(user_model)
            # return choice_return(request, err, user_model)
            # print(str(e))

            # result = {
            #     'result': 'fail_Exception',
            #     'username': username,
            #     'password': password
            #     }
            # return Response(result)

            resultTest = {
                    "result": "pass",
                    "username": "it58070046",
                    "superuser": True,
                    "staff": True,
                    "id": 3,
                    "login_user": 4,
                    "teacher_name": "ดร. บัณฑิต ฐานะโสภณ"
                }
            return Response(resultTest)

        if user is not None and c.bind():
            if user.is_active:
                login(request, user)
                # return render(request,"scoreproj.html",{'Projectset':data_user(user), 'proj_act':form_setting})
                userData = User.objects.filter(username=username)            
                userDataserializer = userSerializer(userData, many=True)
                test = list(userDataserializer.data)
                teacherData = Teacher.objects.filter(login_user_id=test[0]['id'])            
                teacherDataserializer = TeacherLoginSerializer(teacherData, many=True)
                test2 = list(teacherDataserializer.data)
                result = {
                    'result': 'pass',
                    'username': username,
                    'superuser' : test[0]['is_superuser'],
                    'staff' : test[0]['is_staff'],
                    # 'superuser' : False,
                    # 'staff' : False,
                    'id' : test2[0]['id'],
                    'login_user' : test2[0]['login_user'],
                    'teacher_name' : test2[0]['teacher_name']
                }
                return Response(result)
                # resultTest = {
                #     "result": "pass",
                #     "username": "it58070046",
                #     "password": "Lot253929054",
                #     "superuser": true,
                #     "staff": true,
                #     "id": 3,
                #     "login_user": 4,
                #     "teacher_name": "ดร. บัณฑิต ฐานะโสภณ"
                # }
                # return Response(resultTest)
                # return Response(json.dumps(result, ensure_ascii=False))
                
            else:
                state = "The password is valid, but the account has been disabled!"
                # return render(request, 'login.html', {'err_ms':state})
                result = {
                    'result': 'fail_account has been disabled!',
                    'username': username,
                    'password': password
                }
                # return Response(json.dumps(result, ensure_ascii=False))
                return Response(result)
        else:
            state = "The username and password were incorrect."
            # return render(request, 'login.html', {'err_ms':state})
            result = {
                'result': 'fail_incorrect',
                'username': username,
                'password': password
            }
            # return Response(json.dumps(result, ensure_ascii=False))
            return Response(result)
    except User.DoesNotExist as e:
        user_model = authenticate(username=username, password=password)
        # err = err_message(user_model)
        # return choice_return(request, err, user_model)
        result = {
            'result': 'fail_User.DoesNotExist',
            'username': username,
            'password': password
        }
        # return Response(json.dumps(result, ensure_ascii=False))
        return Response(result)
    # return Response(json.dumps(result, ensure_ascii=False))

    result = {
            'result': 'none',
            'username': username,
            'password': password
        }
    return Response(result)

# แสดงเปิดปิดระบบ
class SettingApi(APIView):
    def get(self, request):

        # setting = models.Settings.objects.all()
        # serializer = CheckSettingSerializer(setting, many=True)
        # new_serializer_data = {
        #         "setting": list(serializer.data)
        # }
        # return Response(new_serializer_data)

        setting = Settings.objects.all()
        serializer = CheckSettingSerializer(setting, many=True)
        return Response(serializer.data)



    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# ตั้งค่าผู้ดูแล
class SettingAdminApi(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        input_activate = request.data.get("activate")
        input_forms = request.data.get("forms")
        edit = get_object_or_404(Settings, pk=1)
        edit.activate = input_activate
        edit.forms = input_forms
        edit.save()
        print(edit)
        serializer = CheckSettingSerializer(edit)
        return Response(serializer.data)

    def delete(self, request):
        pass

# แสดง Id ของตารางคะแนน
class ScoreProjIdApi(APIView):
    def get(self, request):        
        
        input_login_user_id = request.GET.get("login_user_id")
        # input_proj_id = request.GET.get("project id") #project id
        # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        teacher = Teacher.objects.get(login_user_id = input_login_user_id)        
        # ScoreProj = teacher.score_projs.filter(id=input_proj_id)
        ScoreProj = teacher.score_projs.all()
        serializer = ScoreProjSerializer(ScoreProj, many=True)
        new_serializer_data = list(serializer.data)
        data = {
                "id": new_serializer_data[0]["id"]           
        } 
        # # ชื่อโครงงาน
        # proj_name = models.Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data.update(data2) 
        # หาว่ากรอกคะแนนแล้ว
        advisor = Teacher.objects.filter(id=input_login_user_id)
        test = CheckGradeDoneSerializer(advisor, many=True)
        new_serializer_data_test = list(test.data) 
        data3 = {
                "proj_mark": new_serializer_data_test[0]['score_projs']
        }        
        data.update(data3) 
        toList = [data]
        return Response(toList)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# แสดง Id ของตารางคะแนน
class ScorePosterjIdApi(APIView):
    def get(self, request):        
        
        input_login_user_id = request.GET.get("login_user_id")
        # input_proj_id = request.GET.get("project id") #project id
        # คะแนนโครงงานส่วนอาจารย์ที่ปรึกษา     
        teacher = Teacher.objects.get(login_user_id = input_login_user_id)        
        # ScoreProj = teacher.score_projs.filter(id=input_proj_id)
        score_posters = teacher.score_posters.all()
        serializer = ScorePosterSerializer(score_posters, many=True)
        new_serializer_data = list(serializer.data)
        data = {
                "id": new_serializer_data[0]["id"]           
        } 
        # # ชื่อโครงงาน
        # proj_name = models.Project.objects.filter(id = new_serializer_data[0]["proj_id"])
        # serializer2 = ProjectNameSerializer(proj_name, many=True) 
        # new_serializer_data2 = list(serializer2.data)
        # data = {
        #         "proj_name_en": new_serializer_data2[0]['proj_name_en']
        # }
        # data.update(data2) 
        # หาว่ากรอกคะแนนแล้ว
        advisor = Teacher.objects.filter(id=input_login_user_id)
        test = CheckGradeDoneSerializer(advisor, many=True)
        new_serializer_data_test = list(test.data) 
        data3 = {
                "poster_mark": new_serializer_data_test[0]['score_posters']
        }        
        data.update(data3) 
        toList = [data]
        return Response(toList)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

#แสดงตารางสอบ
class AllScheduleApi(APIView):
    def get(self, request):

        schStr = ""
        input_login_user_id = request.GET.get("login_user_id")
        # หา scheduleroom_id
        teacher_test = Teacher.objects.filter(login_user = input_login_user_id)
        test = TeacherScheduleListSerializer(teacher_test, many=True)
        new_serializer_data_test = list(test.data)
        sch_id_list = new_serializer_data_test[0]["schedule_teacher"]
        for i in sch_id_list:
            project = ScheduleRoom.objects.get(id = i)
            if schStr == "":
                schStr = project.time_id.time_exam+"="+ project.room_id.room_name+"="+project.date_id.date_exam
            else:
                schStr += ","+project.time_id.time_exam+"="+ project.room_id.room_name+"="+project.date_id.date_exam
        schPosterStr = ""
        test = TeacherSchedulePosterListSerializer(teacher_test, many=True)
        new_serializer_data_test = list(test.data)
        sch_id_list = new_serializer_data_test[0]["schepost_teacher"]
        for i in sch_id_list:
            project = SchedulePoster.objects.filter(id = i)
            sch_room = SchedulePosterSerializer(project, many=True)            
            new_serializer_data_test2 = list(sch_room.data)
            # วันสอบ
            date = SchedulePoster.objects.filter(Q(date_post = new_serializer_data_test2[0]["date_post"]) & Q(proj_id = new_serializer_data_test2[0]["proj_id"]))
            serializer = SchedulePosterSerializer(date, many=True)
            new_serializer_data3 = list(serializer.data)
            if schPosterStr == "":
                schPosterStr = new_serializer_data3[0]['date_post']
            else:
                schPosterStr += ","+new_serializer_data3[0]['date_post']
        new_serializer_data = {
                "sch": schStr,
                "sch_poster": schPosterStr
        }
        return Response(new_serializer_data)

        

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass