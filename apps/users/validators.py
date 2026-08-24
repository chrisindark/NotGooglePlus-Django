from django.core.validators import RegexValidator

ALPHABET_VALIDATOR = RegexValidator(r"^[a-zA-Z]*$", "Only letters are allowed.")

ALPHANUMERIC_VALIDATOR = RegexValidator(
    r"^[a-z][a-z0-9]*$",
    "Only lowercase letters and numbers are allowed. Value should start with a letter.",
)
