import random

# print('sanamsargui', __name__)

def sanamsargui_ner(*ners):
    return random.choice(ners)

def sanamsargui_too(a, b):
    return random.randint(a, b)

def sanamsargui_butarkhai():
    return random.random()

if __name__ == "__main__":
    print(sanamsargui_butarkhai())
    print(sanamsargui_too(10, 100))
