### Titanic - Machine Learning from Disaster

I participated in the Kaggle challenge where it was necessary to predict whether a passenger had survived or not.

After reading the train and test files, I started the preprocessing phase, eliminating the "Cabin" and "Ticket" columns as they are partial, the "ID" column, and the "Name" column because they are not relevant to me.
Then I switched to one hot encoding on the "Sex" and "Embarked" columns. Lastly, I filled in the few empty lines of the "Fare" and "Age" columns with the respective median.

I defined various machine learning models for which understanding was best.
Since there were no labels in the Kaggle test dataset, I thought of using, as metrics, the score and the percentage of 1 in the aforementioned label, which must be similar to the percentage of the train.
Furthermore, again to try to overcome this problem, I used a K-Fold, using the validation set part as a test set, calculating the accuracy.

Thanks to all this, I have identified the Random Forest with the best score and the percentage of 1 most similar to the train.
Obtaining a score of 97.98 and a percentage of 1 equal to 36.84%.

Submitting the results to Kaggle, I got a 75% score.


<!---

Titanic Kaggle challenge

Ho partecipato alla sfida di kaggle dove bisognava prevedere se un passeggero fosse sopravissuto oppure no.

Dopo aver letto i file di train e test, ho cominciato la fase di preprocessing, eliminando le colonne "Cabin" e "Ticket" poichè parziali, la colonna "ID" e la colonna "Name" perchè per me non rilevanti.
Dopo sono passato a fare one hot encoding sulle colonne "Sex" e "Embarked". Per ultimo ho rimepito le poche righe vuote delle colonne "Fare" e "Age" con la rispettiva mediana.

Ho definito vari modelli di Machine Learning per capire quale fosse il migliore.
Dato che nel dataset di test di kaggle non erano presenti le label, ho pensato di utilizzare, come metriche, lo score e la percentuale di 1 nella label predetta, che deve essere simile alla percentuale del train.
Inoltre, sempre per cercare di ovviare a questo problema, ho utilizzato un K-Fold, utilizzando la parte di validation set come test set calcolandoci l'accuracy.

Grazie a tutto questo, ho individuato la Random Forest con lo score migliore e la percentuale di 1 più simile a quella di train.
Ottenendo uno score di 97.98 e una percentuale di 1 uguale a 36.84 %.

Inviando i risultati a kaggle, ho ottenuto uno score del 75%.
--->
