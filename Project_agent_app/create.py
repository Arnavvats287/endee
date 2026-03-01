from endee import Endee, Precision

INDEX_NAME = "hr_policies"
DIMENSION = 384

# Connect
client = Endee()

# index
client.create_index(
    name=INDEX_NAME,
    dimension=DIMENSION,
    space_type="cosine",
    precision=Precision.INT8 #facing problems at precison , idk if its the library or the way im using it, will check later
)

print(f"Index '{INDEX_NAME}' created successfully.")