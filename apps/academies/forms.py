from django import forms
from .models import Academy, Coach

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ['name', 'description', 'location', 'city', 'sport', 'fees', 'coach_name', 'coach_experience', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 h-32'}),
            'location': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'sport': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fees': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'coach_name': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'coach_experience': forms.NumberInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'sport', 'experience']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-purple-500'}),
            'sport': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-purple-500'}),
            'experience': forms.NumberInput(attrs={'class': 'w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-purple-500'}),
        }
