from ipinfo import trysites
import rich


def main():
    finaldata = trysites.trysites()
    if not finaldata:
        print("None of the IP sites could return even a valid IP.",
              "Perhaps check your network connection?")
    else:
        rich.print(finaldata)


if __name__ == "__main__":
    main()
