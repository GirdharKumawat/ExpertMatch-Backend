import fitz  # PyMuPDF
import json
import google.generativeai as genai
from .models import User, UserInfo, ScoreMatchResult
API ='AIzaSyBXKUWxJ0hR_DQyoJ4T2qYrWOEHfzeJheQ'
def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

def Gemini_api_call(resume_text):
 
  genai.configure(api_key=API)  
  model = genai.GenerativeModel("gemini-2.0-flash")
  prompt = f"""
  Convert the following unstructured text into a structured JSON object. Extract relevant details such as name, summary, education, projects, skills, contact information, and location. Ensure that the JSON object follows a clear hierarchy with appropriate key-value pairs.  

  ### Input:  
  {resume_text}  

  ### Output format:  
  {{
    "name": "Full Name",
    "summary": "Brief summary of the person",
    "education": [
      {{
        "degree": "Degree Name",
        "institution": "Institution Name",
        "year": "Year or Expected Graduation",
        "cgpa": "CGPA/Percentage (if available)"
      }}
    ],
    "projects": [
      {{
        "name": "Project Name",
        "technologies": ["Tech1", "Tech2"],
        "description": "Brief project description"
      }}
    ],
    "skills": {{
      "programming_languages": ["Python", "JavaScript", "C", "C++", "SQL"],
      "frameworks_libraries": ["Django", "React", "Django REST Framework"],
      "tools_technologies": ["GitHub", "Postman", "Agora RTC SDK", "Appwrite"],
      "concepts": ["OOP", "Data Structures", "Algorithms", "RESTful APIs"],
      "database": "MySQL"
    }},
    "contact": {{
      "email": "email@example.com",
      "phone": "1234567890",
      "github": "GitHubUsername",
      "location": "City, State"
    }}
  }}
  """

  response = model.generate_content(prompt)
  textresponse = response.text[response.text.index("{"):-3]
  json_response = json.loads(textresponse)
  return json_response 

def Gemini_AI_Agent(expert_resume,candidate_resume):
 
  genai.configure(api_key=API)  
  model = genai.GenerativeModel("gemini-2.0-flash")
  prompt = f"""
You are an AI system designed to compare two resumes: an **expert resume** and a **candidate resume**.  
Your objective is to assess the **relevance of the candidate's profile** in comparison to the expert's profile based on the following key parameters:  

1. **Education** – Compare the degree, field of study, institution reputation, and alignment with the expert’s background.  
2. **Skills** – Compare technical skills, programming languages, frameworks, and relevant technologies.  
3. **Experience & Projects** – Evaluate work experience, project complexity, technologies used, and industry relevance.  

### **Input:**  
**Expert Resume:**  
{expert_resume}  

**Candidate Resume:**  
{candidate_resume}  

### **Output Format:**  
Provide a structured JSON output with **scores (0 to 10)** for each parameter and an overall total score.  

```json
{{
    "name": "Candidate Name",
    "educationScore": 0.0 to 10.0,
    "skillsScore": 0.0 to 10.0,
    "experienceScore": 0.0 to 10.0,
    "projectScore": 0.0 to 10.0,
    "totalScore": educationScore + skillsScore + experienceScore + projectScore
}}

"""
  response = model.generate_content(prompt)
  textresponse = response.text[response.text.index("{"):-3]
  json_response = json.loads(textresponse)
  return json_response


def create_score_matches(user):
    try:
        print(f"Processing scores for: {user.name} ({user.role})")  # Debugging Line
        
        candidate_role = "candidate"
        expert_role = "expert"

        if user.role == candidate_role:
            experts = User.objects.filter(role=expert_role)
            candidate_resume = UserInfo.objects.get(user=user).info
            print(f"Found {experts.count()} experts.")  # Debugging Line

            for expert in experts:
                expert_resume = UserInfo.objects.get(user=expert).info
                print(f"Matching candidate {user.name} with expert {expert.name}")  # Debugging Line

                # Call AI function
                scores = Gemini_AI_Agent(expert_resume, candidate_resume)
                print(f"AI Response: {scores}")  # Debugging Line

                # Save result
                ScoreMatchResult.objects.create(
                    candidate=user,
                    expert=expert,
                    education_score=scores.get("educationScore", 0.0),
                    skills_score=scores.get("skillsScore", 0.0),
                    experience_score=scores.get("experienceScore", 0.0),
                    project_score=scores.get("projectScore", 0.0),
                    total_score=scores.get("totalScore", 0.0)
                )

        elif user.role == expert_role:
            candidates = User.objects.filter(role=candidate_role)
            expert_resume = UserInfo.objects.get(user=user).info
            print(f"Found {candidates.count()} candidates.")  # Debugging Line

            for candidate in candidates:
                candidate_resume = UserInfo.objects.get(user=candidate).info
                print(f"Matching expert {user.name} with candidate {candidate.name}")  # Debugging Line

                # Call AI function
                scores = Gemini_AI_Agent(expert_resume, candidate_resume)
                print(f"AI Response: {scores}")  # Debugging Line

                # Save result
                ScoreMatchResult.objects.create(
                    candidate=candidate,
                    expert=user,
                    education_score=scores.get("educationScore", 0.0),
                    skills_score=scores.get("skillsScore", 0.0),
                    experience_score=scores.get("experienceScore", 0.0),
                    project_score=scores.get("projectScore", 0.0),
                    total_score=scores.get("totalScore", 0.0)
                )

    except Exception as e:
        print(f"Error creating match scores: {e}")  # Debugging Line

    try:
        candidate_role = "candidate"
        expert_role = "expert"

        if  user.role == candidate_role:
            experts = User.objects.filter(role=expert_role)
            candidate_resume = UserInfo.objects.get(user=user).info

            for expert in experts:
                expert_resume = UserInfo.objects.get(user=expert).info

                # Call AI function to calculate scores
                scores = Gemini_AI_Agent(expert_resume, candidate_resume)  # Already a dict

                if not ScoreMatchResult.objects.filter(candidate_id=candidate.id, expert_id=expert.id).exists():
                  ScoreMatchResult.objects.create(
                      candidate=user,
                      expert=expert,
                      education_score=scores.get("educationScore", 0.0),
                      skills_score=scores.get("skillsScore", 0.0),
                      experience_score=scores.get("experienceScore", 0.0),
                      project_score=scores.get("projectScore", 0.0),
                      total_score=scores.get("totalScore", 0.0)
                  )

        elif user.role == expert_role:
            candidates = User.objects.filter(role=candidate_role)
            expert_resume = UserInfo.objects.get(user=user).info

            for candidate in candidates:
                candidate_resume = UserInfo.objects.get(user=candidate).info

                # Call AI function to calculate scores
                scores = Gemini_AI_Agent(expert_resume, candidate_resume)  # Already a dict

                # Save the result
                if not ScoreMatchResult.objects.filter(candidate_id=candidate.id, expert_id=expert.id).exists():
                  ScoreMatchResult.objects.create(
                      candidate=candidate,
                      expert=user,
                      education_score=scores.get("educationScore", 0.0),
                      skills_score=scores.get("skillsScore", 0.0),
                      experience_score=scores.get("experienceScore", 0.0),
                      project_score=scores.get("projectScore", 0.0),
                      total_score=scores.get("totalScore", 0.0)
                  )

    except Exception as e:
        print(f"Error creating match scores: {e}")