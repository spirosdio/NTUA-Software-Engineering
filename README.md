# Σχολή Ηλεκτρολόγων Μηχανικών & Μηχανικών Η/Υ, ΕΜΠ

Εργασία στο μάθημα Τεχνολογία Λογισμικού - Χειμερινό εξάμηνο 2021-2022

## Ομάδα 01

| Επώνυμο             | Όνομα        | Αριθμός Μητρώου |
|---------------------|--------------|-----------------|
| Τσαούσης            | Κωνσταντίνος |   3117652       |
| Σπύρος              |  Διώχνος     |   3117043       |
| Χρήστος               | Μαρρές      |   3118912       |

## Δομή φακέλων

Η υποχρεωτική κοινή δομή των φακέλων του repository περιγράφεται στο έγγραφο των παραδοτέων (βλ. moodle μαθήματος). 

Η δομή των φακέλων στο συγκεκριμένο παράδειγμα είναι η εξής:

* Στον φάκελο `backend` περιέχεται ο κώδικας του back-end, του api και του συνολικού testing.
* Στον φάκελο `cli` περιέχεται ο κώδικας του command line application.


## Κύριες τεχνολογίες του παραδείγματος


### Back-end

* [Django](https://www.djangoproject.com/)
* [Django rest framework](https://www.django-rest-framework.org/)

### CLI client

* [Node](https://nodejs.org/en/)
* [Commander js](https://www.npmjs.com/package/commander)
* [Axios js](https://www.npmjs.com/package/axios)

## Oδηγίες



*	Προκειμένου να εγκατασταθεί το project πρέπει να γίνουν τα εξής: (Θεωρείται πως οι εντολές "python" και "pip" ισχύουν στο σύστημα, και αν όχι αντίστοιχα οι "python3" ή "pip3", καθώς και η venv)

*	Για το back-end/api πρέπει να γίνουν: pip install τα requirements που υπάρχουν στο requirements.txt

	Αφού γίνει clone το repo:

	```
	source activate στο φάκελο venv/bin για να ξεκινήσει virtual environment (optional) 
	python manage.py makemigrations (στο φάκελο backend/tolls21) 
	python manage.py migrate (στο φάκελο back-end/tolls21) 
	python manage.py populate
	``` 
	Η εντολή populate δεν είναι built in αλλα την έχουμε φτιάξει εμείς, γεμίζει όλα τα tables με ενδεικτικά data.
	
	Η εντολή είναι:
	
	```
	python manage.py runserver 9103 
	```
	(όσο βρίσκεται στο αρχείο backend/tolls21 για να τρέξει ο server στο port 9103 - πιθανά σφάλματα αφορούν την pip install εντολή)

	Χρειάζεται να μπορεί να οριστεί η εντολή "se2101" του node.js globally στον υπολογιστή.




* Το REST API base URL είναι το `http://localhost:9103/interoperability/api`, όπως απαιτείται από την εργασία. 


# ntua-tl21-01
