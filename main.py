import os
from python_terraform import Terraform, IsFlagged

# DO_PATH = os.path.abspath(os.path.join(os.curdir, "configs", "digitalocean"))
DO_PATH = os.path.abspath(os.path.join(os.curdir, "configs", "digitalocean", "do.tf"))
print(DO_PATH)

t = Terraform()

t.init(DO_PATH)


def get_instance_type(provider: str, mem: str, cpu: str):
    resource = cpu + "-" + mem
    mappings = {"DigitalOcean": {}}
    mappings["DigitalOcean"] = {
        "1vcpu-1gb": "s-1vcpu-1gb",
        "1vcpu-2gb": "s-1vcpu-2gb",
        "3vcpu-1gb": "s-3vcpu-1gb",
        "2vcpu-2gb": "s-2vcpu-2gb",
        "1vcpu-3gb": "s-1vcpu-3gb",
        "2vcpu-4gb": "s-2vcpu-4gb",
        "4vcpu-8gb": "s-4vcpu-8gb",
    }

    if provider in mappings:
        if resource in mappings[provider]:
            return mappings[provider][resource]

    return None


deets = {
    # "os": "Ubuntu 16",
    "os": "ubuntu-16-04-x64",
    "name": "Test",
    "memory": "1gb",
    "processor": "1vcpu",
    # "region": "United States",
    "region": "us-east-2",
}

return_code, stdout, stderr = t.apply(
    DO_PATH,
    vars={
        "image": deets["os"],
        "name": deets["name"],
        "size": get_instance_type("DigitalOcean", deets["memory"], deets["processor"]),
        "region": deets["region"],
    },
    **{"skip_plan": True, "auto_approve": IsFlagged, "capture_output": True}
)

if stderr:
    print(str(stderr))
else:
    print(str(stdout))
