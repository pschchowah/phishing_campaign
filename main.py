from Scripts.generate import Generator

# Initialize the Generator class
gen = Generator()
gen.connect()
gen.initialize_model()

# Generate text
gen.generate_text(prompt="Write down Fibonnaci suite first 20 numbers")