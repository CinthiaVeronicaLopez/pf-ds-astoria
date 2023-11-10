# Diccionario de datos


## Google Maps

### metadata_sitios:
La metadata contiene información del comercio, incluyendo localización, atributos y categorías.

    • 'name': 'Walgreens Pharmacy', 
    • 'address': 'Walgreens Pharmacy, 124 E North St, Kendallville, IN 46755', 
    • 'gmap_id': '0x881614ce7c13acbb:0x5c7b18bbf6ec4f7e', 
    • 'description': 'Department of the Walgreens chain providing prescription medications & other health-related items.', 
    • 'latitude': 41.451859999999996, 
    • 'longitude': -85.2666757, 
    • 'category': ['Pharmacy'], 
    • 'avg_rating': 4.2, 
    • 'num_of_reviews': 5, 
    • 'price': '$$', 
    • 'hours': [['Thursday', '8AM–1:30PM'], ['Friday', '8AM–1:30PM'], ['Saturday', '9AM–1:30PM'], ['Sunday', '10AM–1:30PM'], ['Monday', '8AM–1:30PM'], ['Tuesday', '8AM–1:30PM'], ['Wednesday', '8AM–1:30PM']], 
    • 'state': 'Closes soon ⋅ 1:30PM ⋅ Reopens 2PM', 
    • 'url': 'https://www.google.com/maps/place//data=!4m2!3m1!1s0x881614ce7c13acb
    • b:0x5c7b18bbf6ec4f7e?authuser=-1&hl=en&gl=us'

### review-estados    
Se disponibiliza las reviews de los usuarios se conforman de la siguiente manera 
     
    •  'user_id': '101463350189962023774',   
    •  'name': 'Jordan Adams', 
    •  'time': 1627750414677, 
    •  'rating': 5, 
    •  'text': 'Cool place, great people, awesome dentist!', 
    • 'gmap_id': '0x87ec2394c2cd9d2d:0xd1119cfbee0da6f3'

   
## Dataset de Yelp!

### business.pkl 

Contiene información del comercio, incluyendo localización, atributos y categorías.

    •  business_id": "tnhfDv5Il8EaGSXZGiuQGg",
    • "name": "Garaje",
    • "address": "475 3rd St",
    •  "city": "San Francisco",
    •  "state": "CA",
    •  "postal code": "94107",
    •  "latitude": 37.7817529521,
    •  "longitude": -122.39612197,
    •  "stars": 4.5,
    •  "review_count": 1198,
    •  "is_open": 1,(0 = cerrado, 1= abierto)
    •  "categories": ["Mexican","Burgers","Gastropubs",

### review.json 

Contiene las reseñas completas, incluyendo el user_id que escribió el review y el business_id por el cual se escribe la reseña

    • "review_id": "zdSx_SD6obEhz9VrW9uAWA",
    •  string, 22 caracteres id único de usuario, refiere al usuario en user.json
    • "user_id": "Ha3iJu77CxlrFm-vQRs_8g",
    •  "business_id": "tnhfDv5Il8EaGSXZGiuQGg",
    •  "text": "Great place to hang out after work: the prices are decent, and the ambience is fun. It's a bit loud, but very lively. The staff is friendly, and the food is good. They have a good selection of drinks.",
    • "useful": 0,

### user.parquet
 Data del usuario incluyendo referencias a otros usuarios amigos y a toda la metadata asociada al usuario.

    • "user_id": "Ha3iJu77CxlrFm-vQRs_8g",
    •  "name": "Sebastien",
    •  "review_count": 56(numero de reseñas escritas),
    •  "yelping_since": "2011-01-01"(fecha de creación del usuario en Yelp en formato YYYY-MM-DD),
    •  "friends": ["wqoXYLWmpkEH0YvTmHBsJQ",
         "KUXLLiJGrjtSsapmxmpvTA",
         "6e9rJKQC3n0RSKyHLViL-Q"](id de usuarios que son amigos de ese usuario),
    • "useful": 21(número de votos marcados como útiles por el usuario),
    •  "funny": 88(número de votos marcados como graciosos por el usuario),
    •  "cool": 15(número de votos marcados como cool por el usuario),
    •   "fans": 1032(número de fans que tiene el usuario),
    • "elite": [2012, 2013]( años en los que el usuario fue miembro elite),
    •  "average_stars": 4.31(promedio del valor de las reseñas),
    •  "compliment_hot": 339(total de cumplidos 'hot' recibidos por el usuario),
    •  "compliment_more": 668(total de cumplidos varios recibidos por el usuario),
    •  "compliment_profile": 42(total de cumplidos por el perfil recibidos por el usuario),
    •  "compliment_cute": 62(total de cumplidos 'cute' recibidos por el usuario),
    •  "compliment_list": 37(total de listas de cumplidos recibidos por el usuario),
    •  "compliment_note": 356(total de cumplidos como notas recibidos por el usuario),	
    •  "compliment_plain": 68(total de cumplidos planos recibidos por el usuario),
    •  "compliment_cool": 91(total de cumplidos 'cool' recibidos por el usuario),
    •  "compliment_funny": 99(total de cumplidos graciosos recibidos por el usuario),
    •  "compliment_writer": 95(cumplidos escritos recibidos por el usuario),
    •  "compliment_photos": 50(cumplidos en foto recibidos por el usuario)

### checkin.json 

    • "business_id": "tnhfDv5Il8EaGSXZGiuQGg"
    •  "date": "2016-04-26 19:49:16, 2016-08-30 18:36:57, 2016-10-15 02:45:18, 2016-11-18 01:54:50, 2017-04-20 18:39:06, 2017-05-03 17:58:02"

### tip.json

 Tips (consejos) escritos por el usuario. Los tips son más cortas que las reseñas y tienden a dar sugerencias rápidas.

    •  "text": "Secret menu - fried chicken sando is da bombbbbbb Their zapatos are good too.",
    •  "business_id": "tnhfDv5Il8EaGSXZGiuQGg",
    •  "user_id": "49JhAJh8vSQ-vM4Aourl0g"

