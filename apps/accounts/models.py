# Create your models here.

# class AccountDetailPermission(models.Model):
#     user = models.ForeignKey('Account')
#     email = models.CharField(max_length=3, choices=ACCOUNT_PERMISSION_CHOICES,
#                              default=ACCOUNT_PERMISSION_CHOICES[0][0])


# class OauthAccount(models.Model):
#     user = models.ForeignKey('accounts.Account', related_name='oauth', on_delete=models.CASCADE)
#     provider = models.CharField(max_length=32)
#     access_token = models.CharField(max_length=255)
#     refresh_token = models.CharField(max_length=255)
#     id_token = models.CharField(max_length=255)
#     expires_in = models.DateTimeField()
#     token_type = models.CharField(max_length=255)
