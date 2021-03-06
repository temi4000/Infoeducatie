import json
from io import BytesIO
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, CommentForm, FilterForm
from .forms import CreateCosForm, CreateComandaForm
from  .models import CHOICES_UM
from .models import PostModel, Comment, CosulMeu, AdresaDeFacturare
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from authentication.models import Account2
from user_profile.models import Profile, Message
from user_profile.forms import CreateMesajeForm

@login_required(login_url='/login')
def create_post(request):
    current_user = request.user
    try:
        profil = Profile.objects.get(user=current_user)
    except:
        return redirect('/create-profile')
    form = CreatePostForm(request.POST or None, request.FILES or None,user=current_user.account2)
    if request.method == 'POST':
        if form.is_valid():
            post = form.instance
            post.author = current_user
            form.save()
            subject = 'Creare anunt'
            html_message = render_to_string('mail_template.html', {
                'message': 'Anuntul dumneavoastra a fost creat. '
                           'Acesta va trebui verificat de un administrator'
                           ' inainte ca el sa fie vizualizat pe site.'})
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_list = [settings.EMAIL_HOST_USER, current_user.email]
            send_mail(subject, plain_message, from_email, to_list,
                      html_message=html_message, fail_silently=True)
            messages.success(request, 'Anuntul dumneavoastra a fost salvat. '
                                      'Va rugam sa asteptati cateva momente '
                                      'pana cand acesta va fi verificat de '
                                      'catre un administrator. Va multumim!')
    return render(request, "create_post.html", {
        'form': form,
        'user':request.user
    })


def get_post(request, slug):
    post = get_object_or_404(PostModel,slug=slug)
    comm_parent = Comment.objects.filter(is_parent=True).filter(post=post)
    profiles = Profile.objects.all().get(user=post.author)
    form2 = CreateCosForm(request.POST)
    if request.method == "POST" and 'btnform1' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            parent_obj = None
            try:
                parent_id = Comment.objects.get(id=int(request.POST.get("parent_id")))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id.id)
                if parent_qs:
                    parent_obj = parent_qs.first()
                    comment.is_parent = False
                else:
                    comment.is_parent = True
            comment.post = post
            comment.user = request.user
            comment.parent = parent_obj
            comment.save()
        else:
            return redirect('/login')
    if request.method == "POST" and 'btnform2' in request.POST:
        if form2.is_valid() and request.user.is_authenticated:
            cos = form2.instance
            cos.anunturi = post
            cos.cumparator = request.user
            cos.vanzator = post.author
            form2.save()
            messages.success(request, 'Produsul a fost adaugat in cos')
        else:
            return redirect('/login')
    return render(request, 'Post-page.html', {
        'posts':post ,
        'user':request.user,
        'profiles':profiles,
        'comm_parent':comm_parent,
        'form2': form2
    })


@login_required(login_url='/login')
def delete_post(request, slug):
    PostModel.objects.filter(slug=slug).delete()
    return redirect('/')


@login_required(login_url='/login')
def produsele(request):
    current_user = request.user
    cosul = CosulMeu.objects.all().filter(cumparator = current_user)
    query = request.GET.get("q")
    if query:
        cosul = cosul.filter(name__contains=query)
    return render(request, 'cosul_meu.html', {
        'user':current_user,
        'cosul':cosul
    })

@login_required(login_url='/login')
def delete_cos(request, slug):
    CosulMeu.objects.filter(slug=slug).delete()
    return redirect('/cosul-meu')

@login_required(login_url='/login')
def get_comanda(request,slug):
    current_user = request.user
    comanda = PostModel.objects.get(slug=slug)
    form = CreateComandaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid() and request.user.is_authenticated:
            comanda1 = form.instance
            comanda1.creator = current_user
            comanda1.posesor = comanda.author
            comanda1.postcomanda = comanda
            form.save()
            return redirect(comanda.get_finalizare_url())
        else:
            return redirect('/login')
    return render(request, 'detalii_comanda.html', {
        'user':current_user,
        'form':form
    })


@login_required(login_url='/login')
def comanda(request):
    current_user = request.user
    comenzi2 = AdresaDeFacturare.objects.all().filter(creator = current_user.account.user)
    profil = Profile.objects.all()
    query = request.GET.get("q")
    if query:
        comenzi2 = comenzi2.filter(name__contains=query)
    return render(request, 'comenzi.html',{
        'user':current_user,
        'comenzi2':comenzi2,
        'profil':profil
    })


