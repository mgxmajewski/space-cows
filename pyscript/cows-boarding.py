from datetime import datetime as dt

from utils import add_class, remove_class

cows_transport = []

cows_transport_dict = {}

# define the task template that will be use to render new templates to the page
cow_template = Element("task-template").select(".task", from_content=True)
cow_list = Element("list-tasks-container")
new_cow_name = Element("new-cow-name")
new_cow_weight = Element("new-cow-weight")


def add_cow(*ags, **kws):
    # ignore empty task
    if not new_cow_name.element.value or not new_cow_weight.element.value:
        return None

    # create task
    cow_id = f"task-{len(cows_transport)}"
    cow = {
        "id": cow_id,
        "content": f"{new_cow_name.element.value}: {new_cow_weight.element.value}",
        # "content": new_cow_name.element.value,
        "done": False,
        "created_at": dt.now(),
    }

    cows_transport.append(cow)
    cows_transport_dict[new_cow_name.element.value] = new_cow_weight.element.value
    print(cows_transport_dict)

    # add the task element to the page as new node in the list by cloning from a
    # template
    cow_html = cow_template.clone(cow_id, to=cow_list)
    cow_html_content = cow_html.select("p")
    cow_html_content.element.innerText = cow["content"]
    cow_html_check = cow_html.select("input")
    cow_list.element.appendChild(cow_html.element)

    def check_cow(evt=None):
        cow["done"] = not cow["done"]
        if cow["done"]:
            add_class(cow_html_content, "line-through")
        else:
            remove_class(cow_html_content, "line-through")

    new_cow_name.clear()
    new_cow_weight.clear()
    cow_html_check.element.onclick = check_cow


def add_cow_event(e):
    if e.key == "Enter":
        add_cow()


new_cow_name.element.onkeypress = add_cow_event
