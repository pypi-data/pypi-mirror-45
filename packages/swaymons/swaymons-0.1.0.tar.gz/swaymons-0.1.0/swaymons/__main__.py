from . import create_parser, main

if __name__ == '__main__':
    args = create_parser().parse_args()
    main(args)
