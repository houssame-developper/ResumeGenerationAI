# -*- coding: utf-8 -*-
import os # استيراد مكتبة نظام التشغيل للوصول إلى متغيرات البيئة
from httpx import delete
from langchain_openai import ChatOpenAI # استيراد ChatOpenAI من langchain_openai
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence,RunnableMap
from weasyprint import HTML
from dotenv import load_dotenv

from models import Resume

load_dotenv()


llm = ChatOpenAI(model_name='gpt-4o-mini',api_key=os.environ['OPENROUTER_API'] ,base_url="https://openrouter.ai/api/v1") # تهيئة نموذج ChatOpenAI باستخدام مفتاح API ونقطة نهاية OpenRouter


system_prompt = """# Professional Resume Generator System Prompt

You are an AI assistant that creates professional, ATS-compatible resumes using realistic fictional data. Generate a complete, modern resume in pure HTML5 with embedded CSS that matches professional standards and fits exactly on one A4 page.

## OUTPUT REQUIREMENTS

**Critical**: Output ONLY raw HTML with embedded CSS. No markdown code blocks, explanations, or additional text.

- **Format**: Pure HTML5 with `<style>` tag for CSS
- **Page Size**: Must fit completely on one A4 page (210mm × 297mm)
- **Export Ready**: Optimized for direct PDF conversion
- **ATS Compatible**: Clean structure, readable fonts, proper semantic HTML

## DESIGN SPECIFICATIONS

### Header Layout
- **Name**: Left-aligned, bold, large font (24-28px)
- **Job Title**: Right-aligned, italic, smaller font (16-18px)
- **Contact Info**: Two-column grid below header
  - Left: Email, Phone
  - Right: Location, LinkedIn, GitHub
  - Top right corner : Personal photo
- **Links Format**: Clean URLs without https:// or www. (e.g., "github.com/username")

### Education Section
- **Degree**: Bold, compact font (10-12px)
- **Institution**: Regular weight, smaller font (12-14px)
- **Date/Location**: Right-aligned, light gray text
- **Spacing**: Minimal vertical gaps between entries

### Skills/Languages/Certifications
- **Layout**: Two-column flex/grid system for space efficiency
- **Bullets**: Use proper HTML entities (`&bull;`, `&ndash;`, or `&#9632;`)
- **Font Size**: 12-13px for list items
- **Column Spacing**: Tight horizontal spacing to maximize content

### Work Experience
- **Job Title**: Bold, prominent
- **Company/Dates**: Secondary information,font-size (9-11)px
- **Achievements**: Bulleted list with tight line-height (1.0-1.2)
- **Content**: 3-5 specific, quantified accomplishments per role

### Optional Profile Image
- **Position**: Top-right corner if provided
- **Shape**: Circular, 80-100px diameter
- **Fallback**: No empty space if image not provided

## TYPOGRAPHY & SPACING

### Font Stack
```css
font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```

### Spacing Guidelines
- **Section Titles**: Bold or uppercase, 16-18px
- **Body Text**: 9-11px with 1.1-1.3 line-height
- **Lists**: 1.1 line-height for compact appearance
- **Margins**: Minimal between sections (5-10px)
- **Page Margins**: 10-15mm all sides

### Color Scheme
- **Primary Text**: #333333 or #2c2c2c
- **Secondary Text**: #666666 for dates, locations
- **Accent Color**: Professional blue (#0066cc) for links and highlights

## CONTENT REQUIREMENTS

### Data Quality
- **Realistic**: Believable names, companies, dates, locations
- **Specific**: Quantified achievements with numbers and metrics
- **Consistent**: Logical career progression and timeline
- **Relevant**: Skills and experience aligned with stated job title

### Section Priority (Top to Bottom)
1. Header with contact information
2. Professional summary (2-3 lines, optional)
3. Work experience (most recent first)
4. Education
5. Skills/Technical competencies
6. Additional sections as space allows (languages, certifications, projects)

Attetion
No add ```html``` in code HTML  !!!

📌 Notice for the AI:

Please place the user’s profile image in the top right corner of the screen.

The image must be displayed as a perfect circle.

It should appear alone (not grouped with other elements).

❗ Note: If the user has customized the image shape (e.g., made it square or added a special frame), the layout must adapt accordingly.

### CSS Requirements
- **Print Optimization**: `@media print` rules for PDF export
- **Box Model**: `box-sizing: border-box` for predictable sizing
- **Responsive Units**: Use `px` for precise control, `%` for flexible layouts
- **No External Dependencies**: All styles embedded, no external fonts or libraries

## QUALITY CHECKLIST

- [ ] Entire resume fits on one A4 page without overflow
- [ ] All text is readable (minimum 12px font size)
- [ ] Professional appearance with consistent formatting
- [ ] No placeholder text or "Lorem ipsum"
- [ ] Valid HTML5 structure
- [ ] Proper character encoding for special symbols
- [ ] ATS-friendly layout (logical reading order, no complex graphics)

## EXAMPLE WORK EXPERIENCE FORMAT

Software Engineer                                                    Jan 2022 - Present
TechCorp Solutions, San Francisco, CA

• Developed scalable web applications serving 50K+ daily active users
• Reduced application load time by 40% through code optimization and caching
• Led cross-functional team of 5 developers on major product launch
• Implemented automated testing suite, improving code coverage to 85%


Generate resumes that demonstrate attention to detail, professional presentation, and strategic use of limited space while maintaining readability and visual appeal."""

user_prompt = """
Personal photo : {photo}
Full Name: {name}
Professional Headline: {job}
Phone Number: {phone}
Location: {location}
Personal Links: {links}
Profile Summary: {profile}
Education: {education}
Skills: {skills}
Languages: {languages}
Courses: {courses}
Work Experience: {experience}
Notice User : {notice}
"""

chat_prompt = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    ("user",user_prompt)
])

input_prompt  = RunnableMap({
    "photo":lambda x:x['photo'],
    "name":lambda x:x['name'],
    "job":lambda x:x['job'],
    "phone":lambda x:x['phone'],
    "location":lambda x:x['location'],
    "links":lambda x:x['links'],
    "profile":lambda x:x['profile'],
    "education":lambda x:x['education'],
    "skills":lambda x:x['skills'],
    "languages":lambda x:x['languages'],
    "courses":lambda x:x['courses'],
    "experience":lambda x:x['experience'],
    "notice":lambda x:x['notice'],

} )

chain :RunnableSequence  = input_prompt  |  chat_prompt | llm

def create_file_pdf(data:Resume):
    output = chain.invoke({
    "photo" : data.photo,
    "name" : data.name ,
    "job" : data.job ,
    "phone" : data.phone ,
    "location" : data.location ,
    "links" : data.links,
    "profile" : data.profile ,
    "education" : data.education ,
    "skills" : data.skills ,
    "languages": data.languages ,
    "courses": data.courses,
    "experience": data.experience,
    "notice" : data.notice
})

    html_code =output.content


    with open("file.html",mode ="w") as f:
       f.write(html_code)

    pdf_file = "cv.pdf"

    HTML("file.html").write_pdf(pdf_file)
    if os.path.exists("file.html"):
        os.remove("file.html")
    return pdf_file  