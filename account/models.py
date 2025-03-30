from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=[('expert', 'Expert'), ('candidate', 'Candidate'), ('admin', 'Admin')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # ✅ Changed from 'username' to 'name'

    def __str__(self):
        return self.email

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.TextField()

    def __str__(self):
        return f"{self.user.name} Info"
    

class ScoreMatchResult(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="score_results",unique=False)
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expert_scores",unique=False)
    
    education_score = models.FloatField()
    skills_score = models.FloatField()
    experience_score = models.FloatField()
    project_score = models.FloatField()
    total_score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'expert')  # Ensures each expert-candidate pair is unique

    def __str__(self):
        return f"Score ({self.total_score}) for {self.candidate.name} vs {self.expert.name}"
