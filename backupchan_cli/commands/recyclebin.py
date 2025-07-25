from backupchan import API

#
#
#

def setup_subcommands(subparser):
    view_cmd = subparser.add_parser("view", help="View recycle bin")
    view_cmd.set_defaults(func=do_view)

    clear_cmd = subparser.add_parser("clear", help="Clear recycle bin")
    clear_cmd.set_defaults(func=do_clear)
