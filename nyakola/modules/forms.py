from django import forms

class ModuleForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=100)
    cover = forms.ImageField() # Otomatis validasi gambar

    # Tambahkan validasi custom kalau mau
    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 3:
            raise forms.ValidationError("Judul terlalu pendek!")
        return data