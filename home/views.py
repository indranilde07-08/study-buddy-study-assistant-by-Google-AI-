from django.shortcuts import render,redirect,get_object_or_404
from .forms import StudyMaterialForm
from .models import StudyMaterial
from django.contrib.auth.decorators import login_required
from .extract_text import extract_text_from_pdf
from .generative_summary import generate_summary
from .geneeative_quiz import generate_quiz
import sys
from django.contrib import messages



def create(request):
    form = StudyMaterialForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        study_material = form.save(commit=False)   # don't save yet
        study_material.user = request.user         # attach current user
        study_material.save()                      
        return redirect('home:view')
    return render(request, 'create.html', {'form': form})


def view(request):
    if not request.user.is_authenticated:
        return redirect('atun:signin')
    else:
        materials = StudyMaterial.objects.filter(user=request.user)
        return render(request, 'view.html', {'materials': materials})

# Create your views here.

def summary_study_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
    summary = None

    if request.method == 'POST':
        lines = int(request.POST.get('lines', 250))
        text = extract_text_from_pdf(material.pdf.path)

        if text.strip():
            summary = generate_summary(text, lines)
        else:
            summary = "No text found in the PDF."

    return render(request, "summary.html", {"material": material, "summary": summary})

def quiz_study_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
    quiz_data = None
    correct_score = 0
    wrong_score = 0
    feedback = []
    if request.method == 'POST':
        if 'generate' in request.POST:
            num_questions = int(request.POST.get('num_questions', 5))
            text = extract_text_from_pdf(material.pdf.path)
            quiz_data = generate_quiz(text, num_questions=num_questions)
            request.session['quiz_data'] = quiz_data  # Store quiz data in session
        else:
            quiz_data = request.session.get('quiz_data',[])
            for i,q in enumerate(quiz_data):
                user_answer = request.POST.get(f"q{i}")
                print(repr(user_answer[0]))
                sys.stdout.flush()
                correct_answer = q['answer']
                print(repr(correct_answer))
                sys.stdout.flush()
                if user_answer[0]  == correct_answer:
                    correct_score+=1
                    feedback.append(f"Question {i+1}: Correct")
                else: 
                    wrong_score+=1
                    feedback.append(f"Question {i+1}: Incorrect. Correct answer is {correct_answer}.{q['explanation']}")
    return render(request, "quiz.html", {"material": material, "quiz_data": quiz_data, "correct_score": correct_score, "wrong_score": wrong_score, "feedback": feedback})
def edit(request, material_id):
    material = get_object_or_404(StudyMaterial,id=material_id,user=request.user)
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST , request.FILES,instance=material)
        if form.is_valid():
            study_material=form.save(commit=False)
            study_material.user=request.user
            study_material.save()
            messages.success(request,'Material updated successfully')
            return redirect('home:view')
    else:
        form = StudyMaterialForm(instance=material)
    return render(request, 'edit.html', {'form': form})

def delete(request, material_id):
    material = get_object_or_404(StudyMaterial,id=material_id,user=request.user)
    if request.method == 'POST':
        if 'yes' in request.POST:
            material.delete()
            messages.success(request,'Material deleted successfully')
            return redirect('home:view')
        elif 'no' in request.POST:
            return redirect('home:view')
    return render(request, 'delete.html', {'material': material})