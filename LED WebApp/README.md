### LED WebApp

I have created a web-app that allows, if started by a raspberry, a registered user to control the switching on and off of some LEDs thanks to a graphic interface.
In the code, the commands of the GPIO library, therefore the one to make the raspberry execute the commands, are commented. Keeping those commands commented, the application writes only to the HOSTED LOCATED DATABASE, thus simulating the operation of the whole program
#### 1. HOMEPAGE:
On the homepage, you can register if you are a new user or log in if the user has already registered in the past.
Registration requires name, surname, gender, city of residence, email and password, the latters will be used as login credentials.
All this information will be saved on a MySQL database, therefore relational.
The passwords are saved in clear text but I should have saved them in the database encrypted with an algorithm (eg. md5), during the registration phase it will also be checked if the same email with the same password is already registered.
For the login of an already registered user, the program compares the email and password entered by the user with those present in the database, if it finds a match then it allows the user to access, otherwise an operation failed screen appears from which you can return to the homepage
<img src=https://user-images.githubusercontent.com/102221403/199808262-3932a792-2627-4dbc-94be-03c25dbd851a.png>
<img src=https://user-images.githubusercontent.com/102221403/199808463-eb89d34b-8ef8-497b-bbe7-763a25cf0fed.png width="500" height="500">
<img src=https://user-images.githubusercontent.com/102221403/199808486-19aef4c7-0f62-4d6c-8fc6-4b828b09ea11.png width="500" height="500">


#### 2. PAGE LED:
This is the page that a user can access after being authenticated, in this page there will be the representation of the 3 LEDs to be turned on or off in the form of buttons, a button to see the table of all the actions done by that user and a logout button.
The 3 LEDs connected to the raspberry can only light up one at a time so for example if the red LED is on and the user clicks on the button to turn on the blue, the program will first turn off the red and then turn on the blue.
The actions performed by the user such as login and logout and the switching on and off of the buttons are all saved on the database with an id and the day and time in which they were performed.
Thanks to this it was possible to implement a Machine Learning algorithm specifically a KNN to recommend an action that the user could take.
To view the table of activities for each user, the application make a
query where it selects all the fields of the activities table and sorts it by id in descending order.
To log out I made use of the flask sessions together with the user id, and to log out I use the pop command together with the user id so that it removes it from the session and then the application returns to the homepage.
![image](https://user-images.githubusercontent.com/102221403/199808958-8c2e0b00-fd57-4559-9069-d1a10a97f245.png)
![image](https://user-images.githubusercontent.com/102221403/199809111-410104f1-75b9-4aa6-87e7-c561b8b0d48b.png)


#### 3. KNN:
I implemented a KNN from scratch, so without using libraries and using only python lists and dictionaries, therefore without numpy or pandas, this is because such large libraries would be too heavy for the raspberry.
For the implementation, I select, through a query, the date and time of the action and the LED on of the current user, then I omit all the fields of the login and logout database and the LED off (e.g. red off).
From these data I get, I calculate the timestamp of each date, which would be the number of seconds elapsed from 01/01/1970 to the date where that particular action was performed, and I put it in the list of x then I transform the name of the various LEDs in numbers (red = 0, yellow = 1, etc ..). To predict the LED that the user would like to turn on, I take the current timestamp and use it as x_test, then I calculate a sort of manhattan distance, which is actually a simple subtraction between integers, between the current timestamp and the one contained in the database. Thus obtaining another list, which will then be sorted from the smallest to the largest and from this one will then derive the mode of the labels or the predicted value.
Since in doing so we use, to predict the value, the last actions made by the user, I thought of using a very high k (k = 41) so that he could have more samples on which to then do the mode and then since the classification is not binary using such a high k we try to avoid that the class is bimodal.
I have inserted a control so that if the LED lighting actions are less than 41, the web page will show “KNN IS NOT WORKING”.
