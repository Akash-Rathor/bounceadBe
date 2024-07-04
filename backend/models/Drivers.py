from cerberus import Validator, SchemaError

# Define the schema with dependencies rule
schema = {
    "user_type": {"type": "string", "required": True},
    "name": {"type": "string", "required": False},
    "email": {"type": "string", "required": False},
    "mobile": {"type": "integer", "required": False},
    # '_dependencies': {
    #     'dependencies': {
    #         'email': ['mobile'],
    #         'mobile': ['email']
    #     }
    # }
}

# Create a validator instance
v = Validator(schema)


# Function to validate that at least one of email or mobile is present
def validate_data(data):
    if "email" not in data and "mobile" not in data:
        return False, "At least one of 'email' or 'mobile' must be present."
    return v.validate(data), v.errors if v.errors else None


# Sample data
data = {"user_type": "admin", "name": "John Doe"}

# Validate data
is_valid, errors = validate_data(data)
if is_valid:
    print("Data is valid.")
else:
    print("Data is invalid.")
    print(errors)
