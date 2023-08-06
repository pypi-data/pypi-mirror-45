import argparse as ap

# basic funcion that gets a dict from an namespace


def namespace_to_dict(namespace):
    return_dict = {}
    for key, value in namespace._get_kwargs():
        return_dict[key] = value
    return return_dict


# tries to parse arguments given in the command line and if there aren't it gets arguments from input returns a dict


def try_parse(*args):
    try:
        parser = ap.ArgumentParser()
        for arg in args:
            parser.add_argument(arg)
        return namespace_to_dict(parser.parse_args())
    except:
        return_args = {}
        for arg in args:
            return_args[arg] = input("enter " + arg + " value: ")
        return return_args


# gets arguments given in the command line returns a dict


def fast_parse(*args):
    parser = ap.ArgumentParser()
    for arg in args:
        parser.add_argument(arg)
    return namespace_to_dict(parser.parse_args())


if __name__ == "__main__":
    print(
        """Welcome to FastParse, to start you can first import the modules "from fastparse import fastparse.
    To get more details about the module read the "Readme.md" attached to this module """
    )
