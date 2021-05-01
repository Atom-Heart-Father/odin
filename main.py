import os
from python_terraform import Terraform, IsFlagged

# DO_PATH = os.path.abspath(os.path.join(os.curdir, "configs", "digitalocean"))
DO_PATH = os.path.abspath(os.path.join(os.curdir, "configs", "digitalocean"))
os.chdir(DO_PATH)

t = Terraform()

def get_instance_type(provider: str, mem: str, cpu: str):
    resource = str(cpu) + "vcpu-" + str(mem) + "gb"
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

async def father(details = None):
    deets = {
        "os": "ubuntu-16-04-x64",
        "name": "TestPy",
        "memory": "1",
        "processor": "1",
        "region": "nyc3",
    }

    if details:
        deets = details

    return_code, stdout, stderr = t.plan(
        out=DO_PATH+'/out.txt',
        vars={
            "image": deets["os"],
            "name": deets["name"],
            "size": get_instance_type("DigitalOcean", deets["memory"], deets["processor"]),
            "region": deets["region"],
        }
    )

    return_code, stdout, stderr = t.apply(
        DO_PATH+'/out.txt',
        var=None,
        **{"skip_plan": True, "auto_approve": IsFlagged, "capture_output": True}
    )

    if stderr:
        print(str(stderr))
        return False
    else:
        print(str(stdout))
        return True

if __name__ == "__main__":
    father()
