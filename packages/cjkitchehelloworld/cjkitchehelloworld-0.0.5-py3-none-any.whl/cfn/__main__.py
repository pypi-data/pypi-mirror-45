import sys
from cfn.hello import say_hello


def main():
  print(say_hello())



if __name__ == "__main__":
    try:
      main()
    except Exception:
      raise(e)