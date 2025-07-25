import requests.exceptions
import os
from backupchan_cli import utility
from backupchan import API, BackupchanAPIError

#
#
#

def setup_subcommands(subparser):
    #
    #
    #

    upload_cmd = subparser.add_parser("upload", help="Upload a backup")
    # For things like cron jobs etc. using the cli
    upload_cmd.add_argument("--automatic", "-a", action="store_true", help="Mark backup as having been added automatically")
    upload_cmd.add_argument("target_id", type=str, help="ID of the target to upload backup to")
    upload_cmd.add_argument("filename", type=str, help="Name of the file to upload")
    upload_cmd.set_defaults(func=do_upload)

    #
    #
    #

    delete_cmd = subparser.add_parser("delete", help="Delete an existing backup")
    delete_cmd.add_argument("id", type=str, help="ID of the backup to delete")
    delete_cmd.add_argument("--delete-files", "-d", action="store_true", help="Delete backup files as well")
    delete_cmd.set_defaults(func=do_delete)

#
# backupchan backup upload
#

def do_upload(args, _, api: API):
    with open(args.filename, "rb") as file:
        try:
            api.upload_backup(args.target_id, file, os.path.basename(args.filename), not args.automatic)
        except requests.exceptions.ConnectionError:
            utility.failure_network()
        except BackupchanAPIError as exc:
            utility.failure(f"Failed to upload backup: {str(exc)}")
    print("Backup uploaded.")

#
# backupchan backup delete
#

def do_delete(args, _, api: API):
    delete_files = args.delete_files

    try:
        api.delete_backup(args.id, delete_files)
    except requests.exceptions.ConnectionError:
        utility.failure_network()
    except BackupchanAPIError as exc:
        if exc.status_code == 404:
            utility.failure("Backup not found")
        utility.failure(f"Failed to delete backup: {str(exc)}")

    print("Backup deleted.")
