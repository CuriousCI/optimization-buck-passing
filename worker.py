import argparse
import barrel


def blackbox(config: barrel.Config) -> int:
    return 0


OPENBOX_URL: str = ""


def main() -> None:
    argument_parser = argparse.ArgumentParser()
    _ = argument_parser.add_argument("task_id")
    task_id: barrel.OpenBoxTaskId = str(argument_parser.parse_args().task_id)  # pyright: ignore[reportAny]

    # args: argparse.Namespace =

    suggestion = barrel.get_suggestion(task_id=task_id, base_url=OPENBOX_URL)
    print(suggestion)
    barrel.update_observation(task_id=task_id, base_url=OPENBOX_URL)


if __name__ == "__main__":
    main()
