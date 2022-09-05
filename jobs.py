import dagster


@dagster.asset
def get_config(context):
    context.log.info("config: " + str(context.op_config))
    return context.op_config

@dagster.op
def using_config(get_config):
    for key, value in get_config.items():
        print(f"using {key} {value}")


@dagster.job
def do_atm():
    using_config(get_config())


if __name__ == "__main__":
    do_atm.execute_in_process(
        run_config={"ops": {"get_config": {"config": {"env": "dev", "application": "do_stuff"}}}}
    )