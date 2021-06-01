CS1999: Buggy Race Editor TESTING MANUAL
=========================

## STEPS FOR MANUAL TESTING

1. Test "Make Buggy"
	* If you try to submit it when you open It, It should create or edit a table with ID of the buggy = 1
		** If you try to put a cost limit of the buggy, even if you change all the values automaticcaly, It will create you a random buggy based on the cost limit.
	* Add more wheels than tyres, It should give you an error message
	* Try to define the tyres select as empty, It should give you another error message
	* Try to define the pattern of the flag select as empty, It should give you another error message
	* Try to define the type of power select as empty, It should give you another error message
	* Try to define the type of power select as "Hamster", It should show you another input for the hamster booster, do the same for the auxiliary power
	* Try to use the buttons of the selects at the end, you can't use the final selects because are based on the button interaction
	
2. Show Buggy
	* Try to press "Edit Buggy" button and check if It goes to the buggy editor of that buggy
	* Try to delete a buggy pressing the button "delete me" under that buggy and after go back to the home and come back to the "show buggy" page to check if It still there or not (It should be deleeted)
	* Try to delete all the buggies pressing the button "Delete all", and after go back to the home and come back to the "show buggy" page to check if the database is empty and if It shows you "No Buggies, press "Home"
	 
3. GET BUGGY JSON
	* Try to get the json of the first buggy pressing on "Get buggy JSON" on the main page
	* If the database It's empty It should appear an error message, if not, It should appear the json of the first buggy

4. GET ALL BUGGIES JSON
	* Do the same as the point 3. GET BUGGY JSON but obtaining all the buggies json

5. Show the Poster
	* Try to open the poster!

[Test it now!](http://localhost:5000)


