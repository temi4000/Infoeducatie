from django import forms
from .models import PostModel, Comment, CosulMeu
from category.models import Category
from categorie.models import Categorie
from lfcat.models import Lfcategory
from django.shortcuts import get_object_or_404

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['name', 'delivery_time', 'cantity', 'price', 'details', 'image1', 'image2','image3','image4','category','categorie','lfcategory']
        widgets = {
            'image1': forms.FileInput({'required': 'required', 'placeholder': "Image1"}),
            'image2': forms.FileInput({'required': 'required', 'placeholder': "Image2"}),
            'image3': forms.FileInput({'required': 'required', 'placeholder': "Image3"}),
            'image4': forms.FileInput({'required': 'required', 'placeholder': "Image4"})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreatePostForm, self).__init__(*args, **kwargs)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price.isdigit() == False:
            raise forms.ValidationError("Invalid price")
        return price

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.isdigit():
            raise forms.ValidationError("Name contains invalid characters")
        return name

    def clean_details(self):
        details = self.cleaned_data['details']
        return details

    def clean_image4(self):
        image1 = self.cleaned_data['image1']
        image2 = self.cleaned_data['image2']
        image3 = self.cleaned_data['image3']
        image4 = self.cleaned_data['image4']
        image_names = []
        if (image1 and not isinstance(image1, (int, float))):
            image_names.append(image1.name)
        if (image2 and not isinstance(image2, (int, float))):
            image_names.append(image2.name)
        if (image3 and not isinstance(image3, (int, float))):
            image_names.append(image3.name)
        if (image4 and not isinstance(image4, (int, float))):
            image_names.append(image4.name)
        if (len(image_names) - 1 == len(set(image_names))):
            raise forms.ValidationError("You can't upload 2 images"
                                        "that are the same")
        return image4

    def clean_category(self):
        category = get_object_or_404(Category,
                                     name=self.cleaned_data['category'])
        return category

    def clean_categorie(self):
        categorie = get_object_or_404(Categorie,
                                     name=self.cleaned_data['categorie'])
        return categorie

    def clean_lfcategory(self):
        lfcategory = get_object_or_404(Lfcategory,
                                       name=self.cleaned_data['lfcategory'])
        return lfcategory

    def clean_cantity(self):
        cantity = self.cleaned_data['cantity']
        if cantity.isdigit() == False:
            raise forms.ValidationError("Invalid cantity")
        return cantity

    def clean_deliverytime(self):
        delivery_time = self.cleaned_data['delivery_time']
        if delivery_time.isdigit() == False:
            raise forms.ValidationError("Invalid delivery time")
        return delivery_time


class DeleteNewForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = []


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']


class CreateCosForm(forms.ModelForm):
    class Meta:
        model = CosulMeu
        fields = []

    def  __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateCosForm, self).__init__(*args, **kwargs)
