Import os
Import django
From djangoapp.models import Product

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()

def initiate():
	product_type = [
	{“name”:“Pack”, “description”:”Single Expansion Pack”},
	{“name”:”Box”, “description”:”Collection of booster packs and possibly additional products/cards”},
	]

card_instances = [] 
for data in product_data:
	card_instances.append(
	Product.objects.create(
	    name=data[‘name’], description=data[‘description’]
	)
)

card_detail_data = [
{
	“name”: “Booster Pack”,
	“type”: “Sealed”,
	“year”:”2023”
	“product_type”: card_instances[0]
},
]

for data in card_detail_data:
	CardModel.objects.create(
		name=data[‘name’], product_type=data[‘product_type’], type=data[‘type’]
		year=data[‘year’]
	)

If __name__ == “__main__”:
	initiate()
	
