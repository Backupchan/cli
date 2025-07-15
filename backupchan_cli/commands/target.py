import requests
from backupchan_cli import utility
from backupchan import API, BackupType, BackupRecycleCriteria, BackupTarget, BackupRecycleAction

#
#
#

def setup_subcommands(subparser):
    list_cmd = subparser.add_parser("list", help="List all targets")
    list_cmd.set_defaults(func=do_list)

    view_cmd = subparser.add_parser("view", help="View a specific target")
    view_cmd.add_argument("id", type=str, help="ID of the target to view")
    view_cmd.add_argument("--include-recycled", "-r", action="store_true", help="Include recycled backups too")
    view_cmd.set_defaults(func=do_view)

#
# Value to human-readable string conversions and lookup tables
#

HR_TYPES = {
    BackupType.SINGLE: "Single file",
    BackupType.MULTI: "Multiple files"
}

HR_RECYCLE_ACTIONS = {
    BackupRecycleAction.DELETE: "Delete",
    BackupRecycleAction.RECYCLE: "Recycle"
}

def hr_recycle_criteria(target: BackupTarget) -> str:
    if target.recycle_criteria == BackupRecycleCriteria.NONE:
        return "None"
    elif target.recycle_criteria == BackupRecycleCriteria.AGE:
        return f"After {target.recycle_value} days"
    elif target.recycle_criteria == BackupRecycleCriteria.COUNT:
        return f"After {target.recycle_value} copies"
    return "(broken value)"

#
# backupchan target list
#

def do_list(args, _, api: API):
    try:
        targets = api.list_targets()
    except requests.exceptions.ConnectionError:
        utility.failure_network()

    for index, target in enumerate(targets):
        spaces = " " * (len(str(index + 1)) + 1)
        print(f" {index + 1}. |  {target.name}")
        print(f" {spaces} | ID: {target.id}")
        print(f" {spaces} | Type: {HR_TYPES[target.target_type]}")
        print(f" {spaces} | Recycle criteria: {hr_recycle_criteria(target)}")
        if target.recycle_criteria != BackupRecycleCriteria.NONE:
            print(f" {spaces} | Recycle action: {HR_RECYCLE_ACTIONS[target.recycle_action]}")
        print(f" {spaces} | Location: {target.location}")
        print(f" {spaces} | Name template: {target.name_template}")
        print("=========")

#
# backupchan target view
#

# TODO is it necessary to pass config to every subcommand?
def do_view(args, _, api: API):
    try:
        target, backups = api.get_target(args.id)
    except requests.exceptions.ConnectionError:
        utility.failure_network()

    print(f"Name: {target.name}")
    print(f"ID: {target.id}")
    print(f"Type: {HR_TYPES[target.target_type]}")
    print(f"Recycle criteria: {hr_recycle_criteria(target)}")
    if target.recycle_criteria != BackupRecycleCriteria.NONE:
        print(f"Recycle action: {HR_RECYCLE_ACTIONS[target.recycle_action]}")
    print(f"Location: {target.location}")
    print(f"Name template: {target.name_template}")
    print()
    print("Backups (pass -r to view recycled ones too):")
    print()

    if not args.include_recycled:
        backups = [backup for backup in backups if not backup.is_recycled]

    for index, backup in enumerate(backups):
        spaces = " " * (len(str(index + 1)) + 1)
        print(f" {index + 1}. | ID: {backup.id}")
        print(f" {spaces} | Created at: {backup.pretty_created_at()}")
        if args.include_recycled:
            print(f" {spaces} | Recycled: {'Yes' if backup.is_recycled else 'No'}")
        print("=========")
