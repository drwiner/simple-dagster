import dagster


@dagster.asset(config_schema={"env": str})
def get_env(context):
    context.log.info("env: " + context.op_config["env"])
    return context.op_config["env"]

@dagster.op
def using_env(get_env):
    print(f"using env {get_env}")

# Only difference in this example is the cloud vs local

@dagster.job
def do_atm():
    using_env(get_env())


if __name__ == "__main__":
    # Will log "config_param: stuff"
    do_atm.execute_in_process(
        run_config={"ops": {"get_env": {"config": {"env": "CLOUD"}}}}
    )