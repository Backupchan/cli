import os
from backupchan import API

#
#
#

def setup_subcommands(subparser):
    upload_cmd = subparser.add_parser("upload", help="Upload a backup")
    # For things like cron jobs etc. using the cli
    upload_cmd.add_argument("--automatic", "-a", action="store_true", help="Mark backup as having been added automatically")
    upload_cmd.add_argument("target_id", type=str, help="ID of the target to upload backup to")
    upload_cmd.add_argument("filename", type=str, help="Name of the file to upload")
    upload_cmd.set_defaults(func=do_upload)

#
# backupchan backup upload
#

def do_upload(args, _, api: API):
    with open(args.filename, "rb") as file:
        api.upload_backup(args.target_id, file, os.path.basename(args.filename), not args.automatic)
    print("Backup uploaded.")
