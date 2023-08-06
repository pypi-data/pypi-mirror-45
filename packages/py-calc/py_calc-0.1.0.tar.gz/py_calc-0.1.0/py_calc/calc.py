#import click

#@click.command()
#def cli():
#    click.echo("Hello, World!")

def add(x, y):
    """Add Function"""
    return x + y


def subtract(x, y):
    """Subtract Function"""
    return x - y


def multiply(x, y):
    """Multiply Function"""
    return x * y


def divide(x, y):
    """Divide Function"""
    if y == 0:
        raise ValueError('Can not divide by zero!')
    return x / y



if __name__ == '__main__':
    print(add(10,5))
    print(subtract(10,5))
    print(multiply(10,5))
    print(divide(10,5))
