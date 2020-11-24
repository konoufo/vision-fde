# import re
#
# my_str ="a,b,c,test(1,2,3),g,h,test(2,4,6)"
#
# print(re.split('(?<!\(.),(?!.\))', my_str))


nutriments_principaux_13 = "lipides, lipides saturés,lipides trans, cholestérol, sodium, glucides, fibres, sucres, protéines, protein,carboxhydrate,sugar,sugars,calories,calorie,cholesterol, vitamine A,vitamine C, calcium, Fer"
nutriments_principaux_13 = nutriments_principaux_13.split(",")
nutriments_speciaux = "saturés, saturated, trans, polyinsaturés, oméga, monoinsaturés, fibres, sucres, B6, B-6, B12, B-12, vitamine,iron"
nutriments_speciaux = nutriments_speciaux.split(",")
nutriments_facultatifs = "folate, magnésium, niacine, phosphore, potassium, riboflavine, sélénium, thiamine, vitamine B12, vitamine B6, vitamine D, vitamine E, zinc" \
                         ",Pantothénate,Valeur,Valeur é, Valeur énergétique"
nutriments_facultatifs = nutriments_facultatifs.split(",")
all = nutriments_principaux_13 + nutriments_facultatifs + nutriments_speciaux

print(all)
print(list(set(all)))