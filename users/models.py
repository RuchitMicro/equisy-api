from django.db                      import models
from tenant_users.tenants.models    import UserProfile

# Signals
from django.db.models.signals       import post_save
from django.dispatch                import receiver


class TenantUser(UserProfile):
    first_name      =   models.CharField    (max_length = 100,blank = True,)
    last_name       =   models.CharField    (max_length = 100,blank = True,)
    profile_image   =   models.ImageField   (default='/profile/profile_default.jpg', upload_to='profile/')
    user_type       =   models.CharField    (max_length=20, choices=(('Tenant Owner','Tenant Owner'),('Tenant User','Tenant User'),('Support','Support'),('Developer','Developer')), default='Tenant User', null = True, blank = True)
    phone_number    =   models.CharField    (max_length = 100,blank = True,null=True)
    
    address         =   models.TextField    (null=True,blank=True)
    state           =   models.CharField    (max_length = 300, blank = True,null=True)
    city            =   models.CharField    (max_length = 300, blank = True,null=True)
    zip             =   models.CharField    (max_length = 300, blank = True,null=True)
    
    gender          =   models.CharField    (max_length=100, choices=[('Male','Male'),('Female','Female'),('Other','Other'),], null=True, blank=True)

    created_on      =   models.DateField    (auto_now_add=True)

    class Meta:
        ordering    =   ['-created_on']
