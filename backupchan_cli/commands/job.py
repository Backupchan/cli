from backupchan.api import API
from backupchan_cli import utility

def setup_subcommands(subparser):
    list_cmd = subparser.add_parser("list", help="List all jobs")
    list_cmd.set_defaults(func=do_list)

    force_run_cmd = subparser.add_parser("forcerun", help="Force re-run a scheduled job")
    force_run_cmd.add_argument("name", help="Name of the scheduled job to run")
    force_run_cmd.set_defaults(func=do_force_run)

#
# backupchan job list
#

def do_list(args, api: API):
    delayed_jobs, scheduled_jobs = api.list_jobs()
    if len(delayed_jobs) == 0:
        print("There are currently no delayed jobs.")
    else:
        print("Delayed jobs:")
        for job in delayed_jobs:
            print(f"#{job.id} / {job.name} / Status: {job.status} / Start time: {job.pretty_start_time()} / End time: {job.pretty_end_time()}")

    print("\nScheduled jobs:")
    for job in scheduled_jobs:
        print(f"{job.name} / Interval: {job.interval} / Next run at {job.pretty_next_run()}")

#
# backupchan job forcerun
#

def do_force_run(args, api: API):
    api.force_run_job(args.name)
    print(f"Scheduled job {args.name} has been started. Check the log for more details.")
