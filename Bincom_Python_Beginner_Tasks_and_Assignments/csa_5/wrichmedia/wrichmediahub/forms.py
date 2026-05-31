from django import forms
from django.forms import inlineformset_factory
from .models import Post, MediaItem

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Give your post a title"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional description..."
                }
            )
        }

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ["media_type", "text_content", 
                  "image_file", "audio_file", "video_file"]
        widgets = {
            "media_type": forms.Select(
                attrs={
                    "class": "form-select media-type-select"
                }
            ),
            "text_content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your text content here..."
                }
            ),
            "image_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "audio_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "video_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            )
        }


MediaItemFormSet = inlineformset_factory(
    Post,
    MediaItem,
    form=MediaItemForm,
    extra=1,
    can_delete=True
)