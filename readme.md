Instructions And Setup-
Command to install libs :/<br>
    pip install flask<br>
    pip install flask-mysqldb<br>
    pip install mysql<br>

<strong>Make sure to install MySQL Suite and Workbench</strong><br><br>

MySQL setup - 

1. Create Schema: drip.inc<br><br>
2. Create 3 tables - accounts, product, cart.<br>
    1. Accounts setup - <br>
        View setup - go to "/static/setup/account-setup.png"<br>
    2. Product setup - <br>
        View setup - go to "/static/setup/product-setup.png"<br>
    3. Cart setup - <br>
        View setup - go to "/static/setup/cart-setup.png"<br><br>
3. Table Setup<br>
    1. Product setup - <br>
        View setup - go to "/static/setup/product-setup2.png"<br>
    2. Cart Setup - <br>
        View setup - go to "/static/setup/cart-setup2.png" <br>
        Make sure to include [] in productsid column<br>
        ID and userid is manually inputted by the number of users<br>
<br>

Run drip.py and open 127.0.0.1:5000