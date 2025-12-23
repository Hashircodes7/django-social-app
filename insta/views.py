from django.shortcuts import render
from django.shortcuts import redirect
from insta.models import Post,Comment,Like,customusermodel,Profile,Follower
from insta.forms import userinfoform,postform,commentform
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your views here.
def homeview(request):
       
   posts = Post.objects.all()
   return render(request,'insta/index.html',{'posts':posts})

@receiver(post_save, sender=customusermodel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



def useregisterview(request):
    if request.method == 'POST':
        form = userinfoform(request.POST)
        if form.is_valid():
            user = form.save()  # saves user

            # Handle profile fields
            avatar = request.FILES.get('avatar')
            bio = request.POST.get('bio')
            if avatar:
                user.profile.avatar = avatar
            if bio:
                user.profile.bio = bio
            user.profile.save()

            return redirect('index')
    else:
        form = userinfoform()

    return render(request, 'insta/register.html', {"form": form})


             
def userloginview(request):
   if request.method=='POST':
      username=request.POST.get('username')
      password=request.POST.get('password')
        
      user=authenticate(request,username=username,password=password) 
      if user is not None: 
         login(request,user)
         return redirect('index')
      else:
         return render(request,'insta/login.html',{'error':'invalid credentials'})
   else:
       return render(request,'insta/login.html')
        
def userlogoutview(request):
   logout(request)
   return redirect('login')

class createpostview(LoginRequiredMixin,CreateView):
   model=Post
   form_class=postform
   template_name='insta/postform.html'
   success_url=reverse_lazy('index')

   def form_valid(self, form):
       form.instance.user=self.request.user
       return super().form_valid(form)
   

class updatepostview(LoginRequiredMixin,UpdateView):
   model=Post
   form_class=postform
   template_name='insta/postform.html'
   success_url=reverse_lazy('index')

   def get_queryset(self):
      return Post.objects.filter(user=self.request.user)


class confirmdeletepostview(LoginRequiredMixin,DeleteView):
   model=Post
   template_name='insta/deletepost.html'
   success_url=reverse_lazy('index')
   
   def get_queryset(self):
      return Post.objects.filter(user=self.request.user)


class postdetailview(DetailView):
   model=Post
   template_name='insta/postdetail.html'

   def get_context_data(self, **kwargs):
      context=super().get_context_data(**kwargs)
      context['comments']=self.object.comments.all()
      return context

class createcomment(LoginRequiredMixin,View):
   def post(self,request,postid):
      post=get_object_or_404(Post,id=postid)
      form=commentform(request.POST)
      if form.is_valid():
         comment=form.save(commit=False)
         comment.user=request.user
         comment.post=post
         comment.save()

      return redirect('index')

class togglecommentlike(LoginRequiredMixin,View):
   def post(self,request,commentid):
      comment=get_object_or_404(Comment,id=commentid)

      like_qs=Like.objects.filter(user=request.user,comment=comment)
      
      if like_qs.exists():
         like_qs.delete()
      else:
         Like.objects.create(user=request.user,comment=comment)

      return redirect('index')
   
class togglepostlike(LoginRequiredMixin,View):
   def post(self,request,postid):
      post=get_object_or_404(Post,id=postid)
      like_qs=Like.objects.filter(user=request.user,post=post)
      if like_qs.exists():
         like_qs.delete()
      else:
         Like.objects.create(user=request.user,post=post)

      return redirect('index')
   
class togglefollowview(LoginRequiredMixin,View):
   def post(self,request,user_id):
      user=get_object_or_404(customusermodel,id=user_id)

      qs=Follower.objects.filter(follower_user=request.user,following_user=user)
      if qs.exists():
         qs.delete()
      else:
         Follower.objects.create(follower_user=request.user,following_user=user)

      return redirect('index')