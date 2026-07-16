from django import forms

class AdminEventEditReviewForm(forms.Form):
    admin_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add note for approval or rejection...'
        })
    )


