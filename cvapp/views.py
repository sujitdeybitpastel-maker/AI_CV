from django.shortcuts import render
from django.http import HttpResponse
# from .models import Users,Status
import hashlib
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import auth
from django.db.models import Func, F, CharField
from django.db.models.functions import Cast
from ai.generate_cv_service import generate_summary,generate_cv_pdf
import json
from load_env import *
import requests
import os

def generate_md5_hash(data_string):
    """
    Generates the MD5 hash of a given string.

    Args:
        data_string (str): The input string to be hashed.

    Returns:
        str: The 32-character hexadecimal MD5 hash of the input string.
    """
    # Create an MD5 hash object
    md5_hash_object = hashlib.md5()

    # Update the hash object with the bytes of the input string
    # It's crucial to encode the string to bytes, typically using UTF-8
    md5_hash_object.update(data_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hex_digest = md5_hash_object.hexdigest()

    return hex_digest

def get_original_id_from_hash(model, hashed_id):
    """
    Given an MD5 hash of an integer primary key,
    return the original integer ID from the database.
    """
    try:
        obj = model.objects.exclude(status='5').annotate(
            hashed_id=Func(Cast(F('id'), CharField()), function='MD5')
        ).filter(hashed_id=hashed_id).first()
        return obj.id
    except model.DoesNotExist:
        return None
    except Exception:
        return None

def index(request):
    # if not request.session.get('member_id'):
    #     return redirect('login')
    print('Working')
    return render(request, 'index.html')
    # except Exception as e:
    #     print(f"error{str(e)}")


def cv_maker(request):

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        job_role = request.POST.get("exp_role")
        exp_have = request.POST.get("exp_have")
        years_experience = request.POST.get("exp_years")
        skills = ", ".join(request.POST.getlist("skills[]"))
        project_name = request.POST.get("projects")
        summary = request.POST.get("summary")
        final_projects = request.POST.get("final_projects")
        

        print(full_name,summary,final_projects)
        context = {
            "full_name": full_name,
            "job_role": job_role,
            "years_experience": years_experience or 0,
            "skills": skills,
            "project_name": project_name,
            "exp_have": exp_have,
        }

        summary_text = generate_summary(
            provider="openai",
            user_data=context
        )
        
        print("-------summary_text-------",summary_text)

        result = json.loads(summary_text)
        summaries = result["summaries"]
        projects = result["projects"]

        return JsonResponse({
            "summaries": summaries,  # list of 5 strings
            "projects":projects
        })

        # return HttpResponse({
        #     "summary": summary_text
        # })



def cv_download(request):
    if request.method == "POST":
        # --- Collect form data ---
        context = {
            "full_name": request.POST.get("full_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "dob": request.POST.get("dob"),
            "edu_level": request.POST.get("edu_level"),
            "edu_field": request.POST.get("edu_field"),
            "edu_college": request.POST.get("edu_college"),
            "edu_year": request.POST.get("edu_year"),
            "edu_cgpa": request.POST.get("edu_cgpa"),
            "skills": ", ".join(request.POST.getlist("skills[]")),
            "exp_have": request.POST.get("exp_have"),
            "exp_years": request.POST.get("exp_years"),
            "exp_type": request.POST.get("exp_type"),
            "exp_role": request.POST.get("exp_role"),
            "exp_company": request.POST.get("exp_company"),
            "summary": request.POST.get("summary"),
            "final_projects": request.POST.get("final_projects", "").strip(),
        }

        # --- Generate PDF + get real link ---
        result = generate_cv_pdf(provider="openai", project_data=context)
        pdf_link = result.get("link")

        print("Generated PDF Link:", pdf_link)

        return JsonResponse({
            "status": "success",
            "cv_link": pdf_link,
        })

    return JsonResponse({"status": "error", "message": "POST required"}, status=400)

        # Call UseResume API
        # url = "https://useresume.ai/api/v3/resume/create"
        # USERESUME_API_KEY = os.getenv("USERESUME_API_KEY")

        # headers = {
        #     "Authorization": f"Bearer {USERESUME_API_KEY}",
        #     "Content-Type": "application/json",
        # }

        # payload = {
        #     "content": {
        #         "name": full_name,
        #         "role": exp_role or "Fresher",
        #         "email": email,
        #         "phone": phone,
        #         "address": address,
        #         "summary": summary,
        #         "education": [
        #             {
        #         "school": edu_college,
        #         "degree": edu_level,
        #         "field_of_study": edu_field,
        #         "end_date": edu_year,
        #         "grade": edu_cgpa,
        #             }
        #         ],

        #         "employment": [
        #             {
        #                 "title": exp_role or "Fresher",
        #                 "company": exp_company or "N/A",
        #                 # "location": address or "Remote",
        #                 #"start_date": "2024-01-01",
        #                 #"present": True,
        #                 "summary": (
        #                     f"Employment Type: {exp_type}, "
        #                     f"Experience: {exp_years or '0'} years."
        #                 ),
        #             }
                    
        #         ],
        #         "projects": [
        #             {   "name": "Academic Project",
        #                 "short_description": str(final_projects or "No project details provided."),
        #             }
        #         ],
        #         "skills": [{"name": s.strip(), "proficiency": "Advanced"} for s in skills.split(",") if s.strip()],
        #     },
        #     "style": {
        #         "template": "default",
        #         "template_color": "blue",
        #         "font": "inter",
        #         "page_padding": 1.54,
        #         "page_format": "a4",
        #         "date_format": "LLL yyyy",
        #         "background_color": "white",
        #         "profile_picture_radius": "rounded-full",
        #     },
        # }
        # print("-----------project payload----------------",json.dumps(payload["content"]["projects"], indent=2))
        
        # response = requests.post(url, headers=headers, json=payload)

        # # Handle the response
        # if response.status_code == 200:
        #     data = response.json()
        #     file_url = data.get("data", {}).get("file_url")
        #     print("Downloadable CV link:", file_url)

        #     if not file_url:
        #         return JsonResponse({"error": "No file URL returned"}, status=500)

        #     # Fetch the actual PDF file
        #     pdf_response = requests.get(file_url)
        #     if pdf_response.status_code == 200:
        #         filename = f"{full_name}_CV.pdf"
        #         resp = HttpResponse(pdf_response.content, content_type="application/pdf")
        #         resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        #         return resp
        #     else:
        #         return JsonResponse({"error": "Failed to fetch PDF file"}, status=500)
        # else:
        #     print("Error creating CV:", response.text)
        #     return JsonResponse({"error": "Failed to generate CV", "details": response.text}, status=500)

