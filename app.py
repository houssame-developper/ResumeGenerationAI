import os
from typing import Optional
from fastapi import FastAPI,BackgroundTasks, HTTPException,Form,UploadFile,File
from fastapi.responses import  FileResponse,Response
from fastapi.middleware.cors import CORSMiddleware
from models import DownloadToken, Resume
from resumeflows import create_file_pdf
from sqlmodel import create_engine, Session,select,SQLModel
from uuid import uuid4
from shutil import copyfileobj
engine = create_engine('sqlite:///db.sqlite')

app = FastAPI()
SQLModel.metadata.create_all(engine)
origins = [
"https://resumecv-generation-ai-psi.vercel.app/",
"https://resumecv-generation-ai-psi.vercel.app"
]
# تفعيل CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_image( photo: UploadFile):
   photo_path = ""
   if photo.filename:
           # حفظ الصورة
      photo_path = f"images/{photo.filename}"
      os.makedirs("images", exist_ok=True)
      with open(photo_path, "wb") as buffer:
        copyfileobj(photo.file, buffer)
   return  photo_path   
   

@app.post('/resume/create')
async def create_resume(
    name: str = Form(""),
    job: str = Form(""),
    phone: str = Form(""),
    location: str = Form(""),
    links: str = Form(""),
    profile: str = Form(""),
    education: str = Form(""),
    skills: str = Form(""),
    languages: str = Form(""),
    courses: str = Form(""),
    experience: str = Form(""),
    notice: str = Form(""),
    photo: UploadFile = File()  # هنا نستقبل الصورة
):  
    photo_path = upload_image(photo)
    

    # تخزين السيرة الذاتية
    with Session(engine) as session:
        resume = Resume(
            name=name,
            job=job,
            phone=phone,
            location=location,
            links=links,
            profile=profile,
            education=education,
            skills=skills,
            languages=languages,
            courses=courses,
            experience=experience,
            notice=notice,
            photo=photo_path  # مسار الصورة وليس الملف
        )
        session.add(resume)
        session.commit()
        session.refresh(resume)

        token = DownloadToken(token=str(uuid4()), user_id=resume.id)
        session.add(token)
        session.commit()

        return {"token": token.token}
        

@app.get('/user/{token}')
def donwloadFile(token: str,background_tasks: BackgroundTasks):
 try:
   with Session(engine) as session:
    stmt = select(DownloadToken).where(DownloadToken.token == token)   
    result = session.exec(stmt).first()
    if not result :
       return {'response':"Invalid token"}
    resume = session.get(Resume,result.user_id)
    if not resume :
       return {'response':"resume(cv) not found"}    
    file_path = create_file_pdf(resume)
    background_tasks.add_task(os.remove,file_path)
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename='resume.pdf',
        headers={
            "Content-Disposition": f"inline; filename=resume.pdf"
        }
    )
 except Exception as  e :
    return {"response": str(e)}

@app.get('/resume/{token}')
def getDataResume(token: str):
 try:
   with Session(engine) as session:
    stmt = select(DownloadToken).where(DownloadToken.token == token)   
    result = session.exec(stmt).first()
    if not result :
       return {'response':"Invalid token"}
    resume = session.get(Resume,result.user_id)
    if not resume :
       return {'response':"resume(cv) not found"} 
    return {'response':resume}
 except Exception as  e :
    return {"response": str(e)}
 

# دالة لحذف الصورة القديمة
def delete_file_if_exists(file_path: Optional[str]):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

@app.put('/resume/update/{resume_id}')
async def update_resume(
    resume_id: int,
    name: Optional[str] = Form(None),
    job: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    links: Optional[str] = Form(None),
    profile: Optional[str] = Form(None),
    education: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    languages: Optional[str] = Form(None),
    courses: Optional[str] = Form(None),
    experience: Optional[str] = Form(None),
    notice: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(),
):
    with Session(engine) as session:
        resume = session.get(Resume, resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        # حذف الصورة القديمة إن تم رفع صورة جديدة
        if photo and photo.filename:
            delete_file_if_exists(resume.photo)
            resume.photo = upload_image(photo)

        # تحديث باقي الحقول إن وُجدت
        fields_to_update = {
            "name": name,
            "job": job,
            "location": location,
            "phone": phone,
            "links": links,
            "profile": profile,
            "education": education,
            "skills": skills,
            "languages": languages,
            "courses": courses,
            "experience": experience,
            "notice": notice
        }

        for field, value in fields_to_update.items():
            if value is not None:
                setattr(resume, field, value)

        session.add(resume)
        session.commit()
        session.refresh(resume)

    return Response(status_code=200)
