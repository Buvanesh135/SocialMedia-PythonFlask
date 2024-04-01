cms_set_password = """<!DOCTYPE html>
<html>
<body>

<p>Hi {user_name},</p>

  <p>Welcome to Breathefree CMS.</p>
  <p>We have created your Breathefree CMS account with the user name: {email}</p>

  <p>To set your password <a href={cms_set_password_page}>click here</a> 
</p>
<p>Regards,<br>
    Team Breathefree</p>

</body>
</html>"""

user_email_verify = """<!DOCTYPE html>
<html>
<body>
<p>Dear {user_name},</p>
<p> We noticed you were trying to link this email to your Breathefree Account. 
    Please use the OTP provided here to verify</p>
  <h4>{otp}</h4>
<p>Cheers,<br>
    Team Breathefree</p>
</body>
</html>"""
