from django.contrib.auth.base_user import BaseUserManager


class CompanyUserManager(BaseUserManager):
    def create_user(self, email, company_name, phone_number, website, address, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            phone_number=phone_number,
            website=website,
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, company_name=None, phone_number=None, website=None, address=None, password=None,
                         **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            company_name=company_name,
            phone_number=phone_number,
            website=website,
            address=address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
