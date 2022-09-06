import dagster


@dagster.asset(config_schema=dict)
def get_config(context):
    context.log.info("config: " + str(context.op_config))
    return context.op_config


@dagster.op(config_schema={"key": str})
def using_config(context, get_config):
    x = context.op_config["key"]
    print (f"using route {x}")
    # print("ok")
    for key, value in get_config.items():
        print(f"using {key} {value}")

    return True

@dagster.op
def using_default_config(get_config):
    print("No Config Key: Use Default")
    for key, value in get_config.items():
        print(f"using default {key} {value}")
    return True

@dagster.op
def combine(context, a: bool, b: bool):
    print("combined")


@dagster.job
def do_configured_job():
    x = get_config()
    a = using_config(x)
    b = using_default_config(x)
    combine(a, b)


if __name__ == "__main__":
    do_configured_job.execute_in_process(
        run_config={"ops": {"using_config": {"config": {"key": "value"}}, "get_config": {"config": {"env": "dev", "application": "do_stuff"}}}}
    )