@login_required(login_url='/login')
def delete_comanda(request, slug):
    comandar = AdresaDeFacturare.objects.filter(slug=slug).first()
    a = comandar.postcomanda.price
    b = comandar.postcomanda.quantity
    c = a * b
    data = {
        'anunt':comandar.postcomanda.name,
        'pret': comandar.postcomanda.price,
        'cantitate':comandar.postcomanda.quantity,
        'cumparator1':comandar.nume,
        'cumparator2':comandar.prenume,
        'email':comandar.email,
        'nrdetelefon':comandar.nrdetelefon,
        'localitate':comandar.localitate,
        'judet':comandar.judet,
        'adresa': comandar.adresa,
        'vanzator1':comandar.posesor.first_name,
        'vanzator2':comandar.posesor.last_name,
        'oras':comandar.posesor.account2.city,
        'judeet':comandar.posesor.account2.state,
        'adresa2': comandar.posesor.account2.adress,
        'email2': comandar.posesor.email,
        'nrdetelefon2': comandar.posesor.account2.phonenumber,
        'total':c,
    }
    from django.template.loader import get_template
    template_object = get_template('invoice.html')
    html = template_object.render(data)
    from StringIO import StringIO
    pdf_file = StringIO()
    from xhtml2pdf import pisa
    pisa.CreatePDF(html.encode(), pdf_file, encoding='UTF-8')
    from django.core.mail import EmailMessage
    subject="Factura comanda"
    message="Comanda dumneavoastra: %s a fost incheiata cu succes " \
            "de catre %s." %(comandar.postcomanda.name, comandar.posesor)
    from_email = settings.EMAIL_HOST_USER
    to_list = [settings.EMAIL_HOST_USER, comandar.email]
    mail = EmailMessage(subject, message, from_email, to_list)
    mail.attach('factura.pdf', pdf_file.getvalue(), 'application/pdf')
    mail.send()
    AdresaDeFacturare.objects.filter(slug=slug).delete()
    return redirect('/')


@login_required(login_url='/login')
def get_finalizare(request, slug):
    current_user = request.user
    comanda = PostModel.objects.get(slug=slug)
    subject = 'Efectuare comanda'
    html_message = render_to_string('mail_template.html', {
        'message': 'Comanda dumneavoastra a fost realizata. Aceasta va ajunge'
                   ' la dumneavoastra in cel mai scurt timp. Daca comanda nu a'
                   ' ajuns la dumneavoastra in cel mult o saptamana, va rugam '
                   'sa ne contactati'})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_list = [settings.EMAIL_HOST_USER, current_user.email]
    send_mail(subject, plain_message, from_email, to_list,
              html_message=html_message, fail_silently=True)
    return render(request, "finalizare_comanda.html", {
        'user':current_user,
        'comanda':comanda
    })

@login_required(login_url='/login')
def get_comandap(request, slug):
    current_user = request.user
    anunturi = PostModel.objects.all()
    user2 = get_object_or_404(Account2, slug=slug)
    profiles = Profile.objects.all().filter(user=user2.user)
    comandar = AdresaDeFacturare.objects.all().filter(posesor=current_user)
    form4 = CreateMesajeForm(request.POST or None)
    if request.method == 'POST':
        if form4.is_valid() and 'btnform4' in request.POST:
            mesaj = form4.instance
            mesaj.autor = current_user
            form4.save()
            messages.success(request, 'Mesajul dumneavoastra a fost trimis')
    query = request.GET.get("q")
    if query:
        anunturi = anunturi.filter(name__contains=query)
    return render(request, 'view-profilee-comenzi.html', {
        'user': current_user,
        'anunturi': anunturi,
        'profiles': profiles,
        'form4':form4,
        'user2': user2,
        'comenzi2':comandar
    })

@login_required(login_url='/login')
def get_comandat(request, slug):
    current_user = request.user
    anunturi = PostModel.objects.all()
    user2 = get_object_or_404(Account2, slug=slug)
    profiles = Profile.objects.all().filter(user=user2.user)
    comandar = AdresaDeFacturare.objects.all().filter(creator=current_user)
    query = request.GET.get("q")
    if query:
        anunturi = anunturi.filter(name__contains=query)
    return render(request, 'view-profilee-comenzi-t.html', {
        'user': current_user,
        'anunturi': anunturi,
        'profiles': profiles,
        'user2': user2,
        'comenzi2':comandar
    })

def posts_filter(request):
    POST = json.loads(request.body)
    form = FilterForm(data=POST)
    if form.is_valid():
        sort_by = int(POST.get("sort_by", 0))
        products = POST.get("products", [])
        um = POST.get("um", None)
        min_quantity = POST.get("min_quantity", None)
        max_quantity = POST.get("max_quantity", None)
        min_price = POST.get("min_price", None)
        max_price = POST.get("max_price", None)
        qs = PostModel.objects.all()
        if len(products) > 0:
            qs = qs.filter(product_type__in=products)

        if um:
            qs = qs.filter(um=um)
            if min_quantity:
                qs = qs.filter(quantity__gt=min_quantity)
            if max_quantity:
                qs = qs.filter(quantity__lt=max_quantity)

        if min_price:
            qs = qs.filter(price__gt=min_price)
        if max_price:
            qs = qs.filter(price__lt=max_price)

        if sort_by is 0:
            qs = qs.order_by("author")
        elif sort_by is 1:
            qs = qs.order_by("price")
        elif sort_by is 2:
            qs = qs.order_by("-price")
        else:
            qs = qs.order_by("+name")
        return render(request, 'post_list_content.html', {
            'posts': list(qs)
        })
    else:
        print(form.errors)
