Kazamér Zsolt - Project Library

In order to properly use the application, you need to create the tables first. Assuming that you have a PostreSQL server already availabl and you have the necessary Python modules installed, please run the following scripts in the following order:
/database_scripts/create_books.py
/database_scripts/create_users.py
/database_scripts/create_admin_user.py

Once the database is created, you can start populating it with users and books.
Upon starting the application, you will find a main menu. I would recommend registering a couple of users to try the functionalities.

IMPORTANT:
Some actions can be done only by using the admin user. The credentials are hardcoded the password - just like every password - is stored as a hash value.
Username:
admin@admin.com
Password:
admin

If you login to this account in the main menu, you will find yourself in the admin screen. Here, you can manipulate the users and not the books. Books can be manipulated by the users. The admin can reset a user password, it can unlock an account (if the login attempt reaches 3, then the account is considered locked), also the admin user can give and revoke change access to books.

Signing up a user should be obvious. Exceptions are handled and tested. Theoretically, you cannot register a user with wrong values. Same goes for books.

Please note that if you fail to login 3 times in a row, your account will be locked and you need to contact the admin to unlock it. If you fail to login once or twice then you manage to login correctly then your login attempts will be reset to 0.

As an enduser, you can add books to the inventory if you have change access. Also, you can search for books - this is the default access for everyone. After searching for books successfully, you can save the file in xlsx.

Enjoy it