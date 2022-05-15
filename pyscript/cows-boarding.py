from datetime import datetime as dt

from utils import add_class, remove_class
from ps1 import greedy_cow_transport, brute_force_cow_transport

cows_transport = []
cows_transport_dict = {}

results_count = 0

# define the task template that will be use to render new templates to the page
cow_template = Element("cow-list-template").select(".cow", from_content=True)
result_template = Element("result-list-template").select(".result", from_content=True)
cow_trip_div = Element("cow-trip-container")
results_div = Element("results-container")
new_cow_name = Element("new-cow-name")
new_cow_weight = Element("new-cow-weight")
start_optimizing_greedy_btn = Element("start-optimizing-greedy-btn")
start_optimizing_brute_btn = Element("start-optimizing-brute-btn")
remove_cows_btn = Element("remove-cows-btn")


def add_cow(*ags, **kws):
    # ignore empty cow input
    if not new_cow_name.element.value or not new_cow_weight.element.value:
        return None

    # create cow
    cow_id = f"cow-{len(cows_transport)}"
    cow = {
        "id": cow_id,
        "content": f"{new_cow_name.element.value}: {new_cow_weight.element.value}",
        "done": False,
        "created_at": dt.now(),
    }

    cows_transport.append(cow)
    cows_transport_dict[new_cow_name.element.value] = int(new_cow_weight.element.value)

    # add the task element to the page as new node in the list by cloning from a
    # template
    cow_html = cow_template.clone(cow_id, to=cow_trip_div)
    cow_html_content = cow_html.select("p")
    cow_html_content.element.innerText = cow["content"]
    cow_html_check = cow_html.select("input")
    cow_trip_div.element.appendChild(cow_html.element)

    def delete_cow(e):
        cow_html.element.remove()
        current_cow_paragraph = cow_html.element.children.item(0).children.item(1)
        current_cow_name = current_cow_paragraph.innerHTML.split(':')[0]
        del cows_transport_dict[current_cow_name]

    new_cow_name.clear()
    new_cow_weight.clear()
    cow_html_check.element.onclick = delete_cow


def add_result(algo_type):
    # create result
    global results_count
    result_id = f"result-{results_count}"
    result = {
      "id": result_id,
      "content": f"{algo_type.__name__}, {algo_type(cows_transport_dict)}",
      "done": False,
      "created_at": dt.now(),
    }

    results_count += 1

    # add the task element to the page as new node in the list by cloning from a
    # template
    result_html = result_template.clone(result_id, to=results_div)
    result_html_content = result_html.select("p")
    result_html_content.element.innerText = result["content"]
    results_div.element.appendChild(result_html.element)


def add_cow_event(e):
    if e.key == "Enter":
        add_cow()


def start_cow_transport_optimization_greedy_event(e):
    add_result(greedy_cow_transport)
    # greedy_cow_transport(cows_transport_dict)


def start_cow_transport_optimization_brute_event(e):
    add_result(brute_force_cow_transport)


new_cow_name.element.onkeypress = add_cow_event
start_optimizing_greedy_btn.element.onclick = start_cow_transport_optimization_greedy_event
start_optimizing_brute_btn.element.onclick = start_cow_transport_optimization_brute_event
